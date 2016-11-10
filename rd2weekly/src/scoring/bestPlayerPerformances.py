from src.scoring.bestTrio import BestTrio


class BestPlayerPerformances:
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
            "SP": BestTrio(),
            "RP": BestTrio()
        }
        self.__worstPerformers = {
            "SP": BestTrio(reverse=True),
            "RP": BestTrio(reverse=True)
        }

    @property
    def topPerformers(self):
        return self.__topPerformers

    @property
    def worstPerformers(self):
        return self.__worstPerformers