from src.scoring.scoreboard import Scoreboard
from src.scoring.topPerformers import TopPerformers
from src.scoring.worstPerformers import WorstPerformers
from src.summary import trioSummary, matchupSummary
from src.summary.allStarSummary import AllStarSummary
from src.summary.matchupSummary import MatchupSummary
from src.summary.trioSummary import TrioSummary
from src.text.jsonFileHandler import JsonFileHandler


class RedditSummary:
    def __init__(self,
                 scoreboard: Scoreboard,
                 topPerformers: TopPerformers,
                 worstPerformers: WorstPerformers,
                 records: JsonFileHandler):
        self.__scoreboard = scoreboard
        self.__topPerformers = topPerformers
        self.__worstPerformers = worstPerformers
        self.__records = records

    @staticmethod
    def generateSummary(scoreboard: Scoreboard,
                        topPerformers: TopPerformers,
                        worstPerformers: WorstPerformers,
                        records: JsonFileHandler) -> str:
        summary = RedditSummary(scoreboard, topPerformers, worstPerformers, records)
        teamTrios = summary.__getTeamPerformances()
        allStars = summary.__getAllStars()
        pitcherTrios = summary.__getPitcherPerformances()
        matchups = summary.__getMatchupSummary()
        return "\n\n".join([teamTrios, allStars, pitcherTrios, matchups])

    @property
    def scoreboard(self) -> Scoreboard:
        return self.__scoreboard

    @property
    def topPerformers(self) -> TopPerformers:
        return self.__topPerformers

    @property
    def worstPerformers(self) -> WorstPerformers:
        return self.__worstPerformers

    @property
    def records(self) -> JsonFileHandler:
        return self.__records

    def __getTeamPerformances(self) -> str:
        trios = [
                TrioSummary.getTrioString(trioSummary.TOP_THREE_TEAMS_HEADER, self.scoreboard.topThreeTotal()),
                TrioSummary.getTrioString(trioSummary.WORST_THREE_TEAMS_HEADER, self.scoreboard.worstThreeTotal()),
                TrioSummary.getTrioString(trioSummary.TOP_THREE_OFFENSES_HEADER, self.scoreboard.topThreeHitting()),
                TrioSummary.getTrioString(trioSummary.WORST_THREE_OFFENSES_HEADER, self.scoreboard.worstThreeHitting()),
                TrioSummary.getTrioString(trioSummary.TOP_THREE_PITCHING_HEADER, self.scoreboard.topThreePitching()),
                TrioSummary.getTrioString(trioSummary.WORST_THREE_PITCHING_HEADER, self.scoreboard.worstThreePitching())
        ]
        self.scoreboard.resetTeamPointsMode()
        return "\n\n".join(trios)

    def __getAllStars(self) -> str:
        return AllStarSummary.getAllStarString(self.topPerformers)

    def __getPitcherPerformances(self) -> str:
        trios = [
                TrioSummary.getTrioString(trioSummary.TOP_TWO_START_PITCHER_HEADER, self.topPerformers.getPerformersForPosition("2SP")),
                TrioSummary.getTrioString(trioSummary.TOP_ONE_START_PITCHER_HEADER, self.topPerformers.getPerformersForPosition("1SP")),
                TrioSummary.getTrioString(trioSummary.TOP_RELIEF_PITCHER_HEADER, self.topPerformers.getPerformersForPosition("RP")),
                TrioSummary.getTrioString(trioSummary.WORST_STARTING_PITCHER_HEADER, self.worstPerformers.getPerformersForPosition("SP")),
                TrioSummary.getTrioString(trioSummary.WORST_RELIEF_PITCHER_HEADER, self.worstPerformers.getPerformersForPosition("RP"))
        ]
        return "\n\n".join(trios)

    #TODO: get this working
    def __getMatchupSummary(self):
        summary = MatchupSummary(self.scoreboard.matchups)
        lines = [
            summary.getMatchupString(matchupSummary.CLOSEST_MATCHUP),
            summary.getMatchupString(matchupSummary.BIGGEST_BLOWOUT),
            summary.getMatchupString(matchupSummary.STRONGEST_ONE_LOSS),
            summary.getMatchupString(matchupSummary.STRONGEST_TWO_LOSSES),
            summary.getMatchupString(matchupSummary.WEAKEST_ONE_WIN),
            summary.getMatchupString(matchupSummary.WEAKEST_TWO_WINS)
        ]
        return "\n\n".join(lines)
