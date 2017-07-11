from typing import Union, Set

from src.scoring.bestTrio import BestTrio
from src.scoring.player import Player
from src.scoring.team import Team
from src.summary import markdownFormatter

PointScorer = Union[Player, Team]


TOP_THREE_TEAMS_HEADER = "Top Three Teams of the Week"
WORST_THREE_TEAMS_HEADER = "Not Top Three Teams of the Week"
TOP_THREE_OFFENSES_HEADER = "Offensive Powerhouses"
WORST_THREE_OFFENSES_HEADER = "Weaklings"
TOP_THREE_PITCHING_HEADER = "Pitching Factories"
WORST_THREE_PITCHING_HEADER = "Burnt-down Factories"

TOP_TWO_START_PITCHER_HEADER = "2 Start Saviors"
TOP_ONE_START_PITCHER_HEADER = "1 Start Gods"
WORST_STARTING_PITCHER_HEADER = "Had a Bad Day"
TOP_RELIEF_PITCHER_HEADER = "No Start Workhorses"
WORST_RELIEF_PITCHER_HEADER = "The Bullpen Disasters"


class TrioSummary:
    def __init__(self, category: str, trio: BestTrio):
        self.__category = category
        self.__trio = trio

    @property
    def trio(self) -> BestTrio:
        return self.__trio

    @property
    def category(self) -> str:
        return self.__category

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
            return [markdownFormatter.getBulletedScorerString(scorer, "*") for scorer in rankedScorers]
        else:
            return [markdownFormatter.getTiedScorerString(scorer, "*", rank) for scorer in rankedScorers]
