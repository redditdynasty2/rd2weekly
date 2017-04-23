from src.file.jsonFileHandler import JsonFileHandler
from src.scoring.scoreboard import Scoreboard
from src.summary.redditSummary import RedditSummary
from src.web.rd2BrowserSession import RD2BrowserSession
from src.web.scoreboardParser import ScoreboardParser
from src.web.topPerformerParser import TopPerformerParser

__author__ = "Simon Swanson"
__copyright__ = "Copyright 2016, Simon Swanson"
__license__ = "MIT"
__version__ = "pre-alpha"
__maintainer__ = "Simon Swanson"
__email__ = "nomiswanson@gmail.com"
__status__ = "Pre-alpha"

class RD2Week:
    def __init__(self, week, leagueFile, recordFile, credentials):
        self.__leagueJson = JsonFileHandler(leagueFile)
        self.__recordJson = JsonFileHandler(recordFile)
        self.__scoreboard = Scoreboard()
        self.__topPerformers = TopPerformerParser()
        self.__browserSession = RD2BrowserSession(week, self.__leagueJson.originalJson["league_url"], credentials)

    @property
    def leagueJson(self):
        return self.__leagueJson

    @property
    def recordJson(self):
        return self.__recordJson

    @property
    def scoreboard(self):
        return self.__scoreboard

    @property
    def topPerformers(self):
        return self.__topPerformers

    @property
    def browserSession(self):
        return self.__browserSession

    def parseScores(self):
        ScoreboardParser.parseScoreboard(self.scoreboard, self.browserSession)
        TopPerformerParser.parseTopPerformers(self.scoreboard, self.browserSession)

    def generateSummary(self):
        self.leagueJson.writeChangesBack()
        self.recordJson.writeChangesBack()
        RedditSummary(self.scoreboard, self.topPerformers, self.recordJson).generateSummary()

    def __generateRedditSummary(self):
        redditSummary = RedditSummary(self.scoreboard, self.topPerformers, self.recordJson)
        return redditSummary

    def close(self):
        self.browserSession.driver.close()
