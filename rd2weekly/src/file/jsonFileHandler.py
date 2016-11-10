import json

from src.scoring.trio import Trio


class JsonFileHandler(Trio):
    def __init__(self, filename):
        jsonData = JsonFileHandler.__parseJsonFromFile(filename)
        super(JsonFileHandler, self).__init__(first=filename, second=jsonData, third=jsonData)

    @staticmethod
    def __parseJsonFromFile(filename):
        with open(filename, "r+") as jsonFile:
            return json.load(jsonFile)

    @property
    def filename(self):
        return self.__first

    @property
    def originalJson(self):
        return self.__second

    @property
    def activeJson(self):
        return self.__third

    @activeJson.setter
    def activeJson(self, newJson):
        self.__third = newJson

    def writeChangesBack(self):
        if self.originalJson != self.activeJson:
            with open(self.filename, "w") as jsonFile:
                json.dump(self.activeJson, jsonFile)
