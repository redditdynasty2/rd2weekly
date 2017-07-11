from typing import Set

from src.scoring.matchup import Matchup
from src.summary import markdownFormatter

CLOSEST_MATCHUP = "Closest Matchup"
BIGGEST_BLOWOUT = "Blowout of the Week"
STRONGEST_ONE_LOSS = "Strongest Loss"
STRONGEST_TWO_LOSSES = "Strongest 0-2"
WEAKEST_ONE_WIN = "Weakest Win"
WEAKEST_TWO_WINS = "Weakest 2-0"


class MatchupSummary:
    def __init__(self, matchups: Set[Matchup]):
        self.__matchups = matchups

    @property
    def matchups(self) -> Set[Matchup]:
        return self.__matchups

    #TODO: need to get the record book working here, as well
    def getMatchupString(self, category: str) -> str:
        isWin = True
        if category in [ CLOSEST_MATCHUP, BIGGEST_BLOWOUT ]:
            matchups = self.__getMostExtremeMatchup(category == BIGGEST_BLOWOUT)
        elif category in [ STRONGEST_ONE_LOSS, STRONGEST_TWO_LOSSES, WEAKEST_ONE_WIN, WEAKEST_TWO_WINS ]:
            isWin = category not in [ STRONGEST_ONE_LOSS, STRONGEST_TWO_LOSSES ]
            numResults = 1 if category in [ STRONGEST_ONE_LOSS, WEAKEST_ONE_WIN ] else 2
            matchups = self.__getMostExtremePoints(self.__getTeamsWithNWinsOrLosses(numResults, isWin), not isWin, isWin)
        else:
            raise ValueError("Unknown categoy " + category)
        return markdownFormatter.getMatchupString(matchups, category, isWin)

    def __getMostExtremeMatchup(self, descending: bool) -> Set[Matchup]:
        sortedMatchups = sorted(self.matchups, key=lambda matchup: matchup.pointDifference(), reverse=descending)
        extremeMatchups = set()
        for matchup in sortedMatchups:
            if matchup.pointDifference() == sortedMatchups[0].pointDifference():
                extremeMatchups.add(matchup)
        return extremeMatchups

    def __getTeamsWithNWinsOrLosses(self, requiredWinsOrLosses: int, isWin: bool) -> Set[Matchup]:
        matchupsWithNResults = set()
        for matchup in self.matchups:
            teamResults = len(matchup.team1.winLossTie.wins) if isWin else len(matchup.team2.winLossTie.losses)
            if teamResults >= requiredWinsOrLosses and matchup.pointDifference() != 0:
                matchupsWithNResults.add(matchup)
        return matchupsWithNResults

    @staticmethod
    def __getMostExtremePoints(eligibleMatchups: Set[Matchup], descending: bool, isWin: bool) -> Set[Matchup]:
        sortedMatchups = sorted(eligibleMatchups,
                                key=lambda matchup: MatchupSummary.__getTotalPoints(matchup, isWin),
                                reverse=descending)
        extremeMatchups = set()
        for matchup in sortedMatchups:
            if MatchupSummary.__pointsEqual(matchup, sortedMatchups[0], isWin):
                extremeMatchups.add(matchup)
        return extremeMatchups

    @staticmethod
    def __getTotalPoints(matchup: Matchup, isWin: bool) -> float:
        team = matchup.team1 if isWin else matchup.team2
        return team.points.totalPoints

    @staticmethod
    def __pointsEqual(actual: Matchup, expected: Matchup, isWin: bool) -> bool:
        return MatchupSummary.__getTotalPoints(actual, isWin) == MatchupSummary.__getTotalPoints(expected, isWin)
