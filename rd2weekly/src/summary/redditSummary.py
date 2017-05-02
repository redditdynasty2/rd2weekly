# TODO: actually do something
class RedditSummary:
    def __init__(self, scoreboard, topPerformers, records):
        self.__scoreboard = scoreboard
        self.__topPerformers = topPerformers
        self.__records = records

    @staticmethod
    def generateSummary(scoreboard, topPerformers, records):
        summary = RedditSummary(scoreboard, topPerformers, records)
        print("Scoreboard: " + summary.scoreboard)
        print("Top Performers: " + summary.topPerformers)
        print("Records: " + summary.records)

    @property
    def scoreboard(self):
        return self.__scoreboard

    @property
    def topPerformers(self):
        return self.__topPerformers

    @property
    def records(self):
        return self.__records
