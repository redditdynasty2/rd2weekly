from src.scoring.team import Team


class Matchup:
    def __init__(self, team1: Team, team2: Team):
        [sortedTeam1, sortedTeam2] = list({ team1, team2 })
        self.__team1 = sortedTeam1
        self.__team2 = sortedTeam2

    @property
    def team1(self):
        return self.__team1

    @property
    def team2(self):
        return self.__team2

    def pointDifference(self):
        return self.team1.points - self.team2.points

    def __eq__(self, other: "Matchup") -> bool:
        return { self.team1, self.team2 } == { self.team1, self.team2 }

    def __lt__(self, other: "Matchup") -> bool:
        return self != other and self.pointDifference() < other.pointDifference()

    def __hash__(self) -> int:
        return hash({ self.team1, self.team2 })

    def __repr__(self) -> str:
        builder = "team1={0}".format(self.team1)
        builder += ","
        builder += "team2={0}".format(self.team2)
        return "Matchup[{0}]".format(builder)
