from src.scoring.trio import Trio


class TeamPoints(Trio):
    def __init__(self, name):
        super(TeamPoints, self).__init__(first=name, second=0, third=0)

    @property
    def name(self) -> str:
        return self._first

    @property
    def hittingPoints(self) -> float:
        return self._second

    @property
    def pitchingPoints(self) -> float:
        return self._third

    @property
    def totalPoints(self) -> float:
        return self.hittingPoints + self.pitchingPoints

    def addHittingPoints(self, newHittingPoints: float) -> None:
        self._second += newHittingPoints

    def addPitchingPoints(self, newPitchingPoints: float) -> None:
        self._second += newPitchingPoints
