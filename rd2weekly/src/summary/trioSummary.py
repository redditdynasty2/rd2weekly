from itertools import chain
from typing import Union, List, Set

from src.scoring.bestTrio import BestTrio
from src.scoring.player import Player
from src.scoring.team import Team
from src.summary import markdownFormatter

PointScorer = Union[Player, Team]


class TrioSummary:
    def __init__(self, category: str, trio: BestTrio):
        self.__category = category
        self.__trio = trio

    @property
    def trio(self) -> BestTrio:
        return self.__trio

    @property
    def category(self) -> str:
        return self.category

    #TODO: pull info from record books and previous weeks (that'll be tricky)
    @staticmethod
    def getTrioString(category: str, trio: BestTrio) -> str:
        summary = TrioSummary(category, trio)
        return summary.__getTrioSummary()

    def __getTrioSummary(self):
        lines = [ markdownFormatter.getHeaderString(self.category) ]
        for rank, rankedScorers in enumerate([self.trio.first, self.trio.second, self.trio.third]):
            [lines.append(line) for line in TrioSummary.__getRankedScorerLines(rankedScorers, rank + 1)]
        return "\n\n".join(lines)

    @staticmethod
    def __getRankedScorerLines(rankedScorers: Set[PointScorer], rank: int):
        if len(rankedScorers) == 1:
            return [markdownFormatter.getSingleScorerString(scorer, "*") for scorer in rankedScorers]
        else:
            return [markdownFormatter.getTiedScorerString(scorer, "*", rank) for scorer in rankedScorers]
