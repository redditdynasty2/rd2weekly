from src.scoring.trio import Trio


class TeamPoints(Trio):
    def __init__(self, name):
        super(TeamPoints, self).__init__(first=name, second=0, third=0)

    @property
    def name(self):
        return self._first

    @property
    def hittingPoints(self):
        return self._second

    @property
    def pitchingPoints(self):
        return self._third

    @property
    def totalPoints(self):
        return self.hittingPoints + self.pitchingPoints

    def addHittingPoints(self, newHittingPoints):
        self._second+=newHittingPoints

    def addPitchingPoints(self, newPitchingPoints):
        self._second+=newPitchingPoints
