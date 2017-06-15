from typing import List, Set

from src.scoring.bestTrio import BestTrio
from src.scoring.player import Player


class TopPerformers:
    def __init__(self):
        self.__topPerformers = {
            "C": BestTrio(False),
            "1B": BestTrio(False),
            "2B": BestTrio(False),
            "3B": BestTrio(False),
            "SS": BestTrio(False),
            "OF": BestTrio(False),
            "CF": BestTrio(False),
            "U": BestTrio(False),
            "1SP": BestTrio(False),
            "2SP": BestTrio(False),
            "RP": BestTrio(False) }

    def getPerformersForPosition(self, position: str) -> BestTrio:
        if position in self.positions():
            return self.__topPerformers[position]
        else:
            return self.__topPerformers["U"]


    def positions(self) -> List[str]:
        return list(self.__topPerformers.keys())

    @staticmethod
    def getAllStarPositions() -> List[str]:
        return ["C", "1B", "2B", "3B", "SS", "OF", "CF", "U"]

    def addPlayer(self, player: Player) -> None:
        cleanedPlayerPositions = TopPerformers.__getCleanedPlayerPositions(player.positions.copy())
        for position in cleanedPlayerPositions:
            bumpedFromTrio = self.getPerformersForPosition(position).addScorer(player)
            if self.__positionCanFallBackToUtility(position):
                [self.getPerformersForPosition("U").addScorer(bumpedPlayer) for bumpedPlayer in bumpedFromTrio]

    def __repr__(self):
        return "TopPerformers[{0}]".format(self.__topPerformers)

    @staticmethod
    def __getCleanedPlayerPositions(positions: Set[str]) -> Set[str]:
        if "SP" in positions:
            return { "1SP" }
        elif "U" in positions and len(positions) > 1:
            positions.remove("U")
        return positions

    @staticmethod
    def __positionCanFallBackToUtility(position: str) -> bool:
        return position in TopPerformers.getAllStarPositions()
