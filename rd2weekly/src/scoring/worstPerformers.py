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
