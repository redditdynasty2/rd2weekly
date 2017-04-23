# TODO: actually do something
class RedditSummary:
    def __init__(self, scoreboard, topPerformers, records):
        self.__scoreboard = scoreboard
        self.__topPerformers = topPerformers
        self.__records = records

    def generateSummary(self):
        pass

    @property
    def scoreboard(self):
        return self.__scoreboard

    @property
    def topPerformers(self):
        return self.__topPerformers

    @property
    def records(self):
        return self.__records
