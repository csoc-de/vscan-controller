import configparser
import sys
import multiprocessing
import threading
import time
import getpass
import subprocess
import select

from VulnScanner import VulnScanner
from VulnPortList import VulnPortList
from VulnScanConfig import VulnScanConfig
from VulnScanCreds import VulnScanCreds


# from pygtail import Pygtail


class MainMenu(object):
    _jobs = []

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('VulnScanner.conf')
        cfg_list = config.sections()
        vulnscanner = []
        for scanner in cfg_list:
            # cfg_file = config.get(scanner, 'cfg_file')
            db_file = config.get(scanner, 'db_file')
            keep_reports = config.get(scanner, 'keep_reports')
            scanner_id = config.get(scanner, 'scanner_id')
            user = config.get(scanner, 'user')
            password = config.get(scanner, 'password')
            scanner_host = config.get(scanner, 'scanner_host', fallback=None)
            scanner_port = config.get(scanner, 'scanner_port', fallback=None)
            log_host = config.get(scanner, 'log_host')
            log_port = config.get(scanner, 'log_port')

            # vulnscanner.append(VulnScanner(name=scanner, configFile=cfg_file, dbFile=db_file, keepReports=keep_reports, scanner_id=scanner_id))
            vulnscanner.append(
                VulnScanner(name=scanner, dbFile=db_file, scanner_host=scanner_host, scanner_port=scanner_port,
                            user=user, password=password, log_host=log_host, log_port=log_port,
                            keepReports=keep_reports, scanner_id=scanner_id))
        self._scannerList = vulnscanner
        self._options = [("List Scanner", self._optionListScanner), ("Start all Scanner", self.optionStartAll),
                         ("Select Scanner", self._optionSelectScanner),
                         ("Show runnning Scanner", self._optionShowRunning),
                         # ("Monitor Scanner-Logs (exit with Ctrl-C)", self._optionMonitor),
                         ("Exit", self._optionExit)]

    def show(self):
        time.sleep(0.5)
        while True:
            print("Available Options:")
            for i in range(0, len(self._options)):
                print(str(i + 1) + ": " + str(self._options[i][0]))
            print("\nSelect Option:")
            try:
                self._options[self._getInput() - 1][1]()
            except Exception as e:
                print("Input not valid!\n")
                print(e)
                self.show()

    def _optionListScanner(self):
        print("Available Scanner:")
        for i in range(0, len(self._scannerList)):
            if self._scannerList[i] is not None:
                print(str(i + 1) + ": " + str(self._scannerList[i]))
        print("\n")

    def optionStartAll(self):
        for scanner in self._scannerList:
            scannermenu = VulnScannerMenu(currentMenu=self, scanner=scanner)
            scannermenu.optionStart()

    def _optionSelectScanner(self):
        self._optionListScanner()
        print("Enter ScannerNumber:")
        vulnscanner = self._scannerList[int(self._getInput()) - 1]
        scannermenu = VulnScannerMenu(currentMenu=self, scanner=vulnscanner)
        scannermenu.show()
        # try:
        #    vulnscanner = self._scannerList[int(self._getInput()) - 1]
        #    scannermenu = VulnScannerMenu(currentMenu=self, scanner=vulnscanner)
        #    scannermenu.show()
        # except:
        #    print("input not valid!\n")
        #    self.show()

    def _optionShowRunning(self):
        if len(self._jobs) == 0:
            print("No Scanner running!")
        else:
            print("Currently running:")
            for i in range(0, len(self._jobs)):
                print(str(i + 1) + ": " + str(self._jobs[i][0]))
        print("\n")

    # def _optionMonitor(self):
    # f = subprocess.Popen(['tail', '-f', "log/vscan-controller.log"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # p = select.poll()
    # p.register(f.stdout)
    # try:
    #    while True:
    #        if p.poll(1):
    #            line = f.stdout.readline().strip()
    #            encoding = 'utf-8'
    #            print(str(line, encoding))
    #        time.sleep(1)
    # print("Log:")
    # try:
    #    while True:
    #        for line in Pygtail("log/vscan-controller.log"):
    #            sys.stdout.write(line)
    # except KeyboardInterrupt:
    #    pass

    def _optionExit(self):
        for scanner in self._scannerList:
            scannermenu = VulnScannerMenu(currentMenu=self, scanner=scanner)
            scannermenu.optionStop()
        sys.exit()

    def _getInput(self):
        myinput = input()
        return int(myinput)


