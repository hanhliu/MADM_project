from abc import abstractmethod


class AbstractDatabaseManager:

    def __init__(self):
        pass

    @abstractmethod
    def createDatabase(self):
        pass

    @abstractmethod
    def addToDatabase(self, *args, **kwargs):
        pass

    @abstractmethod
    def removeFromDatabase(self, *args, **kwargs):
        pass

    @abstractmethod
    def getAllFromDatabase(self):
        pass

    @abstractmethod
    def getAllNameFromDatabase(self):
        pass