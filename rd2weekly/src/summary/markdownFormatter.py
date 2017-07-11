from typing import Union, Set

from src.scoring.matchup import Matchup
from src.scoring.player import Player
from src.scoring.team import Team

PointScorer = Union[Player, Team]


def getHeaderString(category):
    return " * **{0}**".format(category)

def getBulletedScorerString(scorer: PointScorer, bulletFormat: str) -> str:
    scorerString = getPlayerPoints(scorer) if type(scorer) is Player else getTeamPoints(scorer)
    return "  {0} {1}".format(bulletFormat, scorerString)

def getPlayerPoints(scorer):
    suffix = ""
    if not scorer.active:
        suffix = " (from the bench)"
    return "{0}, {1}, {2} points{3}".format(scorer.name, scorer.team, pointsString(scorer.points), suffix)

def pointsString(points: float) -> str:
    if points * 10 % 10 == 0:
        return str(int(points))
    else:
        return str(points)

def getTeamPoints(scorer: Team) -> str:
    return "{0}, {1} points".format(scorer.name, pointsString(scorer.points))

def getTiedScorerString(scorer: PointScorer, bulletFormat: str, rank: int) -> str:
    base = getBulletedScorerString(scorer, bulletFormat)
    if rank == 1:
        return "{0} (tied for 1st)".format(base)
    elif rank == 2:
        return "{0} (tied for 2nd)".format(base)
    elif rank == 3:
        return "{0} (tied for 3rd)".format(base)
    else:
        raise ValueError("Unhandled rank {0}".format(rank))

def getMatchupString(matchups: Set[Matchup], category: str, isWin: bool) -> str:
    if len(matchups) == 1:
        matchupString = getSingleMatchupString(next(iter(matchups)), isWin)
    else:
        matchupString = " and ".join([getSingleMatchupString(matchup, isWin) for matchup in matchups])
    return " * **{0}**: {1}".format(category, matchupString)

def getSingleMatchupString(matchup: Matchup, isWin: bool) -> str:
    midString = ", tied with " if matchup.pointDifference() == 0 else " over " if isWin else ", to "
    matchup.team1.pointMode = matchup.team2.pointMode = "total"
    if isWin:
        matchupString = "{0}{1}{2}".format(getTeamPoints(matchup.team1), midString, getTeamPoints(matchup.team2))
    else:
        matchupString = "{0}{1}{2}".format(getTeamPoints(matchup.team2), midString, getTeamPoints(matchup.team1))
    matchup.team1.pointMode = matchup.team2.pointMode = None
    return matchupString
