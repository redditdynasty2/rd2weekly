from src.scoring.bestTrio import BestTrio


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
    def topPerformers(self):
        return self.__topPerformers

    def positions(self):
        return self.topPerformers.keys()

    def addPlayer(self, player):
        for position in player.positions:
            if position == "SP":
                self.topPerformers["1SP"].addIfTopThree(player)
            elif position in self.topPerformers.keys():
                self.topPerformers[position].addIfTopThree(player)
