import re

from bs4 import BeautifulSoup

from src.scoring.topPerformers import TopPerformers
from src.scoring.worstPerformers import WorstPerformers


class TopPerformerParser:
    # TODO: finish functionality (scraping, updating player position info, etc.)
    # TODO: consider separating scraping and storing of data
    def __init__(self, scoreboard, browserSession):
        self.__scoreboard = scoreboard
        self.__browserSession = browserSession
        self.__topPerformers = TopPerformers()
        self.__worstPerformers = WorstPerformers()

    def parseTopPerformers(self):
        for position in self.topPerformers.positions():
            if self.topPerformers.topPerformers[position].first:
                # already processed
                continue
            else:
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
        self.__getSortedPerformancesForPosition(position)

    def __getSortedPerformancesForPosition(self, position):
        soup = BeautifulSoup(self.browserSession.getSortedPerformancesByPosition(position), "html.parser")
        playerRows = soup.find_all("tr", class_=re.compile(r"row\d+"))
        return playerRows
