class VulnTarget:

    def __init__(self, name: str, hosts: str, exclude_hosts: str, port_list_id: str, target_id=None):
        self.target_id = target_id
        self.name = name
        self.hosts = hosts
        self.exclude_hosts = exclude_hosts
        self.port_list_id = port_list_id
        if target_id is None:
            self.target_id = ""

    def __repr__(self):
        return "id: " + self.target_id + "\t\tName: " + self.name + "\t\t Hosts: " + self.hosts + "\t\t Exclude Hosts: " + self.exclude_hosts

    def getId(self):
        return self.target_id

    def setId(self, target_id):
        self.target_id = target_id

    def getHosts(self):
        return self.hosts

    def getName(self):
        return self.name

    def getExcludeHosts(self):
        return self.exclude_hosts

    def getPortListId(self):
        return self.port_list_id
