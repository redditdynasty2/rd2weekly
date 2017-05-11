from typing import Union, Set

from src.scoring.player import Player
from src.scoring.team import Team
from src.scoring.trio import Trio
PointScorer = Union[Player, Team]

class BestTrio(Trio):
    def __init__(self, reverse: bool = False):
        super(BestTrio, self).__init__(first=set(), second=set(), third=set())
        self.__reverse = reverse

    @property
    def first(self) -> Set[PointScorer]:
        return self._first

    @property
    def second(self) -> Set[PointScorer]:
        return self._second

    @property
    def third(self) -> Set[PointScorer]:
        return self._third

    def addIfTopThree(self, newPoints: PointScorer) -> bool:
        allPlayerInTopThree = self.first.union(self.second.union(self.third))
        if newPoints not in allPlayerInTopThree:
            spot = 0
            while spot < 3:
                spot += 1
                if self.__jumpSpotIfAllowed(spot, newPoints):
                    self.__pruneToTopThree()
                    return True
        return False

    def __jumpSpotIfAllowed(self, spot: int, newPoints: PointScorer) -> bool:
        comparison = self.__pointComparison(spot, newPoints)
        if comparison > 0:
            self.__jumpSpot(spot, newPoints)
        elif comparison == 0:
            self.__addToSpot(spot, newPoints)
        return comparison >= 0


    def __pointComparison(self, spot: int, newPoints: PointScorer) -> int:
        existingPoints = self.__getExistingPointsFromSpot(spot)
        if existingPoints:
            ourPoints = next(iter(existingPoints))
            multiplier = -1 if self.__reverse else 1
            return multiplier * ((newPoints > ourPoints) - (newPoints < ourPoints))
        else:
            return 1

    def __getExistingPointsFromSpot(self, spot: int) -> Set[PointScorer]:
        if spot == 1:
            return self.first
        elif spot == 2:
            return self.second
        else:
            return self.third

    def __jumpSpot(self, spot: int, newPoints: PointScorer) -> None:
        i = 3
        while i >= spot:
            if i == 3:
                self._third = { newPoints }
            elif i == 2:
                self._third = self.second.copy()
                self._second = { newPoints }
            else:
                self._second = self.first.copy()
                self._first = { newPoints }
            i-=1

    def __addToSpot(self, spot: int, newPoints: PointScorer) -> None:
        self.__getExistingPointsFromSpot(spot).add(newPoints)

    def __pruneToTopThree(self) -> None:
        if len(self.first) > 2:
            self._second = set()
        if len(self.first) + len(self.second) > 2:
            self._third = set()

    def __repr__(self) -> str:
        builder = "first={0}".format(self.first)
        builder += ","
        builder += "second={0}".format(self.second)
        builder += ","
        builder += "third={0}".format(self.third)
        builder += ","
        builder += "reverse={0}".format(self.__reverse)
        return "BestTrio[{0}]".format(builder)
