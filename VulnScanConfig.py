class VulnScanConfig:

    def __init__(self, id, name, comment, nvtcount):
        self._id = id
        self._name = name
        self._comment = comment
        self._nvtcount = nvtcount

    def __repr__(self):
        return "Name: " + self._name + "\t\t NVT Count: " + self._nvtcount + "\t\t Comment: " + self._comment

    def getName(self):
        return self._name

    def getNVTCount(self):
        return self._nvtcount

    def getId(self):
        return self._id
