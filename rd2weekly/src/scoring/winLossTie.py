from typing import List

from src.scoring.trio import Trio


class WinLossTie(Trio):
    def __init__(self):
        super(WinLossTie, self).__init__(first=[], second=[], third=[])

    @property
    def wins(self) -> List[str]:
        return self._first

    @property
    def losses(self) -> List[str]:
        return self._second

    @property
    def ties(self) -> List[str]:
        return self._third

    def addWin(self, otherTeamName: str) -> None:
        self.wins.append(otherTeamName)

    def addLoss(self, otherTeamName: str) -> None:
        self.losses.append(otherTeamName)

    def addTie(self, otherTeamName: str) -> None:
        self.ties.append(otherTeamName)

    def __repr__(self) -> str:
        builder = "wins={0}".format(self.wins)
        builder += ","
        builder += "losses={0}".format(self.losses)
        builder += ","
        builder += "ties={0}".format(self.ties)
        return "WinLossTie[{0}]".format(builder)
