class Player:
    def __init__(self, name, cbsIdNumber, positions, points, active):
        self.__name = name
        self.__cbsIdNumber = cbsIdNumber
        self.__positions = set(positions)
        self.__points = points
        self.__active = active

    @property
    def name(self):
        return self.__name

    @property
    def cbsIdNumber(self):
        return self.__cbsIdNumber

    @property
    def positions(self):
        return self.__positions

    @property
    def points(self):
        return self.__points

    @property
    def active(self):
        return self.__active

    def merge(self, other):
        assert self == other and self.points == other.points
        for position in other.positions:
            if "P" in position:
                # we trust the pitcher eligibility passed in with the other player
                self.__positions = { position }
            else:
                self.positions.add(position)

    def __eq__(self, other):
        return self.name == other.name and self.cbsIdNumber == other.cbsId

    def __lt__(self, other):
        return self.points < other.points and self != other
