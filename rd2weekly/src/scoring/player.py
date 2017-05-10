from typing import Set, List


class Player:
    def __init__(self, name: str, cbsIdNumber: int, positions: List[str], points: float, active: bool):
        self.__name = name
        self.__cbsIdNumber = cbsIdNumber
        self.__positions = set(positions)
        self.__points = points
        self.__active = active

    @property
    def name(self) -> str:
        return self.__name

    @property
    def cbsIdNumber(self) -> int:
        return self.__cbsIdNumber

    @property
    def positions(self) -> Set[str]:
        return self.__positions

    @property
    def points(self) -> float:
        return self.__points

    @property
    def active(self) -> bool:
        return self.__active

    def merge(self, other: "Player") -> None:
        assert self == other and self.points == other.points
        for position in other.positions:
            if "P" in position:
                # we trust the pitcher eligibility passed in with the other player
                self.__positions = { position }
            elif position:
                self.positions.add(position)

    def __str__(self) -> str:
        builder = "name={0}".format(self.name)
        builder += ","
        builder += "cbsIdNumber={0}".format(self.cbsIdNumber)
        builder += ","
        builder += "positions={0}".format(self.positions)
        builder += ","
        builder += "points={0}".format(self.points)
        builder += ","
        builder += "active={0}".format(str(self.active))
        return "Player[{0}]".format(builder)

    def __eq__(self, other: "Player") -> bool:
        return self.name == other.name and self.cbsIdNumber == other.cbsIdNumber

    def __lt__(self, other: "Player") -> bool:
        return self.points < other.points and self != other

    def __hash__(self) -> int:
        return hash("{0}-{1}".format(self.name, self.cbsIdNumber))
