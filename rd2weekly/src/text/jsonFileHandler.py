import json

from src.scoring.trio import Trio


class JsonFileHandler(Trio):
    def __init__(self, filename):
        jsonData = JsonFileHandler.__parseJsonFromFile(filename)
        super(JsonFileHandler, self).__init__(first=filename, second=jsonData, third=jsonData)

    @staticmethod
    def __parseJsonFromFile(filename: str):
        return json.load(filename)

    @property
    def filename(self) -> str:
        return self._first

    @property
    def originalJson(self) -> dict:
        return self._second

    @property
    def activeJson(self) -> dict:
        return self._third

    @activeJson.setter
    def activeJson(self, newJson: dict) -> None:
        self._third = newJson

    def writeChangesBack(self) -> None:
        if self.originalJson != self.activeJson:
            with open(self.filename, "w") as jsonFile:
                json.dump(self.activeJson, jsonFile)
