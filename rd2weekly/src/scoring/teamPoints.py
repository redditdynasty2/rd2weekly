from src.scoring.trio import Trio


class TeamPoints(Trio):
    def __init__(self, name):
        super(TeamPoints, self).__init__(first=name, second=0, third=0)

    @property
    def name(self):
        return self.__first

    @property
    def hittingPoints(self):
        return self.__second

    @property
    def pitchingPoints(self):
        return self.__third

    @property
    def totalPoints(self):
        return self.hittingPoints + self.pitchingPoints

    def addHittingPoints(self, newHittingPoints):
        self.__second+=newHittingPoints

    def addPitchingPoints(self, newPitchingPoints):
        self.__second+=newPitchingPoints
