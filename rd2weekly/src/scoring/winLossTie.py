from typing import Set

from src.scoring.trio import Trio


class WinLossTie(Trio):
    def __init__(self):
        super(WinLossTie, self).__init__(first=set(), second=set(), third=set())

    @property
    def wins(self) -> Set[str]:
        return self._first

    @property
    def losses(self) -> Set[str]:
        return self._second

    @property
    def ties(self) -> Set[str]:
        return self._third

    def addResult(self, result: str, otherTeamName: str) -> None:
        if result == "win":
            self.wins.add(otherTeamName)
        elif result == "loss":
            self.losses.add(otherTeamName)
        elif result == "tie":
            self.ties.add(otherTeamName)
        else:
            raise ValueError("Unknown result type " + result)

    def __repr__(self) -> str:
        builder = "wins={0}".format(self.wins)
        builder += ","
        builder += "losses={0}".format(self.losses)
        builder += ","
        builder += "ties={0}".format(self.ties)
        return "WinLossTie[{0}]".format(builder)
