import json

from gvm.xml import pretty_print

from VulnConnector import VulnConnector
from VulnPortList import VulnPortList
from VulnScanConfig import VulnScanConfig
from VulnScanCreds import VulnScanCreds
from VulnTarget import VulnTarget
from VulnTask import VulnTask
from VulnReport import VulnReport
from gvm.protocols.gmp.requests.v225 import CredentialType
from gvm.protocols.gmp.requests.v225 import AliveTest


def connect(scanner_host=None, scanner_port=None, socket_path=None):
    return VulnConnector(scanner_host=scanner_host, scanner_port=scanner_port, socket_path=socket_path).gmp


def safe_connect(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(str(e))
            return e

    return func_wrapper


class VulnController:

    @safe_connect
    def __init__(self, username, password, scanner_host=None, scanner_port=None, socket_path=None):
        self._scanner_host = scanner_host
        self._scanner_port = scanner_port
        self._socket_path = socket_path
        self._username = username
        self._password = password
        self._gmp = connect(scanner_host=scanner_host, scanner_port=scanner_port, socket_path=socket_path)
        resp = self._gmp.authenticate(username=username, password=password)

    @safe_connect
    def disconnect(self):
        self._gmp.disconnect()

    @classmethod
    def configRead(cls, cfg_path):
        with open(cfg_path, "r") as json_config_file:
            return json.load(json_config_file)

    @classmethod
    def configWrite(cls, cfg_path, cfg):
        with open(cfg_path, "w") as json_config_file:
            json.dump(cfg, json_config_file, indent=4)
        return

    @classmethod
    def dataRead(cls, data_path):
        with open(data_path, "r") as json_config_file:
            return json.load(json_config_file)

    @classmethod
    def dataWrite(cls, data_path, data):
        with open(data_path, "w") as json_config_file:
            json.dump(data, json_config_file, indent=4)
        return

    @safe_connect
    def newTarget(self, name, hosts, exclude_hosts, port_list_id, credentials: VulnScanCreds = None):
        alivetest = AliveTest.ICMP_TCP_ACK_SERVICE_AND_ARP_PING
        if credentials is not None:
            if credentials.getCredType() is None:
                credentials.setCredType = credentials.getName().split("_")[0]
            if credentials.getCredType() == "smb":
                respond = self._gmp.create_target(name=name, hosts=[hosts], exclude_hosts=[exclude_hosts],
                                                  smb_credential_id=credentials.getId(), alive_test=alivetest,
                                                  port_list_id=port_list_id, reverse_lookup_unify="true")
            elif credentials.getCredType() == "ssh":
                respond = self._gmp.create_target(name=name, hosts=[hosts], exclude_hosts=[exclude_hosts],
                                                  ssh_credential_id=credentials.getId(), alive_test=alivetest,
                                                  port_list_id=port_list_id, reverse_lookup_unify="true")
        else:
            respond = self._gmp.create_target(name=name, hosts=[hosts], exclude_hosts=[exclude_hosts],
                                              alive_test=alivetest,
                                              port_list_id=port_list_id, reverse_lookup_unify="true")

        #pretty_print(respond)
        if respond.get('status_text') == "Target exists already":
            if hosts.find(",") != -1:
                hosts = "~" + hosts
                hosts = hosts.replace(",", " AND ~")
            else:
                hosts = "hosts=" + hosts
            response = self._gmp.get_targets(filter_string=hosts + " port_list=" + port_list_id)
            target = response.find(".//target")
            return target.attrib['id']
        else:
            return respond.attrib['id']

    @safe_connect
    def deleteTarget(self, target: VulnTarget):
        target_id = target.getId()
        response = self._gmp.delete_target(target_id=target_id)
        if response.attrib['status'] == "404":
            print(response.attrib['status_text'], "- from Target:", target.getName())
            return
        print(target, " deleted!")
        return

    @safe_connect
    def newTask(self, name, scan_config, target: VulnTarget, scanner_id=None):
        # default openvas scanner
        # scanner_id = "08b69003-5fc2-4037-a479-93b440211c73"
        # openvas scanner on gvm11
        # scanner_id = "44582509-0357-4676-a08b-08029a2fba13"
        # todo: catch target not available
        target_id = target.getId()
        response = self._gmp.create_task(name=name, config_id=scan_config, target_id=target_id, scanner_id=scanner_id,
                                         alterable="true")
        # pretty_print(response)
        if response.attrib['status'] == "404":
            print(response.attrib['status_text'], "- from Task:", name)
            return
        # todo: check create response
        return response.attrib['id']

    @safe_connect
    def deleteTask(self, task: VulnTask):
        task_id = task.getId()
        response = self._gmp.delete_task(task_id=task_id)
        # pretty_print(response)
        if response.attrib['status'] == "404":
            print(response.attrib['status_text'], "- from Task:", task.getName())
            return
        print(task, " deleted!")
        return

    @safe_connect
    def startTask(self, task_id):
        task_response = self._gmp.start_task(task_id=task_id)
        # pretty_print(task_response)
        if task_response.attrib['status'] == "404":
            print("task not found on scanner")
        else:
            status_text = task_response.attrib['status_text']
            if status_text == "Task is active already":
                print(status_text)
                return -1
                # todo
                # return report_id of running task
                # pretty_print(self._gmp.get_reports(filter="task_id="+task_id+", "))
                # ZUR NOT: TASK ANHALTEN UND NEU STARTEN
                # todo
            elif status_text == "Service temporarily down" or status_text == "Failed to find task":
                print(status_text)
                return -1
            else:
                report = task_response.find(".//report_id")
                report_id = report.text
                return report_id

    @safe_connect
    def getReport(self, report_id):
        # old get_report
        # response = self._gmp.get_report(report_id=report_id, details=1)

        # new get_report
        response = self._gmp.get_report(report_id=report_id, details=1, ignore_pagination="1",
                                        filter_string="apply_overrides=0 levels=hml min_qod=70")
        # response = self._gmp.get_reports(report_id, apply_overrides=0, levels="hml", rows=100, min_qod=70)
        return response

    @safe_connect
    def delReport(self, report_id):
        response = self._gmp.delete_report(report_id=report_id)
        if response.attrib['status'] == "404":
            return False
        # pretty_print(response)
        if response.attrib['status'] == "200" or response.attrib['status'] == '201':
            return True

    @safe_connect
    def checkConnection(self):
        self._gmp = connect(scanner_host=self._scanner_host, scanner_port=self._scanner_port, socket_path=self._socket_path)
        self._gmp.authenticate(username=self._username, password=self._password)

    @safe_connect
    def checkTaskId(self, task_id):
        response = self._gmp.get_task(task_id=task_id)
        if response.attrib['status'] == "404":
            return None
        else:
            # return id if found
            task = response.find(".//task")
            return task.attrib['id']

    @safe_connect
    def getPortLists(self):
        # todo: sync with db
        PortList = {}
        response = self._gmp.get_port_lists()
        portlists = response.findall('.//port_list')
        for portlist in portlists:
            listid = portlist.attrib['id']
            name = portlist.find('name').text
            portcountall = portlist.find('port_count/all').text
            portcounttcp = portlist.find('port_count/tcp').text
            portcountudp = portlist.find('port_count/udp').text
            portlistobj = VulnPortList(id=id, name=name, portcountall=portcountall, portcounttcp=portcounttcp,
                                       portcountudp=portcountudp)
            PortList[listid] = portlistobj
        return PortList

    @safe_connect
    def getScanConfigs(self):
        # todo: sync with db
        Configs = {}
        response = self._gmp.get_scan_configs()
        configlist = response.findall('.//config')
        for config in configlist:
            config_id = config.attrib['id']
            config_name = config.find('name').text
            config_comment = config.find('comment').text
            config_nvtcount = config.find('nvt_count').text
            config_obj = VulnScanConfig(id=config_id, name=config_name, comment=config_comment,
                                        nvtcount=config_nvtcount)
            Configs[config_id] = config_obj
        return Configs

    @safe_connect
    def resetScanner(self):
        response = self._gmp.get_tasks()
        tasklist = response.findall('.//task')
        for task in tasklist:
            task_id = task.attrib['id']
            self._gmp.delete_task(task_id=task_id)
        response = self._gmp.get_targets()
        targetlist = response.findall('.//target')
        for target in targetlist:
            target_id = target.attrib['id']
            self._gmp.delete_target(target_id=target_id)

    # todo: create new scan configs

    # todo: cred handling for ssh + smb/wmi
    # todo: handle configs with cred

    # response = self._gmp.get_nvt_families()
    # family = response.findall('.//family')
    # for i in family:
    #    name = i.find("name").text
    #    nvtcount = i.find("max_nvt_count").text
    #    print(name, nvtcount)

    @safe_connect
    def resumeTask(self, task_id):
        task_response = self._gmp.resume_task(task_id=task_id)
        if task_response.attrib['status'] == "404":
            print("task not found on scanner")
        else:
            status_text = task_response.attrib['status_text']
            if status_text == "Task is active already":
                print(status_text)
            elif status_text == "Service temporarily down" or status_text == "Failed to find task":
                print(status_text)
                return -1
            else:
                report = task_response.find(".//report_id")
                report_id = report.text
                return report_id

    @safe_connect
    def createCredentials(self, name, login, password):
        cred_type = CredentialType.USERNAME_PASSWORD
        response = self._gmp.create_credential(login=login, password=password, name=name, credential_type=cred_type)
        # print(response)

    def deleteCredentials(self, credendial:VulnScanCreds):
        cred_id = credendial.getId()
        response = self._gmp.delete_credential(credential_id=cred_id)
        if response.attrib['status'] == "200" or response.attrib['status'] == '201':
            return True
        else:
            return False

    @safe_connect
    def getCredentials(self):
        credentials = {}
        response = self._gmp.get_credentials()
        credslist = response.findall('.//credential')
        for cred in credslist:
            cred_id = cred.attrib['id']
            cred_name = cred.find('name').text
            cred_login = cred.find('login').text
            cred_obj = VulnScanCreds(id=cred_id, name=cred_name, login=cred_login)
            credentials[cred_id] = cred_obj
        return credentials
