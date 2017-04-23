import re

from bs4 import BeautifulSoup

from src.scoring.bestTrio import BestTrio


# TODO: finish functionality
class TopPerformerParser:
    def __init__(self, scoreboard, browserSession):
        self.__scoreboard = scoreboard
        self.__browserSession = browserSession
        self.__topPerformers = {
            "C": BestTrio(),
            "1B": BestTrio(),
            "2B": BestTrio(),
            "3B": BestTrio(),
            "SS": BestTrio(),
            "OF": BestTrio(),
            "CF": BestTrio(),
            "U": BestTrio(),
            "1SP": BestTrio(),
            "2SP": BestTrio(),
            "RP": BestTrio() }
        self.__worstPerformers = {
            "SP": BestTrio(reverse=True),
            "RP": BestTrio(reverse=True) }

    def parseTopPerformers(self):
        for position in self.topPerformers.keys():
            if self.topPerformers[position].first:
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

