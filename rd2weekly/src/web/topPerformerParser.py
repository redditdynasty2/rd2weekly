import re

from bs4 import BeautifulSoup

from src.scoring.player import Player
from src.scoring.topPerformers import TopPerformers
from src.scoring.worstPerformers import WorstPerformers
from src.web.scoreboardParser import ScoreboardParser


class TopPerformerParser:
    def __init__(self, scoreboard, browserSession):
        self.__scoreboard = scoreboard
        self.__browserSession = browserSession
        self.__topPerformers = TopPerformers()
        self.__worstPerformers = WorstPerformers()

    def parseTopPerformers(self):
        for position in self.topPerformers.positions():
            if not self.topPerformers.topPerformers[position].first:
                self.__parseTopPerformersForPosition(position)

    @property
    def scoreboard(self):
        return self.__scoreboard

    @property
    def browserSession(self):
        return self.__browserSession

    @property
    def topPerformers(self):
        return self.__topPerformers

    @property
    def worstPerformers(self):
        return self.__worstPerformers

    def __parseTopPerformersForPosition(self, position):
        if "P" in position:
            position = "SP:RP"
        playerRows = self.__getSortedPerformancesForPosition(position)
        for player in playerRows:
            self.__processNewPlayerInfo(player)

    def __getSortedPerformancesForPosition(self, position):
        soup = BeautifulSoup(self.browserSession.getSortedPerformancesByPosition(position), "html.parser")
        playerSoupsRows = soup.find_all("tr", class_=re.compile(r"row\d+"))
        return [TopPerformerParser.__parsePlayerRow(playerSoup, position) for playerSoup in playerSoupsRows]

    @staticmethod
    def __parsePlayerRow(playerSoup, position):
        name = TopPerformerParser.__parsePlayerName(playerSoup)
        cbsId = ScoreboardParser.getPlayerId(playerSoup)
        points = TopPerformerParser.__parsePlayerPoints(playerSoup)
        positions = TopPerformerParser.__parsePosition(playerSoup, position)
        return Player(name, cbsId, points, positions, [])

    @staticmethod
    def __parsePlayerName(playerSoup):
        return playerSoup.find("a", class_="playerLink").string.strip()

    @staticmethod
    def __parsePlayerPoints(playerSoup):
        pointString = playerSoup.find("td", class_="bold", string=re.compile(r"\d+\.\d+")).string.strip()
        try:
            return float(pointString)
        except ValueError:
            return 0

    @staticmethod
    def __parsePosition(playerSoup, position):
        if "P" in position:
            return TopPerformerParser.__parsePitcherPosition(playerSoup)
        else:
            return TopPerformerParser.__parsePositionPlayerPosition(playerSoup, position)

    @staticmethod
    def __parsePositionPlayerPosition(playerSoup, position):
        positionSoup = playerSoup.find("span", class_="playerPositionAndTeam")
        positionMatch = re.search(r"^\s*(\w+)\s+\|", positionSoup.string.strip())
        if positionMatch:
            return [position, positionMatch.group(1)]
        else:
            return position

    @staticmethod
    def __parsePitcherPosition(playerSoup):
        gameStartedIndex = 1
        gameStartedString = playerSoup.find_all("td", align="right")[gameStartedIndex].string.strip()
        try:
            if int(gameStartedString) == 0:
                return "RP"
            elif int(gameStartedString) == 1:
                return "1SP"
            else:
                return "2SP"
        except ValueError:
            return "RP"

    def __processNewPlayerInfo(self, player):
        self.topPerformers.addPlayer(player)
        self.worstPerformers.addPlayer(player)
        self.scoreboard.updatePlayer(player)