class VulnScannerMenu(MainMenu):

    def __init__(self, currentMenu, scanner: VulnScanner):
        super().__init__()
        self.scanner = scanner
        self.prevMenu = currentMenu
        self._options = [("Start", self.optionStart), ("Stop", self.optionStop), ("Import", self.optionImport),
                         ("Show Schedule", self._optionShowSchedule),
                         ("List Targets", self._optionListTargets), ("Add Target", self._optionAddTarget),
                         ("Delete Target", self._optionDeleteTarget),
                         ("List Tasks", self._optionListTasks), ("Add Task", self._optionAddTask),
                         ("Delete Task", self._optionDeleteTask),
                         ("List PortLists", self._optionListPortList), ("List ScanConfigs", self._optionListScanConfig),
                         ("List Credentials", self._optionListScanCreds), ("Add Credentials", self._optionAddCred),
                         ("Delete Credential", self._optionDelCred),
                         ("Reset Queue", self._optionResetQueue), ("Reset Scanner", self._optionResetScanner),
                         ("Back", self._optionBack)]

    def optionStart(self):
        running = False
        for i in super()._jobs:
            if i[0] == self.scanner.name:
                running = True
        if running:
            print(self.scanner.name, "scanner already running")
        else:
            self.scanner.addlogger()
            t = threading.Thread(target=self._worker)
            super()._jobs.append((self.scanner.name, t))
            t.start()
            # multi processing
            # using threads instead for dynamic scheduling
            # p = multiprocessing.Process(target=self._worker)
            # super()._jobs.append((self.scanner.name, p))
            # p.start()

    def optionStop(self):
        for i in self._jobs:
            if i[0] == self.scanner.name:
                # p = i[1]
                # self.scanner.setStatus(status="stopped")
                # p.terminate()
                # p.join()
                t = i[1]
                self.scanner.setStatus(status="stopped")
                t.join()
                self._jobs.remove(i)
                print(self.scanner.name + " stopped\n")

    def optionImport(self):
        print("Enter file for import:")
        import_file = input()

        try:
            with open(import_file) as fp:
                for cnt, line in enumerate(fp):
                    line = line.strip()
                    optionlist = line.split(",")
                    print(optionlist)
                    tar_name = optionlist[0]
                    tar_host = optionlist[1]
                    task_port = optionlist[2]
                    task_inter = optionlist[3]
                    task_freq = optionlist[4]
                    task_start = optionlist[5]

                    scan_list = self.scanner.getScanConfigs()
                    default_scan_config_id = scan_list[0]
                    try:
                        for scan_config_id in scan_list:
                            cur_scan_config = self.scanner.getScanConfig(scan_config_id)
                            if cur_scan_config.getName() == "Full and fast ohne bf":
                                default_scan_config_id = scan_config_id
                                break
                    except Exception as e:
                        for scan_config_id in scan_list:
                            cur_scan_config = self.scanner.getScanConfig(scan_config_id)
                            if cur_scan_config.getName() == "Full and fast":
                                default_scan_config_id = scan_config_id
                                break
                    port_list = self.scanner.getPortLists()
                    default_port_config_id = port_list[0]
                    for port_config_id in port_list:
                        cur_port_config = self.scanner.getPortList(portlist_id=port_config_id)
                        if task_port == "all":
                            if cur_port_config.getName() == "All TCP and Nmap top 100 UDP":
                                default_port_config_id = port_config_id
                                break
                        elif task_port == "default":
                            if cur_port_config.getName() == "OpenVAS Default":
                                default_port_config = cur_port_config
                                break
                    print("add target\n")
                    print("name: ", tar_name)
                    print("host: ", tar_host)
                    print(type(default_port_config_id), "portlistid: ", default_port_config_id)
                    target_id = self.scanner.addTarget(name=tar_name, hosts=tar_host, exclude_hosts="",
                                                       port_list_id=default_port_config_id)
                    print(target_id)
                    target = self.scanner.getTarget(target_id=target_id)
                    self.scanner.addTask(target=target, scan_config=default_scan_config_id, interval=task_inter,
                                         frequency=task_freq, start_time=task_start)
        finally:
            fp.close()

        # for
        # self.scanner.addTarget(name=name, hosts=hosts, port_list_id=port_list_id, exclude_hosts=exclude_hosts)
        # self.scanner.addTask(target=target, scan_config=scan_config_id, interval=interval, frequency=frequency, start_time=start_time)

    def _optionShowSchedule(self):
        self.scanner.showSchedule()

    def _optionListTargets(self):
        self.scanner.listTargets()

    def _optionAddTarget(self):
        print("Enter Target Name:")
        name = input()
        print("Enter Hosts:")
        hosts = input()
        print("Enter Exclude Hosts (leave empty to skip):")
        exclude_hosts = input()

        portlists = self.scanner.getPortLists()
        self._optionListPortList()
        print("Enter Number of Port List for Target:")
        port_list_number = self._getInput()
        port_list_id = portlists[port_list_number - 1]
        port_list = self.scanner.getPortList(portlist_id=port_list_id)

        credlist = self.scanner.getScanCreds()
        self._optionListScanCreds()
        print("Enter Number of Credential for authenticated scans on Target (leave empty to skip):")
        cred_input = input()
        #cred_number = self._getInput()
        cred_obj = ""
        if cred_input != "":
            cred_number = int(cred_input)
            cred_id = credlist[cred_number - 1]
            cred_obj = self.scanner.getScanCred(scancred_id=cred_id)
        print("Add Target with:")
        print("Name: ", name, " Hosts: ", hosts, " Exclude Hosts: ", exclude_hosts, " Port List: ", port_list.getName())
        print("Yes / No?")
        confirm = input()
        if confirm == "Yes" or confirm == "yes" or confirm == "y" or confirm == "Y":
            if isinstance(cred_obj, VulnScanCreds):
                self.scanner.addTarget(name=name, hosts=hosts, port_list_id=port_list_id, exclude_hosts=exclude_hosts,
                                   credentials=cred_obj)
            else:
                self.scanner.addTarget(name=name, hosts=hosts, port_list_id=port_list_id, exclude_hosts=exclude_hosts)
            print("Target added!")
        else:
            print("Target NOT added!")

    def _optionDeleteTarget(self):

        self.scanner.listTargets()
        targets = self.scanner.getTargets()
        print("Enter Target Number to delete:")
        target_number = self._getInput()
        target_id = targets[target_number - 1]
        target = self.scanner.getTarget(target_id=target_id)
        # print(targetlist)
        # print(targetlist[target-1])
        print("Delete Target with:")
        print("Name: ", target.getName(), " Hosts: ", target.getHosts(), " Exclude Hosts: ", target.getExcludeHosts(),
              " Port List: ", target.getPortListId())
        print("Yes / No?")
        confirm = input()
        if confirm == "Yes" or confirm == "yes" or confirm == "y" or confirm == "Y":
            self.scanner.deleteTarget(target=target)
        else:
            print("Target NOT deleted!")

    def _optionListTasks(self):
        self.scanner.listTasks()

    def _optionAddTask(self):
        self.scanner.listTargets()
        targets = self.scanner.getTargets()
        print("Enter Number of Target for Task:")
        target_number = self._getInput()
        target_id = targets[target_number - 1]
        target = self.scanner.getTarget(target_id=target_id)
        scanconfigs = self.scanner.getScanConfigs()
        self._optionListScanConfig()
        print("Enter Number of Scanner Config for Task:")
        scan_config_number = self._getInput()
        scan_config_id = scanconfigs[scan_config_number - 1]
        scan_config = self.scanner.getScanConfig(scanconfig_id=scan_config_id)
        print("Enter Task Interval (minute, hour, day, monday, tuesday...):")
        interval = input()
        print("Enter Task Frequency (Number):")
        frequency = input()
        print("Enter Start Time of Task (e.g. 3:15 for Interval = days:")
        start_time = input()
        print("Add Task with:")
        print("Target: ", target.getName(), " Scan Config: ", scan_config.getName(), " Interval: ", interval,
              " Frequency: ", frequency, " Start Time: ", start_time)
        print("Yes / No?")
        confirm = input()
        if confirm == "Yes" or confirm == "yes" or confirm == "y" or confirm == "Y":
            self.scanner.addTask(target=target, scan_config=scan_config_id, interval=interval, frequency=frequency,
                                 start_time=start_time)
            print("Task added!")
        else:
            print("Target NOT added!")

    def _optionDeleteTask(self):
        self._optionListTasks()
        print("Enter Task Number to delete:")
        task_number = self._getInput()
        tasklist = self.scanner.getTasks()
        task_id = tasklist[task_number - 1]
        task = self.scanner.getTask(task_id=task_id)
        print("Delete Task with:")
        print("Task: ", task.getName(), " Target: ", task.getTarget(), " Scan Config: ", task.getScanConfigId(),
              " Interval: ", task.getInterval(),
              " Frequency: ", task.getFrequency(), " Start Time: ", task.getStartTime())
        print("Yes / No?")
        confirm = input()
        if confirm == "Yes" or confirm == "yes" or confirm == "y" or confirm == "Y":
            self.scanner.deleteTask(task=task)
            print("Task deleted!")
        else:
            print("Target NOT deleted!")

    def _optionListPortList(self):
        self.scanner.listPortList()

    def _optionListScanConfig(self):
        self.scanner.listScanConfig()

    def _optionAddCred(self):
        print("SMB or SSH Cred? Enter Number: \n 1. smb \n 2. ssh")
        cred_type_number = self._getInput()
        if cred_type_number == 1:
            cred_type = "smb"
        elif cred_type_number == 2:
            cred_type = "ssh"
        else:
            return
        print("Enter Login/Username:")
        login = input()
        print("Enter Password:")
        password = getpass.getpass()
        self.scanner.addCred(credtype=cred_type, login=login, password=password)

    def _optionDelCred(self):
        credlist = self.scanner.getScanCreds()
        self._optionListScanCreds()
        print("Enter Number of Credential to delete:")
        cred_number = self._getInput()
        cred_id = credlist[cred_number - 1]
        cred_obj = self.scanner.getScanCred(scancred_id=cred_id)
        print("Delete Credential:")
        print(cred_obj, " \n ")
        print("Yes / No?")
        confirm = input()
        if confirm == "Yes" or confirm == "yes" or confirm == "y" or confirm == "Y":
            if self.scanner.delCred(credential=cred_obj):
                print("Credential deleted!")
            else:
                print("Credential NOT deleted!")
        else:
            print("Credential NOT deleted!")

    def _optionListScanCreds(self):
        self.scanner.listScanCreds()

    def _optionResetScanner(self):
        self.scanner.resetScanner()
        self.optionStop()
        self.optionStart()

    def _optionResetQueue(self):
        self.scanner.resetQueue()
        self.optionStop()
        self.optionStart()

    def _optionBack(self):
        self.prevMenu.show()

    def _worker(self):
        # print(multiprocessing.current_process().name, "Starting")
        self.scanner.start()
        # print(multiprocessing.current_process().name, "Exiting")
