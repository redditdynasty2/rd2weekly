from typing import List, Dict

from src.scoring.bestTrio import BestTrio
from src.scoring.topPerformers import TopPerformers
from src.summary import markdownFormatter


class AllStarSummary:
    def __init__(self, topPerformers: TopPerformers, positions: List[str]):
        self.__title = "All-Stars"
        self.__allStars = topPerformers.topPerformers
        self.__positions = positions

    @property
    def title(self) -> str:
        return self.__title

    @property
    def allStars(self) -> Dict[str, BestTrio]:
        return self.__allStars

    @property
    def positions(self) -> List[str]:
        return self.__positions

    #TODO: lots of logic needed here; need to make sure we're not duplicating performances
    #TODO: incorporate records and previous weeks here
    #TODO: write out if player was not active
    @staticmethod
    def getAllStarString(topPerformers: TopPerformers, positions: List[str]) -> str:
        summary = AllStarSummary(topPerformers, positions)
        return summary.__getAllStarSummary()

    def __getAllStarSummary(self) -> str:
        return "\n\n".join(self.__getAllStarSummaryLines(self.positions))

    def __getAllStarSummaryLines(self, positions: List[str]) -> List[str]:
        lines = []
        lines.append(markdownFormatter.getHeaderString("All-Stars"))
        for position in positions:
            scorer = next(iter(self.allStars[position].first))
            lines.append(markdownFormatter.getSingleScorerString(scorer, "\{0})".format(position)))
        return lines
