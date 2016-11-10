from src.file.jsonFileHandler import JsonFileHandler
from src.scoring.bestPlayerPerformances import BestPlayerPerformances
from src.scoring.scoreboard import Scoreboard
from src.web.rd2browser import RD2BrowserSession
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
        self.__scoreboard = Scoreboard(self.__leagueJson.originalJson["league_name"], week)
        self.__topPerformers = BestPlayerPerformances()
        self.__browserSession = RD2BrowserSession(week, self.__leagueJson.originalJson["league_url"], credentials)

    def parseScores(self):
        ScoreboardParser.parseScoreboard(self.__scoreboard, self.__browserSession)
        TopPerformerParser.parseTopPerformers()

    def generateSummary(self):
        self.__leagueJson.writeChangesBack()
        self.__recordJson.writeChangesBack()
