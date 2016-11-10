from src.scoring.trio import Trio


class WinLossTie(Trio):
    def __init__(self):
        super(WinLossTie, self).__init__(first=[], second=[], third=[])

    @property
    def wins(self):
        return self.__first

    @property
    def losses(self):
        return self.__second

    @property
    def ties(self):
        return self.__third

    def addWin(self, otherTeamName):
        self.wins.append(otherTeamName)

    def addLoss(self, otherTeamName):
        self.losses.append(otherTeamName)

    def addTie(self, otherTeamName):
        self.ties.append(otherTeamName)
