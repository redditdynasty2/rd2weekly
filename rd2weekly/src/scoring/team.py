from typing import Union, List

from src.scoring.player import Player
from src.scoring.teamPoints import TeamPoints
from src.scoring.winLossTie import WinLossTie


class Team:
    def __init__(self, name):
        self.__name = name
        self.__points = TeamPoints(name)
        self.__winLossTie = WinLossTie()
        self.__players = []
        self.__pointMode = None

    @property
    def name(self) -> str:
        return self.__name

    @property
    def points(self) -> Union[float, TeamPoints]:
        if self.pointMode == "total":
            return self.__points.totalPoints
        elif self.pointMode == "hitting":
            return self.__points.hittingPoints
        elif self.pointMode == "pitching":
            return self.__points.pitchingPoints
        else:
            return self.__points

    @property
    def winLossTie(self) -> WinLossTie:
        return self.__winLossTie

    @property
    def players(self) -> List[Player]:
        return self.__players

    @property
    def pointMode(self) -> str:
        return self.__pointMode

    @pointMode.setter
    def pointMode(self, hittingPitchingTotal: str) -> None:
        self.__pointMode = hittingPitchingTotal

    def addPlayerToTeam(self, newPlayer: Player) -> None:
        if newPlayer not in self.players:
            self.players.append(newPlayer)
            if newPlayer.active:
                if newPlayer.isPitcher():
                    self.points.addPitchingPoints(newPlayer.points)
                else:
                    self.points.addHittingPoints(newPlayer.points)

    def __eq__(self, other: "Team") -> bool:
        return self.name == other.name

    def __lt__(self, other: "Team") -> bool:
        return self != other and self.points < other.points

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        self.pointMode = None
        builder = "name={0}".format(self.name)
        builder += ","
        builder += "points={0}".format(self.points)
        builder += ","
        builder += "winLossTie={0}".format(self.winLossTie)
        builder += ","
        builder += "players={0}".format(self.players)
        return "Team[{0}]".format(builder)
