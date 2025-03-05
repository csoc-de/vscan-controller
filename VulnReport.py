class VulnReport:

    def __init__(self, report_id, task_id, status=None):
        self.id = report_id
        if status is None:
            self.status = "New"
        else:
            self.status = status
        self.taskId = task_id
        self.starttime = ""
        self.endtime = ""
        self.logged = False
        self.progress = "0"

    def __repr__(self):
        return self.status + "ID: " + self.id

    def getId(self):
        return self.id

    def getTaskId(self):
        return self.taskId

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status

    def setProgress(self, progress):
        self.progress = progress

    def getProgress(self):
        return str(self.progress)

    def getStartTime(self):
        return self.starttime

    def setStartTime(self, starttime):
        self.starttime = starttime

    def getEndTime(self):
        return self.endtime

    def setEndTime(self, endtime):
        self.endtime = endtime

    def setLogged(self, status: bool):
        self.logged = status

    def getLogged(self):
        return self.logged
