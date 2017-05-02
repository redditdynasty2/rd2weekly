# TODO: actually do something
class RedditSummary:
    def __init__(self, scoreboard, topPerformers, records):
        self.__scoreboard = scoreboard
        self.__topPerformers = topPerformers
        self.__records = records

    @staticmethod
    def generateSummary(scoreboard, topPerformers, records):
        summary = RedditSummary(scoreboard, topPerformers, records)
        print("Scoreboard: {0}".format(summary.scoreboard))
        print("Top Performers: {0}".format(summary.topPerformers))
        print("Records: {0}".format(summary.records))

    @property
    def scoreboard(self):
        return self.__scoreboard

    @property
    def topPerformers(self):
        return self.__topPerformers

    @property
    def records(self):
        return self.__records
