from typing import Dict, List

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

    @property
    def topPerformers(self) -> Dict[str, BestTrio]:
        return self.__topPerformers

    def positions(self) -> List[str]:
        return list(self.topPerformers.keys())

    @staticmethod
    def getAllStarPositions():
        return ["C", "1B", "2B", "3B", "SS", "OF", "CF", "U"]

    def addPlayer(self, player: Player) -> None:
        for position in player.positions:
            if position == "SP":
                self.topPerformers["1SP"].addScorer(player)
            elif position in self.topPerformers.keys():
                self.topPerformers[position].addScorer(player)
            else:
                self.topPerformers["U"].addScorer(player)

    def __repr__(self):
        return "TopPerformers[{0}]".format(self.topPerformers)
