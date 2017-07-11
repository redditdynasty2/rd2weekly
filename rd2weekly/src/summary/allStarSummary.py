from typing import List

from src.scoring.topPerformers import TopPerformers
from src.summary import markdownFormatter


class AllStarSummary:
    def __init__(self, topPerformers: TopPerformers):
        self.__title = "All-Stars"
        self.__allStars = topPerformers

    @property
    def title(self) -> str:
        return self.__title

    @property
    def allStars(self) -> TopPerformers:
        return self.__allStars

    @property
    def positions(self) -> List[str]:
        return TopPerformers.getAllStarPositions()

    #TODO: lots of logic needed here; need to make sure we're not duplicating performances
    #TODO: incorporate records and previous weeks here
    #TODO: write out if player was not active
    @staticmethod
    def getAllStarString(topPerformers: TopPerformers) -> str:
        summary = AllStarSummary(topPerformers)
        return summary.__getAllStarSummary()

    def __getAllStarSummary(self) -> str:
        return "\n\n".join(self.__getAllStarSummaryLines(self.positions))

    def __getAllStarSummaryLines(self, positions: List[str]) -> List[str]:
        lines = []
        lines.append(markdownFormatter.getHeaderString("All-Stars"))
        for position in positions:
            scorer = next(iter(self.allStars.getPerformersForPosition(position).first))
            lines.append(markdownFormatter.getBulletedScorerString(scorer, "\{0})".format(position)))
        return lines
