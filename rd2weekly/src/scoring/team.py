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
    def name(self):
        return self.__name

    @property
    def points(self):
        if self.pointMode == "total":
            return self.__points.totalPoints
        elif self.pointMode == "hitting":
            return self.__points.hittingPoints
        elif self.pointMode == "pitching":
            return self.__points.pitchingPoints
        else:
            return self.__points

    @property
    def winLossTie(self):
        return self.__winLossTie

    @property
    def players(self):
        return self.__players

    @property
    def pointMode(self):
        return self.__pointMode

    @pointMode.setter
    def pointMode(self, hittingPitching):
        self.__pointMode = hittingPitching

    def addPlayer(self, newPlayer):
        if newPlayer not in self.players:
            if "P" in newPlayer.positions:
                self.points.addPitchingPoints(newPlayer.points)
            else:
                self.points.addHittingPoints(newPlayer.points)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.points < other.points and self != other
