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
        if not self.__topThreeTotal.first:
            self.__setTeamPointsMode("total")
            [self.__topThreeTotal.addIfTopThree(team) for team in self.teams]
            self.__resetTeamPointsMode()
        return self.__topThreeTotal

    def __setTeamPointsMode(self, mode):
        for team in self.teams:
            team.pointMode = mode

    def __resetTeamPointsMode(self):
        self.__setTeamPointsMode(None)

    @property
    def worstThreeTotal(self):
        if not self.__worstThreeTotal.first:
            self.__setTeamPointsMode("total")
            [self.__worstThreeTotal.addIfTopThree(team) for team in self.teams]
            self.__resetTeamPointsMode()
        return self.__worstThreeTotal

    @property
    def topThreeHitting(self):
        if not self.__topThreeHitting.first:
            self.__setTeamPointsMode("hitting")
            [self.__topThreeHitting.addIfTopThree(team) for team in self.teams]
            self.__resetTeamPointsMode()
        return self.__topThreeHitting

    @property
    def worstThreeHitting(self):
        if not self.__worstThreeHitting.first:
            self.__setTeamPointsMode("hitting")
            [self.__worstThreeHitting.addIfTopThree(team) for team in self.teams]
            self.__resetTeamPointsMode()
        return self.__worstThreeHitting

    @property
    def topThreePitching(self):
        if not self.__topThreePitching.first:
            self.__setTeamPointsMode("pitching")
            [self.__topThreePitching.addIfTopThree(team) for team in self.teams]
            self.__resetTeamPointsMode()
        return self.__topThreePitching

    @property
    def worstThreePitching(self):
        if not self.__worstThreePitching.first:
            self.__setTeamPointsMode("pitching")
            [self.__worstThreePitching.addIfTopThree(team) for team in self.teams]
            self.__resetTeamPointsMode()
        return self.__worstThreePitching

    def updatePlayer(self, player):
        for existing in [team for team in self.teams]:
            if existing == player:
                existing.merge(player)
                continue
