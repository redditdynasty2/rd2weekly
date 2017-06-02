from src.scoring.scoreboard import Scoreboard
from src.scoring.topPerformers import TopPerformers
from src.scoring.worstPerformers import WorstPerformers
from src.summary.allStarSummary import AllStarSummary
from src.summary.trioSummary import TrioSummary
from src.text.jsonFileHandler import JsonFileHandler

TOP_THREE_TEAMS_HEADER = "Top Three Teams of the Week"
WORST_THREE_TEAMS_HEADER = "Not Top Three Teams of the Week"
TOP_THREE_OFFENSES_HEADER = "Offensive Powerhouses"
WORST_THREE_OFFENSES_HEADER = "Weaklings"
TOP_THREE_PITCHING_HEADER = "Pitching Factories"
WORST_THREE_PITCHING_HEADER = "Burnt-down Factories"

TOP_TWO_START_PITCHER_HEADER = "2 Start Saviors"
TOP_ONE_START_PITCHER_HEADER = "1 Start Gods"
WORST_STARTING_PITCHER_HEADER = "Had a Bad Day"
TOP_RELIEF_PITCHER_HEADER = "No Start Workhorses"
WORST_RELIEF_PITCHER_HEADER = "The Bullpen Disasters"


class RedditSummary:
    def __init__(self, scoreboard, topPerformers, worstPerformers, records):
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
        return "\n\n".join([teamTrios, allStars])

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
        trios = []
        trios.append(TrioSummary.getTrioString(TOP_THREE_TEAMS_HEADER, self.scoreboard.topThreeTotal))
        trios.append(TrioSummary.getTrioString(WORST_THREE_TEAMS_HEADER, self.scoreboard.worstThreeTotal))
        trios.append(TrioSummary.getTrioString(TOP_THREE_OFFENSES_HEADER, self.scoreboard.topThreeHitting))
        trios.append(TrioSummary.getTrioString(WORST_THREE_OFFENSES_HEADER, self.scoreboard.worstThreeHitting))
        trios.append(TrioSummary.getTrioString(TOP_THREE_PITCHING_HEADER, self.scoreboard.topThreePitching))
        trios.append(TrioSummary.getTrioString(WORST_THREE_PITCHING_HEADER, self.scoreboard.worstThreePitching))
        return "\n\n".join(trios)

    def __getAllStars(self) -> str:
        allStarPositions = ["C", "1B", "2B", "3B", "SS", "OF", "CF", "U"]
        return AllStarSummary.getAllStarString(self.topPerformers, allStarPositions)

    #TODO: get working, shouldn't be hard, mostly done with trioSummary
    def __getPitcherPerformances(self) -> str:
        trios = []
        trios.append(TrioSummary.getTrioString(TOP_TWO_START_PITCHER_HEADER, self.topPerformers.topPerformers["2SP"]))
        trios.append(TrioSummary.getTrioString(TOP_ONE_START_PITCHER_HEADER, self.topPerformers.topPerformers["1SP"]))
        trios.append(TrioSummary.getTrioString(TOP_RELIEF_PITCHER_HEADER, self.worstPerformers.worstPerformers["RP"]))
        trios.append(TrioSummary.getTrioString(WORST_STARTING_PITCHER_HEADER, self.worstPerformers.worstPerformers["SP"]))
        trios.append(TrioSummary.getTrioString(WORST_RELIEF_PITCHER_HEADER, self.worstPerformers.worstPerformers["RP"]))
        return "\n\n".join(trios)

    #TODO: get this working
    def __getMatchupSummary(self):
        pass
