from typing import Dict, List

from src.scoring.bestTrio import BestTrio
from src.scoring.player import Player


class TopPerformers:
    def __init__(self):
        self.__topPerformers = {
            "C": BestTrio(),
            "1B": BestTrio(),
            "2B": BestTrio(),
            "3B": BestTrio(),
            "SS": BestTrio(),
            "OF": BestTrio(),
            "CF": BestTrio(),
            "U": BestTrio(),
            "1SP": BestTrio(),
            "2SP": BestTrio(),
            "RP": BestTrio() }

    @property
    def topPerformers(self) -> Dict[str, BestTrio]:
        return self.__topPerformers

    def positions(self) -> List[str]:
        return list(self.topPerformers.keys())

    def addPlayer(self, player: Player) -> None:
        for position in player.positions:
            if position == "SP":
                self.topPerformers["1SP"].addIfTopThree(player)
            elif position in self.topPerformers.keys():
                self.topPerformers[position].addIfTopThree(player)
            else:
                self.topPerformers["U"].addIfTopThree(player)

    def __repr__(self):
        return "TopPerformers[{0}]".format(self.topPerformers)
