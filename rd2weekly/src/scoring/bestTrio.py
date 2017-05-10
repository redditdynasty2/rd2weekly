from typing import Union, Set

from src.scoring.player import Player
from src.scoring.team import Team
from src.scoring.trio import Trio


class BestTrio(Trio):
    def __init__(self, reverse=False):
        super(BestTrio, self).__init__(first=set(), second=set(), third=set())
        self.__reverse = reverse

    @property
    def first(self) -> Set[Union[Player, Team]]:
        return self._first

    @property
    def second(self) -> Set[Union[Player, Team]]:
        return self._second

    @property
    def third(self) -> Set[Union[Player, Team]]:
        return self._third

    def addIfTopThree(self, newPoints: Union[Player, Team]) -> bool:
        allPlayerInTopThree = self.first.union(self.second.union(self.third))
        if newPoints not in allPlayerInTopThree:
            spot = 1
            while spot <= 3:
                if self.__jumpSpotIfAllowed(spot, newPoints):
                    self.__pruneToTopThree()
                    return True
        return False

    def __jumpSpotIfAllowed(self, spot: int, newPoints: Union[Player, Team]) -> bool:
        comparison = self.__pointComparison(spot, newPoints.points)
        if comparison > 0:
            return self.__jumpSpot(spot, newPoints)
        elif comparison == 0:
            return self.__addToSpot(spot, newPoints)


    def __pointComparison(self, spot: int, newPoints: Union[Player, Team]) -> int:
        existingPoints = self.__getExistingPointsFromSpot(spot)
        if existingPoints:
            ourPoints = next(iter(existingPoints))
            multiplier = -1 if self.__reverse else 1
            return multiplier * ((newPoints > ourPoints) - (newPoints < ourPoints))
        else:
            return 1

    def __getExistingPointsFromSpot(self, spot: int) -> set:
        if spot == 1:
            return self.first
        elif spot == 2:
            return self.second
        else:
            return self.third

    def __jumpSpot(self, spot: int, newPoints: Union[Player, Team]) -> bool:
        i = 3
        while i >= spot:
            if i == 3:
                self.__third = { newPoints }
            elif i == 2:
                self.__third = self.second
                self.__second = { newPoints }
            else:
                self.__second = self.first
                self.__first = { newPoints }
            i-=1
        return True

    def __addToSpot(self, spot: int, newPoints: Union[Player, Team]) -> bool:
        self.__getExistingPointsFromSpot(spot).add(newPoints)
        return True

    def __pruneToTopThree(self) -> None:
        if len(self.first) > 3:
            self.__second = set()
        if len(self.first) + len(self.second) > 3:
            self.__third = set()
