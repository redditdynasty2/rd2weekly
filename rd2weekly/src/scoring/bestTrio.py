from typing import Union, Set

from src.scoring.player import Player
from src.scoring.team import Team
from src.scoring.trio import Trio

PointScorer = Union[Player, Team]


class BestTrio(Trio):
    def __init__(self, sortAscending: bool):
        super(BestTrio, self).__init__(first=set(), second=set(), third=set())
        self.__isAscending = sortAscending

    @property
    def first(self) -> Set[PointScorer]:
        return self._first

    @property
    def second(self) -> Set[PointScorer]:
        return self._second

    @property
    def third(self) -> Set[PointScorer]:
        return self._third

    @property
    def isAscending(self) -> bool:
        return self.__isAscending

    def getRank(self, pointScorer: PointScorer) -> int:
        for rank in range(1, 4):
            if self.__pointComparison(rank, pointScorer) >= 0:
                return rank
        else:
            return 4

    def __pointComparison(self, rank: int, newPoints: PointScorer) -> int:
        existingAtRank = self.__getExistingRank(rank)
        if existingAtRank:
            existingPoints = next(iter(existingAtRank))
            multiplier = -1 if self.isAscending else 1
            return multiplier * ((newPoints > existingPoints) - (newPoints < existingPoints))
        else:
            return 1

    def __getExistingRank(self, rank: int) -> Set[PointScorer]:
        if rank == 1:
            return self.first
        elif rank == 2:
            return self.second
        else:
            return self.third

    def addScorer(self, newPoints: PointScorer) -> Set[PointScorer]:
        """returns scorers that were displaced, if any"""
        rank = self.getRank(newPoints)
        if rank != 4:
            return self.__jumpOrJoinRank(rank, newPoints)
        return set()

    def __jumpOrJoinRank(self, rank: int, newPoints: PointScorer) -> Set[PointScorer]:
        comparison = self.__pointComparison(rank, newPoints)
        if comparison > 0:
            return self.__jumpRank(rank, newPoints)
        elif comparison == 0:
            self.__addToRank(rank, newPoints)
            return set()
        else:
            raise ValueError("Point scorer '{0}' cannot jump rank {1}".format(newPoints, rank))

    def __jumpRank(self, rank: int, newPoints: PointScorer) -> Set[PointScorer]:
        """returns scorers that were displaced"""
        i = 3
        retval = self.third
        while i >= rank:
            if i == 3:
                self._third = { newPoints }
            elif i == 2:
                self._third = self.second
                self._second = { newPoints }
            else:
                self._second = self.first
                self._first = { newPoints }
            i-=1
        self.__pruneToTopThree()
        return retval

    def __addToRank(self, rank: int, newPoints: PointScorer) -> None:
        self.__getExistingRank(rank).add(newPoints)
        self.__pruneToTopThree()

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
        builder += "isAscending={0}".format(self.isAscending)
        return "BestTrio[{0}]".format(builder)
