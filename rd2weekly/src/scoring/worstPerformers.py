from src.scoring.bestTrio import BestTrio


class WorstPerformers:
    def __init__(self):
        self.__worstPerformers = {
            "SP": BestTrio(reverse=True),
            "RP": BestTrio(reverse=True) }

    @property
    def worstPerformers(self):
        return self.__worstPerformers

    def positions(self):
        return self.worstPerformers.keys()

    def addPlayer(self, player):
        for position in player.positions:
            if "SP" in position:
                self.worstPerformers["SP"].addIfTopThree(player)
            elif position in self.worstPerformers.keys():
                self.worstPerformers[position].addIfTopThree(player)

