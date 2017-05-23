# TODO: actually do something
from src.scoring.scoreboard import Scoreboard
from src.scoring.topPerformers import TopPerformers
from src.scoring.worstPerformers import WorstPerformers
from src.text.jsonFileHandler import JsonFileHandler


class RedditSummary:
    def __init__(self, scoreboard, topPerformers, worstPerformers, records):
        self.__scoreboard = scoreboard
        self.__topPerformers = topPerformers
        self.__worstPerformers = worstPerformers
        self.__records = records

    @staticmethod
    def generateSummary(scoreboard: Scoreboard,
                        topPerformers: TopPerformers,
                        worstPerformers: WorstPerformers,
                        records: JsonFileHandler) -> None:
        summary = RedditSummary(scoreboard, topPerformers, worstPerformers, records)
        print(summary.topPerformers)

    @property
    def scoreboard(self) -> Scoreboard:
        return self.__scoreboard

    @property
    def topPerformers(self) -> TopPerformers:
        return self.__topPerformers

    @property
    def worstPerformers(self) -> WorstPerformers:
        return self.__worstPerformers

    @property
    def records(self) -> JsonFileHandler:
        return self.__records
