from VulnTarget import VulnTarget


class VulnTask:

    def __init__(self, target: VulnTarget, scan_config, interval: str, frequency: int, start_time, task_id=None):
        self.task_id = task_id
        self.name = target.getName() + "_" + target.getHosts()
        self.target = target
        self.scan_config = scan_config
        self.interval = interval
        self.frequency = frequency
        self.start_time = start_time
        self.status = 0
        self._job = ""

    def __repr__(self):
        return "Name: " + self.name + " Int: " + self.interval + " Freq: " + self.frequency

    def getId(self):
        return self.task_id

    def getStatus(self):
        return self.status

    def getName(self):
        return self.name

    def getTarget(self):
        return self.target

    def getScanConfigId(self):
        return self.scan_config

    def getFrequency(self):
        return self.frequency

    def getInterval(self):
        return self.interval

    def getStartTime(self):
        return self.start_time

    def setId(self, task_id):
        self.task_id = task_id

    def getJob(self):
        return self._job

    def setJob(self, job):
        self._job = job
