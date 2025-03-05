class VulnScanCreds:

    def __init__(self, id, name, login):
        self._id = id
        self._name = name
        self._login = login
        self._cred_type = name.split("_")[0]

    def __repr__(self):
        return "Name: " + self._name + "\t\t " + "\t\t Login: " + self._login

    def getName(self):
        return self._name

    def getLogin(self):
        return self._login

    def getId(self):
        return self._id

    def getCredType(self):
        return self._cred_type

    def setCredType(self, cred_type):
        self._cred_type = cred_type
