class VulnPortList:

    def __init__(self, id, name, portcountall, portcounttcp, portcountudp):
        self._id = id
        self._name = name
        self._countall = portcountall
        self._counttcp = portcounttcp
        self._countudp = portcountudp

    def __repr__(self):
        return "All Ports: " + self._countall + "\t\t TCP Ports: " + self._counttcp + "\t\t UDP Ports: " + self._countudp + "\t\tName: " + self._name

    def getAllPortCount(self):
        return int(self._countall)

    def getName(self):
        return self._name

    def getId(self):
        return self._id
