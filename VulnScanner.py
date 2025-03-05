import json
import queue
import re
import time
import datetime
import xmltodict
import socket
import copy
from gvm.xml import pretty_print
from lxml import etree

from VulnScanCreds import VulnScanCreds
from VulnController import VulnController
from VulnScannerDB import VulnScannerDB
from VulnLogger import VulnLogger
from VulnSysLogger import VulnSysLogger
from VulnTarget import VulnTarget
from VulnTask import VulnTask
from VulnReport import VulnReport
from VulnPortList import VulnPortList
from safe_schedule import SafeScheduler


class VulnScanner:

    # def __init__(self, name, configFile, dbFile, keepReports, scanner_id):
    def __init__(self, name, dbFile, user, password, log_host, log_port, keepReports, scanner_id, scanner_host=None,
                 scanner_port=None):
        self._controller = VulnController
        self.scheduler = SafeScheduler()
        self._targets = {}
        self._tasks = {}
        self._port_list = {}
        self._scan_configs = {}
        self._scan_creds = {}
        self._jobs = {}
        self._queue = queue.Queue()
        self.name = name
        self.log_host = log_host
        self.log_port = log_port
        # self.cfg_path = configFile
        self.data_path = dbFile
        self._keepReports = keepReports
        self._vulnscanner_id = scanner_id
        self._status = "created"
        # hostname to uniquely identify vulnscanner
        self.hostname = socket.gethostname()
        self.logger = None
        # cfg = self._controller.configRead(cfg_path=configFile)
        # create controller as object with data from configFile
        if scanner_host is not None and scanner_port is not None:
            self._controller = VulnController(scanner_host=scanner_host, scanner_port=scanner_port, username=user,
                                              password=password)
        else:
            self._controller = VulnController(socket_path="/opt/gvm/var/run/gvmd.sock", username=user,
                                              password=password)
        # create/open and init db for current status of reports
        self._db = VulnScannerDB(dbFile=dbFile)

        cur = self._db.getAllTargets()
        rows = cur.fetchall()

        for i in rows:
            self._targets[i[0]] = (
                VulnTarget(target_id=i[0], name=i[1], hosts=i[2], exclude_hosts=i[3], port_list_id=i[4]))

        self._checkTargets()

        # init all tasks from DB
        cur = self._db.getAllTasks()
        rows = cur.fetchall()

        for i in rows:
            task_id = i[0]

            # target didnt change from last time task was updated
            if i[2] in self._targets:
                target_id = i[2]
            # target is new and can be mapped to task
            else:
                for curtargetid in self._targets:
                    if i[1] == (self._targets[curtargetid].getName() + "_" + self._targets[curtargetid].getHosts()):
                        target_id = curtargetid
                        continue

            scan_config = i[3]
            frequency = i[4]
            interval = i[5]
            start_time = i[6]
            self._tasks[i[0]] = (
                VulnTask(task_id=task_id, target=self._targets[target_id], scan_config=scan_config, frequency=frequency,
                         interval=interval, start_time=start_time))
            # if target specified in task_config is available in targets
            if target_id in self._targets:
                self._tasks[task_id] = VulnTask(target=self._targets[target_id], scan_config=scan_config,
                                                interval=interval,
                                                frequency=frequency, start_time=start_time, task_id=task_id)
        self._checkTasks()

        for i in self._tasks:
            self._updateConfig(my_object=self._tasks[i])

        self._initPortList()
        self._initScanConfigs()
        self._initScanCreds()

    # except Exception as e:
    #    print(self.name + " init exception")
    #    print(str(e))

    def __repr__(self):
        return self.name

    def addlogger(self):
        # create logger with data from configFile
        if self.log_host == "FileBeat":
            self._logger = VulnSysLogger(name=self.name, ident=self.hostname)
        else:
            self._logger = self._loggerCreate(name=self.name + "_logger", log_host=self.log_host,
                                              log_port=self.log_port,
                                              ident=self.hostname)

    def _loggerCreate(self, name, log_host, log_port, ident):
        return VulnLogger(name=name, log_host=log_host, log_port=log_port, ident=ident)

    def logTest(self):
        report_test = VulnReport(report_id="cb0226d0-6689-4fdb-9c0b-ba8e4188e39c",
                                 task_id="c5258329-959d-480e-9392-e2ecabdfc592")
        # self.__getReport(report=report_test)
        report_test = self._updateReport(report_test)
        self._logReport(report=report_test)

    def dbTest(self):
        tasks = self.getTasks()
        task_id = tasks[0]
        # print(task_id)
        task = self._tasks[task_id]
        self.startTask(task)
        self._checkQueue()
        # self._updateReport(report_test)

    # start scanner to run in while true loop
    def start(self):
        self.scheduler.clear()
        self._initTasks()
        self._createSchedule()
        self._status = "started"
        # self.logTest()
        # self.dbTest()

        while self._status != "stopped":
            try:
                self._logger.sysLog(self.name + " starting")
                # print(self.name + " starting")
                while self._status != "stopped":
                    self.scheduler.run_pending()
                    time.sleep(1)
            except Exception as e:
                self._logger.sysLog(self.name + " except")
                # print(self.name + " except")
                continue

    # update target/task to configFile
    def _updateConfig(self, my_object):
        # cfg = self._controller.configRead(cfg_path=self.cfg_path)
        if type(my_object) == VulnTarget:
            self._db.insertTarget(target=my_object)
            # write new target to cfg file
            # target_id = my_object.getId()
            # cfg['targets'][target_id] = {"name": my_object.getName(),
            #                             "hosts": my_object.getHosts(),
            #                             "exclude_hosts": my_object.getExcludeHosts(),
            #                             "port_list_id": my_object.getPortListId()}
        elif type(my_object) == VulnTask:
            self._db.insertTask(task=my_object)
            # task_id = my_object.getId()
            # cfg['tasks'][task_id] = {"name": my_object.getName(),
            #                         "target_id": my_object.getTarget().getId(),
            #                         "scan_config_id": my_object.getScanConfigId(),
            #                         "schedule": {"frequency": my_object.getFrequency(),
            #                                      "interval": my_object.getInterval(),
            #                                      "start_time": my_object.getStartTime()
            #                                      }
            #                         }
        else:
            return
        # self._controller.configWrite(cfg_path=self.cfg_path, cfg=cfg)

    def _delFromConfig(self, my_object):
        # cfg = self._controller.configRead(cfg_path=self.cfg_path)
        object_id = my_object.getId()
        if type(my_object) == VulnTarget:
            self._db.deleteTarget(target=my_object)
            # cfg['targets'].pop(object_id)
        elif type(my_object) == VulnTask:
            self._db.deleteTask(task=my_object)
            # cfg['tasks'].pop(object_id)
        # self._controller.configWrite(cfg_path=self.cfg_path, cfg=cfg)

    def _updateReportinDB(self, report: VulnReport):
        result = self._db.selectReport(report=report)
        rows = result.fetchall()
        if len(rows) > 0:
            if report.getStatus() == "DELETE":
                self._db.deleteReport(report=report)
            else:
                if report.getStatus() == rows[0][2]:
                    self._logger.sysLog(self.name + " no db update needed")
                    # print(self.name, "no db update needed")
                else:
                    self._logger.sysLog(self.name + " updating report in db")
                    # print(self.name, "updating report in db")
                    self._db.insertReport(report=report)
        else:
            self._logger.sysLog(self.name + " insert report to db")
            # print(self.name, "insert report to db")
            self._db.insertReport(report=report)
        return

    # def _updateTarget(self, target: VulnTarget):
    #    self._db.updateTarget(target=target)

    def showSchedule(self):
        print("Schedule:")
        for job in self.scheduler.jobs:
            print(job)
        print("\n")

    def _initPortList(self):
        # gets port list from scanner
        portList = self._controller.getPortLists()
        self._port_list = portList

    def getPortLists(self):
        return sorted(self._port_list, key=lambda x: self._port_list[x].getAllPortCount())

    def getPortList(self, portlist_id):
        return self._port_list[portlist_id]

    def listPortList(self):
        print(self.name + " PortLists:")
        portlists = self.getPortLists()
        j = 1
        for i in portlists:
            print(str(j) + ". " + str(self._port_list[i]))
            j += 1
        print("\n")

    def _initScanConfigs(self):
        # gets port list from scanner
        scanConfigs = self._controller.getScanConfigs()
        self._scan_configs = scanConfigs

    def _initScanCreds(self):
        scanCreds = self._controller.getCredentials()
        self._scan_creds = scanCreds

    def getScanConfigs(self):
        return sorted(self._scan_configs, key=lambda x: self._scan_configs[x].getName())

    def getScanConfig(self, scanconfig_id):
        return self._scan_configs[scanconfig_id]

    def listScanConfig(self, ):
        print(self.name + " ScanConfigs:")
        configlist = self.getScanConfigs()
        j = 1
        for i in configlist:
            print(str(j) + ". " + str(self._scan_configs[i]))
            j += 1
        print("\n")

    def getScanCreds(self):
        return sorted(self._scan_creds, key=lambda x: self._scan_creds[x].getName())

    def getScanCred(self, scancred_id):
        return self._scan_creds[scancred_id]

    def listScanCreds(self, ):
        print(self.name + " ScanCreds:")
        credlist = self.getScanCreds()
        j = 1
        for i in credlist:
            print(str(j) + ". " + str(self._scan_creds[i]))
            j += 1
        print("\n")

    def _checkTargets(self):
        myadddict = {}
        myremovelist = []
        for i in self._targets:
            # self._db.insertTarget(target=self._targets[i])
            new_id = self._createTarget(self._targets[i])

            if new_id != i:
                tmp_target = copy.copy(self._targets[i])
                tmp_target.setId(target_id=new_id)
                myadddict[new_id] = tmp_target
                myremovelist.append(i)
        for j in myadddict:
            self._targets[j] = myadddict[j]
            self._updateConfig(my_object=myadddict[j])
        for k in myremovelist:
            tmp_target = self._targets.pop(k)
            self._delFromConfig(my_object=tmp_target)

    def _createTarget(self, target: VulnTarget, credentials: VulnScanCreds = None):
        # create new target via controller on scanner
        name = target.getName()
        hosts = target.getHosts()
        exclude_hosts = target.getExcludeHosts()
        port_list_id = target.getPortListId()
        target_id = self._controller.newTarget(name=name, hosts=hosts, exclude_hosts=exclude_hosts,
                                               port_list_id=port_list_id, credentials=credentials)
        if target_id == 0:
            return
        print(target_id)
        return target_id

    def addTarget(self, name, hosts, port_list_id, exclude_hosts=None, credentials: VulnScanCreds = None):
        # todo: check if target is in cfg file or available as object
        # add new target object as value with key target_id to targets dict
        new_target = VulnTarget(name=name, hosts=hosts, exclude_hosts=exclude_hosts, port_list_id=port_list_id)
        target_id = self._createTarget(new_target, credentials=credentials)
        if target_id is not None:
            new_target.setId(target_id=target_id)
            self._targets[target_id] = new_target
            self._updateConfig(new_target)
            return target_id
        else:
            print(self.name + " Target already exists!")

    def deleteTarget(self, target: VulnTarget):
        target_in_use = False
        task_using_target = ""
        for task in self._tasks:
            if self._tasks[task].target == target:
                target_in_use = True
                task_using_target = self.getTask(task_id=task)
        if not target_in_use:
            self._delFromConfig(my_object=target)
            # self._db.deleteTarget(target=target)
            self._targets.pop(target.getId())
            self._controller.deleteTarget(target=target)
            print(self.name + " Target:" + str(target) + "deleted!")
        else:
            print(self.name + " Target:" + str(target) + " NOT deleted, target is in use by task: " + str(
                task_using_target))

    def getTargets(self):
        return sorted(self._targets, key=lambda x: self._targets[x].getHosts())

    def getTarget(self, target_id):
        return self._targets[target_id]

    def listTargets(self):
        print(self.name + " Targets:")
        targets = self.getTargets()
        j = 1
        for i in targets:
            print(str(j) + ". " + str(self._targets[i]))
            j += 1
        print("\n")

    def _initTasks(self):
        dbQueue = self._db.initQueue()
        for i in dbQueue:
            # print(i)
            self._queue.put(VulnReport(report_id=i[0], task_id=i[1], status=i[2]))
        # todo: check if target and scan config from file is configured on scanner
        return

    def _maintenance(self):
        self._controller.checkConnection()
        for i in self._tasks:
            cur_task = self._tasks[i]
            rows2delete = self._db.maintenance(cur_task, self._keepReports)
            if len(rows2delete) > 0:
                for report in rows2delete:
                    report = VulnReport(report_id=report[0], task_id=report[1], status="Done")
                    if self._delReport(report=report):
                        report.setStatus(status="DELETE")
                    self._updateReport(report=report)

    # update report object with data from scanner
    def _updateReport(self, report: VulnReport):
        if type(report) == VulnReport:
            response = self._getReport(report)
            # pretty_print(response)
            if response.attrib['status'] == "404":
                # print(self.name + " Report not found on scanner")
                self._logger.sysLog(self.name + " Report not found on scanner")
                report.setStatus(status="DELETE")
            else:
                # if Logged = skip instructions
                if report.getStatus() != "Logged":
                    status = response.find('.//scan_run_status').text
                    report.setStatus(status=status)
                    # update Report after start
                    if status != "Requested" and status != "New":
                        start_time = response.find('.//scan_start').text
                        report.setStartTime(starttime=start_time)
                    # set end_time
                    if status == "Done":
                        end_time = response.find('.//scan_end').text
                        report.setEndTime(endtime=end_time)
                    if status == "Running":
                        progress = response.find('.//progress').text
                        report.setProgress(progress=progress)
            self._updateReportinDB(report=report)
            return report

    def _delReport(self, report: VulnReport):
        report_id = report.getId()
        return self._controller.delReport(report_id=report_id)

    def addTask(self, target: VulnTarget, scan_config, interval, frequency, start_time):
        # add new task object as value with key task_id to tasks dict
        new_task = (VulnTask(target=target, scan_config=scan_config, interval=interval,
                             frequency=frequency, start_time=start_time))
        new_task_id = self._createTask(new_task)
        new_task.setId(task_id=new_task_id)
        self._tasks[new_task_id] = new_task
        self._updateConfig(new_task)
        self._scheduleTask(new_task)

    def _createTask(self, task: VulnTask):
        name = task.getName()
        target = task.getTarget()
        scan_config = task.getScanConfigId()
        scanner_id = self._vulnscanner_id
        # check if task exists already
        task_id = self._controller.newTask(name=name, scan_config=scan_config, target=target, scanner_id=scanner_id)
        return task_id

    def _checkTasks(self):
        myadddict = {}
        myremovelist = []
        for i in self._tasks:
            result = self._controller.checkTaskId(task_id=i)
            if result == i:
                continue
            elif result is None:
                tmp_task = copy.copy(self._tasks[i])
                new_id = self._createTask(self._tasks[i])
                tmp_task.setId(task_id=new_id)
                myadddict[new_id] = tmp_task
                myremovelist.append(i)
        for j in myadddict:
            self._tasks[j] = myadddict[j]
            self._updateConfig(my_object=myadddict[j])
        for k in myremovelist:
            tmp_task = self._tasks.pop(k)
            self._delFromConfig(my_object=tmp_task)

    def _createSchedule(self):
        tasks = self.getTasks()
        for task in tasks:
            cur_task = self._tasks[task]
            self._scheduleTask(cur_task)
        self.scheduler.every(60).seconds.do(self._checkQueue)
        self.scheduler.every(10).minutes.do(self._maintenance)
        # schedule.every().minute.do(self._checkQueue)
        # self.scheduler.every(300).seconds.do(self.logTest)

    def _scheduleTask(self, task: VulnTask):
        interval = task.getInterval()
        freq = int(task.getFrequency())
        start = task.getStartTime()
        # print(start)
        # print(len(start))
        if len(start) == 4:
            start = "0" + start
        if freq == "" or freq is None:
            freq = 1
        if interval == "minute" or interval == "minutes":
            job = self.scheduler.every(freq).minutes.do(self.startTask, task)
        elif interval == "hour" or interval == "hours":
            if len(start) == 5:
                job = self.scheduler.every(freq).hours.at(start).do(self.startTask, task)
            else:
                job = self.scheduler.every(freq).hours.do(self.startTask, task)
        elif interval == "day" or interval == "days":
            job = self.scheduler.every(freq).days.at(start).do(self.startTask, task)
        elif interval == "monday":
            job = self.scheduler.every(freq).monday.at(start).do(self.startTask, task)
        elif interval == "tuesday":
            job = self.scheduler.every(freq).tuesday.at(start).do(self.startTask, task)
        elif interval == "wednesday":
            job = self.scheduler.every(freq).wednesday.at(start).do(self.startTask, task)
        elif interval == "thursday":
            job = self.scheduler.every(freq).thursday.at(start).do(self.startTask, task)
        elif interval == "friday":
            job = self.scheduler.every(freq).friday.at(start).do(self.startTask, task)
        elif interval == "saturday":
            job = self.scheduler.every(freq).saturday.at(start).do(self.startTask, task)
        elif interval == "sunday":
            job = self.scheduler.every(freq).sunday.at(start).do(self.startTask, task)
        task.setJob = job

    def startTask(self, task: VulnTask):
        task_id = task.getId()
        report_id = self._controller.startTask(task_id=task_id)
        if report_id != -1:
            report = VulnReport(report_id=report_id, task_id=task_id)
            report.setStatus(status="Running")
            self._logger.sysLog(self.name + " starting task with TaskId: " + task_id + " -> ReportId: " + report_id)
            # print(self.name + " starting task with TaskId: " + task_id + " -> ReportId: " + report_id)
            self._queue.put(report)

    def resumeTask(self, task: VulnTask):
        task_id = task.getId()
        report_id = self._controller.resumeTask(task_id=task_id)
        if report_id != -1:
            report = VulnReport(report_id=report_id, task_id=task_id)
            report.setStatus(status="Running")
            self._logger.sysLog(self.name + " resumed task with TaskId: " + task_id + " -> ReportId: " + report_id)
            # print(self.name + " starting task with TaskId: " + task_id + " -> ReportId: " + report_id)
            self._queue.put(report)

    def getTasks(self):
        return sorted(self._tasks)

    def listTasks(self):
        print(self.name + " Tasks:")
        tasks = self.getTasks()
        j = 1
        for i in tasks:
            print(str(j) + ". " + str(self._tasks[i]))
            j += 1
        print("\n")

    # get next report object from scanner and run instructions for status
    def _checkQueue(self):
        # print(self._queue.qsize())
        self._logger.sysLog(self.name + " checking...")
        # print(self.name + " checking...")
        if self._queue.empty():
            self._logger.sysLog(self.name + " Queue Empty")
            # print(self.name + " Queue Empty")
        else:
            # print(self._queue.qsize())
            report = self._queue.get()
            if type(report) == VulnReport:
                try:
                    report = self._updateReport(report=report)
                    status = report.getStatus()
                    if status == "Done":
                        self._logger.sysLog(self.name + " done report found - " + report.getId())
                        # print(self.name + " done report found")
                        report = self._logReport(report)
                        # report = self._logReportFileBeat(report)
                        self._queue.put(report)
                        return
                    elif status == "Interrupted" or status == "Stopped":
                        taskId = report.getTaskId()
                        # get Task Object from TaskDict
                        self.resumeTask(self._tasks[taskId])
                    elif status == "Running":
                        if self._isReportStuck(report=report):
                            self._delReport(report=report)
                            print("REPORT STUCK")
                            # del report
                            return
                        pass
                    elif status == "Requested":
                        pass
                    elif status == "Logged" or status == "DELETE":
                        # report send to Log -> destroy object
                        self._logger.sysLog(self.name + " deleting report " + report.getId())
                        # self._delReport(report=report)
                        # print(self.name + " deleting report" + report.getId())
                        del report
                        return
                    self._queue.put(report)
                except:
                    self._queue.put(report)
                self._logger.sysLog(
                    self.name + " Report not done, progess: " + report.getProgress() + "%, " + " putting back in queue ReportId: " + report.getId())

                """
                report = self._updateReport(report=report)
                status = report.getStatus()
                if status == "Done":
                    self._logger.sysLog(self.name + " done report found - " + report.getId())
                    # print(self.name + " done report found")
                    report = self._logReport(report)
                    # report = self._logReportFileBeat(report)
                    self._queue.put(report)
                    return
                elif status == "Interrupted" or status == "Stopped":
                    taskId = report.getTaskId()
                    # get Task Object from TaskDict
                    self.resumeTask(self._tasks[taskId])
                elif status == "Running":
                    if self._isReportStuck(report=report):
                        self._delReport(report=report)
                        print("REPORT STUCK")
                        # del report
                        return
                    pass
                elif status == "Requested":
                    pass
                elif status == "Logged" or status == "DELETE":
                    # report send to Log -> destroy object
                    self._logger.sysLog(self.name + " deleting report " + report.getId())
                    # self._delReport(report=report)
                    # print(self.name + " deleting report" + report.getId())
                    del report
                    return
                self._queue.put(report)
                self._logger.sysLog(self.name + " Report not done, progess: " + report.getProgress() + "%, " +  " putting back in queue ReportId: " + report.getId())
                # print(self.name + " report not done, putting back in queue " + report.getId())
                #self._queue.put(report)
                """

    def _isReportStuck(self, report: VulnReport):
        max_delta_time = 0
        start_time = report.getStartTime()
        cur_time = datetime.datetime.utcnow()
        if start_time != "":
            # print("START", start_time, "NOW: ", cur_time)
            task_id = report.getTaskId()
            task = self._tasks[task_id]
            freq = int(task.getFrequency())
            interval = task.getInterval()
            # print("freq",freq)
            # print("interval", interval)
            if interval == "minute" or interval == "minutes":
                max_delta_time = datetime.timedelta(minutes=freq)
            elif interval == "hour" or interval == "hours":
                max_delta_time = datetime.timedelta(hours=freq)
            elif interval == "day" or interval == "days":
                max_delta_time = datetime.timedelta(days=freq)
            elif interval == "monday" or interval == "tuesday" or interval == "wednesday" or interval == "thursday" or interval == "friday" or interval == "saturday" or interval == "sunday":
                max_delta_time = datetime.timedelta(days=7 * freq)
            delta = cur_time - datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
            max_delta_time = max_delta_time * 4
            # print("DELTA", delta)
            # print("MAX DELTA", max_delta_time)
            if delta > max_delta_time:
                return True
        return False

    def _getReport(self, report: VulnReport):
        report_id = report.getId()
        return self._controller.getReport(report_id=report_id)

    def _logReport(self, report: VulnReport):
        if type(report) == VulnReport:
            return self._logReportSysLog(report)

    def _logReportFileBeat(self, report: VulnReport):
        reportResponse = self._getReport(report=report)
        xmlstr = etree.tostring(reportResponse, encoding='utf8', method='xml')
        jsonreport = xmltodict.parse(xmlstr, dict_constructor=dict)
        f = open("/var/log/csoc-vscan/" + report.getId() + ".json", "w")
        f.write(json.dumps(jsonreport))
        f.close()
        report.setStatus("Logged")
        self._logger.sysLog(self.name + " report " + report.getId() + " logged!")
        return report

    # log issues and ports from report to logger and return report object
    def _logReportSysLog(self, report: VulnReport):
        self._logger.sysLog(self.name + " logging...")
        # print(self.name + " logging...")
        islogged_issues = True
        islogged_ports = True
        # todo: change priority for high severity?
        reportResponse = self._getReport(report=report)
        # pretty_print(reportResponse)
        # print(type(reportResponse))
        #print(reportResponse)
        issues = reportResponse.findall('.//results/result')
        ports = reportResponse.findall('.//ports/port')
        if len(issues) > 0:
            counter = 0
            for i in issues:
                # rename result to vulnerability
                i.tag = "vulnerability"
                c = etree.Element("id")
                c.text = report.getId() + "_issue" + str(counter)
                i.append(c)
                d = etree.Element("scan_time")
                d.text = report.getEndTime()
                i.append(d)
                # replace host tag with issue_host
                for port in i.iter('host'):
                    port.tag = 'issue_host'
                if i.find('.//hostname').text is None:
                    i.find('.//hostname').text = i.find('.//issue_host').text

                # DESCRIPTION
                if i.find('.//description').text is not None:
                    # print("DESC FOUND")
                    modifiedDescription = str(i.find('.//description').text)

                    # print("1:", modifiedDescription)
                    # modifiedDescription = modifiedDescription.strip()

                    modifiedDescription = re.sub(' "', ' ', modifiedDescription)
                    modifiedDescription = re.sub(" '", ' ', modifiedDescription)
                    modifiedDescription = re.sub('\', ', ' ', modifiedDescription)
                    modifiedDescription = re.sub(' +', ' ', modifiedDescription)
                    modifiedDescription = re.sub('\n+', ' - ', modifiedDescription)
                    # modifiedDescription = modifiedDescription[:250]

                    # 225 working
                    # 256 not working
                    # modifiedDescription = modifiedDescription.replace('\n\n\n\n', ' - ')
                    # modifiedDescription = modifiedDescription.replace('\n\n\n', ' - ')
                    # modifiedDescription = modifiedDescription.replace('\n\n', ' - ')
                    # modifiedDescription = modifiedDescription.replace('\n', ' - ')

                    # modifiedDescription.replace('\\n', ' - ')
                    # modifiedDescription.replace('\t', ' - ')
                    # modifiedDescription.replace('\r\n', ' - ')
                    # modifiedDescription = repr(modifiedDescription)
                    # print("2:", modifiedDescription)

                    i.find('.//description').text = modifiedDescription
                    # print("DESCRIPTION:", i.find('.//description').text)
                #
                # pretty_print(i)
                issue = xmltodict.parse(etree.tostring(i), dict_constructor=dict)
                # self.logger.log(priority=3, message=json.dumps(issue["result"]))
                cur_result = self._logger.csocLog(priority=3, message=json.dumps(issue))
                if islogged_issues != cur_result:
                    islogged_issues = False
                counter += 1
        if len(ports) > 0:
            counter = 0
            for i in ports:
                # id_text = report.getId() + "_port" + str(counter)
                # i.set("id", id_text)
                i.tag = 'port_result'
                c = etree.Element("id")
                c.text = report.getId() + "_port" + str(counter)
                i.append(c)
                d = etree.Element("scan_time")
                d.text = report.getEndTime()
                i.append(d)
                # replace host tag with port_host
                for port in i.iter('host'):
                    port.tag = 'port_host'
                # pretty_print(i)
                port = xmltodict.parse(etree.tostring(i), dict_constructor=dict)

                #############################################
                #############################################
                #############################################
                # log only issues
                #############################################

                # cur_result = self._logger.csocLog(priority=3, message=json.dumps(port["port_result"]))
                # self.logger.log(priority=3, message=json.dumps(port))
                counter += 1
                # if islogged_ports != cur_result:
                #    islogged_ports = False
                islogged_ports = True
        if islogged_issues and islogged_ports:
            report.setStatus("Logged")
            self._logger.sysLog(self.name + " report " + report.getId() + " logged!")
            # print(self.name + " report " + report.getId() + " logged!")
        else:
            self._logger.sysLog(self.name + " report " + report.getId() + " NOT logged!")
            # print(self.name + " report " + report.getId() + " NOT logged!")
        return report

    def setStatus(self, status):
        self._status = status

    def getStatus(self):
        return self._status

    def getTask(self, task_id):
        return self._tasks[task_id]

    def deleteTask(self, task):
        self._controller.deleteTask(task=task)
        self._delFromConfig(my_object=task)
        # self._db.deleteTask(task=task)
        task_to_remove = self._tasks.pop(task.getId())
        # print(task_to_remove)
        job = task.getJob()
        self.scheduler.cancel_job(job=job)
        print(self.name + " Task:" + str(task) + "deleted!")

    def addCred(self, credtype, login, password):
        self._controller.createCredentials(name=credtype + "_" + login, login=login, password=password)
        self._initScanCreds()
        print(self.name + " Credentials added!")

    def delCred(self, credential:VulnScanCreds):
        status = self._controller.deleteCredentials(credendial=credential)
        self._initScanCreds()
        return status

    def resetQueue(self):
        self._db.clearQueue()
        self._queue.queue.clear()

    def resetScanner(self):
        self._controller.resetScanner()
        print(self.name + "Restart Service to Reinit")
