from typing import Set, Union

from src.scoring.bestTrio import BestTrio
from src.scoring.matchup import Matchup
from src.scoring.player import Player
from src.scoring.team import Team


class Scoreboard:
    def __init__(self):
        self.__teams = set()
        self.__matchups = set()

    @property
    def teams(self) -> Set[Team]:
        return self.__teams

    @property
    def matchups(self) -> Set[Matchup]:
        return self.__matchups

    def getTeam(self, teamName: str) -> Union[Team, None]:
        for team in self.teams:
            if team.name == teamName:
                return team
        return None

    def topThreeTotal(self) -> BestTrio:
        return self.__getTopThreeTeams("total", False)

    def __getTopThreeTeams(self, pointMode: str, reverse: bool) -> BestTrio:
        trio = BestTrio(reverse)
        self.__setTeamPointsMode(pointMode)
        [trio.addScorer(team) for team in self.teams]
        return trio

    def __setTeamPointsMode(self, mode) -> None:
        for team in self.teams:
            team.pointMode = mode

    def worstThreeTotal(self) -> BestTrio:
        return self.__getTopThreeTeams("total", True)

    def topThreeHitting(self) -> BestTrio:
        return self.__getTopThreeTeams("hitting", False)

    def worstThreeHitting(self) -> BestTrio:
        return self.__getTopThreeTeams("hitting", True)

    def topThreePitching(self) -> BestTrio:
        return self.__getTopThreeTeams("pitching", False)

    def worstThreePitching(self) -> BestTrio:
        return self.__getTopThreeTeams("pitching", True)

    def resetTeamPointsMode(self) -> None:
        self.__setTeamPointsMode(None)

    def updatePlayer(self, player: Player) -> Player:
        for team in self.teams:
            for existing in team.players:
                if existing == player:
                    existing.merge(player)
                    return existing
        return player

    def __repr__(self) -> str:
        builder = "teams={0}".format(self.teams)
        builder += ","
        builder += "matchups={0}".format(self.matchups)
        return "Scoreboard[{0}]".format(builder)
