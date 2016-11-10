class Player:
    def __init__(self, name, cbsIdNumber, positions, points, active):
        self.__name = name
        self.__cbsIdNumber = cbsIdNumber
        self.__positions = positions
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

    @positions.setter
    def positions(self, newPositions):
        self.__positions = newPositions

    def __eq__(self, other):
        return self.__cbsIdNumber == other.__cbsId

    def __lt__(self, other):
        return self.points < other.points and self != other
