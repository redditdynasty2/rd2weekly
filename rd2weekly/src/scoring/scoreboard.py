from src.scoring.bestTrio import BestTrio


class Scoreboard:
    def __init__(self):
        self.__teams = []
        self.__topThreeTotal = BestTrio()
        self.__worstThreeTotal = BestTrio(reverse=True)
        self.__topThreeHitting = BestTrio()
        self.__worstThreeHitting = BestTrio(reverse=True)
        self.__topThreePitching = BestTrio()
        self.__worstThreePitching = BestTrio(reverse=True)

    @property
    def teams(self):
        return self.__teams

    @property
    def topThreeTotal(self):
        return self.__topThreeTotal

    @property
    def worstThreeTotal(self):
        return self.__worstThreeTotal

    @property
    def topThreeHitting(self):
        return self.__topThreeHitting

    @property
    def worstThreeHitting(self):
        return self.__worstThreeHitting

    @property
    def topThreePitching(self):
        return self.__topThreePitching

    @property
    def worstThreePitching(self):
        return self.__worstThreePitching

    def getTopThreeTeams(self):
        self.__setTeamPointsMode("total")
        [self.topThreeTotal.addIfTopThree(team) for team in self.teams]
        self.__resetTeamPointsMode()
        return self.topThreeTotal

    def __setTeamPointsMode(self, mode):
        for team in self.teams:
            team.pointMode = mode

    def __resetTeamPointsMode(self):
        self.__setTeamPointsMode(None)

    def getWorstThreeTeams(self):
        self.__setTeamPointsMode("total")
        [self.worstThreeTotal.addIfTopThree(team) for team in self.teams]
        self.__resetTeamPointsMode()
        return self.worstThreeTotal

    def getTopThreeHittingTeams(self):
        self.__setTeamPointsMode("hitting")
        [self.topThreeHitting.addIfTopThree(team) for team in self.teams]
        self.__resetTeamPointsMode()
        return self.topThreeHitting

    def getWorstThreeHittingTeams(self):
        self.__setTeamPointsMode("hitting")
        [self.worstThreeHitting.addIfTopThree(team) for team in self.teams]
        self.__resetTeamPointsMode()
        return self.worstThreeHitting

    def getTopThreePitchingTeams(self):
        self.__setTeamPointsMode("pitching")
        [self.topThreePitching.addIfTopThree(team) for team in self.teams]
        self.__resetTeamPointsMode()
        return self.topThreePitching

    def getWorstThreePitchingTeams(self):
        self.__setTeamPointsMode("pitching")
        [self.worstThreePitching.addIfTopThree(team) for team in self.teams]
        self.__resetTeamPointsMode()
        return self.worstThreePitching

