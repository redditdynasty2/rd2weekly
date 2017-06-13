from typing import Dict, KeysView

from src.scoring.bestTrio import BestTrio
from src.scoring.player import Player


class WorstPerformers:
    def __init__(self):
        self.__worstPerformers = {
            "SP": BestTrio(True),
            "RP": BestTrio(True) }

    @property
    def worstPerformers(self) -> Dict[str, BestTrio]:
        return self.__worstPerformers

    def positions(self) -> KeysView[str]:
        return self.worstPerformers.keys()

    def addPlayer(self, player: Player) -> None:
        for position in player.positions:
            if "SP" in position:
                self.worstPerformers["SP"].addScorer(player)
            elif position in self.worstPerformers.keys():
                self.worstPerformers[position].addScorer(player)

    def __repr__(self) -> str:
        return "WorstPerformers[{0}]".format(self.worstPerformers)
