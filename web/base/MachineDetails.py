
class MachineDetails:
    """def __init__(self, id, name, ami=None, tags=None, creation_date=None):
        self.id = id
        self.name = name
        self.ami = ami
        self.tags = tags
        self.creation_date = creation_date"""

    def __init__(self, boto_instance):
        self.__instance = boto_instance

    @property
    def id(self):
        return self.__instance.id

    @property
    def name(self):
        return self.__instance.tags["Name"]

    @property
    def tags(self):
        return self.__instance.tags

    @property
    def creation_date(self):
        return self.__instance.launch_time

    @property
    def state(self):
        return self.__instance.state
