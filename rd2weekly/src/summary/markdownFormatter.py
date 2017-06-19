from typing import Union

from src.scoring.player import Player
from src.scoring.team import Team

PointScorer = Union[Player, Team]


def getHeaderString(category):
    return " * **{0}**".format(category)

def getSingleScorerString(scorer: PointScorer, bulletFormat: str) -> str:
    if type(scorer) is Player:
        return "  {0} {1}, {2}, {3}".format(bulletFormat, scorer.name, scorer.team, scorer.points)
    else:
        return "  {0} {1}, {2}".format(bulletFormat, scorer.name, scorer.points)

def getTiedScorerString(scorer: PointScorer, bulletFormat: str, rank: int) -> str:
    base = getSingleScorerString(scorer, bulletFormat)
    if rank == 1:
        return "{0} (tied for 1st)".format(base)
    elif rank == 2:
        return "{0} (tied for 2nd)".format(base)
    elif rank == 3:
        return "{0} (tied for 3rd)".format(base)
    else:
        raise ValueError("Unhandled rank {0}".format(rank))

#TODO: get player team name involved
def getPlayerScoringString(scorer: Player, bulletFormat: str) -> str:
    base = getSingleScorerString(scorer, bulletFormat)
    if not scorer.active:
        base = "{0} (from the bench)".format(base)
    return base
