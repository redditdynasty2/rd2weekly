from typing import Dict, KeysView

from src.scoring.bestTrio import BestTrio
from src.scoring.player import Player


class WorstPerformers:
    def __init__(self):
        self.__worstPerformers = {
            "SP": BestTrio(reverse=True),
            "RP": BestTrio(reverse=True) }

    @property
    def worstPerformers(self) -> Dict[str, BestTrio]:
        return self.__worstPerformers

    def positions(self) -> KeysView[str]:
        return self.worstPerformers.keys()

    def addPlayer(self, player: Player) -> None:
        for position in player.positions:
            if "SP" in position:
                self.worstPerformers["SP"].addIfTopThree(player)
            elif position in self.worstPerformers.keys():
                self.worstPerformers[position].addIfTopThree(player)

