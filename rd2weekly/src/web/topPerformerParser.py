import re
from typing import List, Tuple

from bs4 import BeautifulSoup

from src.scoring.player import Player
from src.scoring.scoreboard import Scoreboard
from src.scoring.topPerformers import TopPerformers
from src.scoring.worstPerformers import WorstPerformers
from src.web.rd2BrowserSession import RD2BrowserSession
from src.web.scoreboardParser import ScoreboardParser


class TopPerformerParser:
    def __init__(self, scoreboard: Scoreboard, browserSession: RD2BrowserSession):
        self.__scoreboard = scoreboard
        self.__browserSession = browserSession
        self.__topPerformers = TopPerformers()
        self.__worstPerformers = WorstPerformers()

    @staticmethod
    def parseTopPerformers(scoreboard: Scoreboard, browserSession: RD2BrowserSession) -> "TopPerformerParser":
        parser = TopPerformerParser(scoreboard, browserSession)
        for position in parser.topPerformers.positions():
            if not parser.topPerformers.topPerformers[position].first:
                parser.__parseTopPerformersForPosition(position)
        return parser

    @property
    def scoreboard(self) -> Scoreboard:
        return self.__scoreboard

    @property
    def browserSession(self) -> RD2BrowserSession:
        return self.__browserSession

    @property
    def topPerformers(self) -> TopPerformers:
        return self.__topPerformers

    @property
    def worstPerformers(self) -> WorstPerformers:
        return self.__worstPerformers

    def __parseTopPerformersForPosition(self, position: str) -> None:
        if "P" in position:
            position = "SP:RP"
        playerRows = self.__getSortedPerformancesForPosition(position)
        for player in playerRows:
            self.__processNewPlayerInfo(player)

    def __getSortedPerformancesForPosition(self, position: str) -> List[Player]:
        soup = BeautifulSoup(self.browserSession.getSortedPerformancesByPosition(position), "html.parser")
        playerSoupsRows = soup.find_all("tr", class_=re.compile(r"row\d+"))
        return [TopPerformerParser.__parsePlayerRow(playerSoup, position) for playerSoup in playerSoupsRows]

    @staticmethod
    def __parsePlayerRow(playerSoup: BeautifulSoup, position: str) -> Player:
        cbsId, name = TopPerformerParser.__getNameAndId(playerSoup)
        points = TopPerformerParser.__parsePlayerPoints(playerSoup)
        positions = TopPerformerParser.__parsePosition(playerSoup, position)
        return Player(name, cbsId, positions, points, None)

    @staticmethod
    def __getNameAndId(playerSoup: BeautifulSoup) -> Tuple[int, str]:
        tag = playerSoup.find("a", class_="playerLink")
        name = tag.string.strip()
        cbsId = ScoreboardParser.getPlayerId(tag)
        return cbsId, name

    @staticmethod
    def __parsePlayerPoints(playerSoup: BeautifulSoup) -> float:
        pointString = playerSoup.find("td", class_="bold", string=re.compile(r"\d+\.\d+")).string.strip()
        try:
            return float(pointString)
        except ValueError:
            return 0

    @staticmethod
    def __parsePosition(playerSoup: BeautifulSoup, position: str) -> List[str]:
        if "P" in position:
            return TopPerformerParser.__parsePitcherPosition(playerSoup)
        else:
            return TopPerformerParser.__parsePositionPlayerPosition(playerSoup, position)

    @staticmethod
    def __parsePositionPlayerPosition(playerSoup: BeautifulSoup, position: str) -> List[str]:
        positionSoup = playerSoup.find("span", class_="playerPositionAndTeam")
        positionMatch = re.search(r"^\s*(\w+)\s+\|", positionSoup.string.strip())
        if positionMatch:
            return [position, positionMatch.group(1)]
        else:
            return [position]

    @staticmethod
    def __parsePitcherPosition(playerSoup: BeautifulSoup) -> List[str]:
        gameStartedIndex = 1
        gameStartedString = playerSoup.find_all("td", align="right")[gameStartedIndex].string.strip()
        try:
            if int(gameStartedString) == 0:
                return ["RP"]
            elif int(gameStartedString) == 1:
                return ["1SP"]
            else:
                return ["2SP"]
        except ValueError:
            return ["RP"]

    def __processNewPlayerInfo(self, player: Player) -> None:
        updatedPlayer = self.scoreboard.updatePlayer(player)
        self.topPerformers.addPlayer(updatedPlayer)
        self.worstPerformers.addPlayer(updatedPlayer)
