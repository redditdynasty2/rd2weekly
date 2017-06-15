from typing import KeysView

from src.scoring.bestTrio import BestTrio
from src.scoring.player import Player


class WorstPerformers:
    def __init__(self):
        self.__worstPerformers = {
            "SP": BestTrio(True),
            "RP": BestTrio(True) }

    def getPerformersForPosition(self, position: str) -> BestTrio:
        if position in self.positions():
            return self.__worstPerformers[position]
        raise ValueError("Unknown worst performer position: " + position)

    def positions(self) -> KeysView[str]:
        return self.__worstPerformers.keys()

    def addPlayer(self, player: Player) -> None:
        for position in player.positions:
            if "SP" in position:
                self.getPerformersForPosition("SP").addScorer(player)
            elif "P" in position:
                self.getPerformersForPosition("RP").addScorer(player)

    def __repr__(self) -> str:
        return "WorstPerformers[{0}]".format(self.__worstPerformers)
