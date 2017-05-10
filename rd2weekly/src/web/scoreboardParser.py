import re
from typing import List, Tuple

from bs4 import BeautifulSoup

from src.scoring.player import Player
from src.scoring.scoreboard import Scoreboard
from src.scoring.team import Team
from src.web.rd2BrowserSession import RD2BrowserSession


class ScoreboardParser:
    def __init__(self, browserSession: RD2BrowserSession):
        self.__scoreboard = Scoreboard()
        self.__browserSession = browserSession

    @staticmethod
    def parseScoreboard(browserSession: RD2BrowserSession) -> Scoreboard:
        parser = ScoreboardParser(browserSession)
        matchupLinks = parser.__parseMatchups()
        [parser.__scrapeMatchup(matchup) for matchup in matchupLinks]
        return parser.scoreboard

    @property
    def scoreboard(self) -> Scoreboard:
        return self.__scoreboard

    @property
    def browserSession(self) -> RD2BrowserSession:
        return self.__browserSession

    def __parseMatchups(self) -> List[str]:
        soup = BeautifulSoup(self.browserSession.getScoreboardBase(), "html.parser")
        matchups = soup.find_all("table", id=re.compile(r"^matchup_hilite_\d+$"))
        return [matchup.find("a", href=re.compile(r"javascript:Atl.swap\(\d+\)"))["href"] for matchup in matchups]

    def __scrapeMatchup(self, matchupLink: str) -> None:
        self.__loadMatchupInBrowser(matchupLink)
        self.__processTeam("away")
        self.__processTeam("home")

    def __loadMatchupInBrowser(self, matchupLink: str) -> None:
        self.browserSession.getScoreboardBase()
        self.browserSession.clickOnCssElement("a[href='{0}']".format(matchupLink))

    def __processTeam(self, homeOrAway: str) -> None:
        soup = BeautifulSoup(self.browserSession.getSource(), "html.parser")
        teamName = soup.find("td", class_="teamname", id="{0}_big_name".format(homeOrAway)).string.strip()
        if teamName not in [team.name for team in self.scoreboard.teams]:
            print("Team {0} getting added".format(teamName))
            team = Team(teamName)
            ScoreboardParser.__createNewTeam(team, soup, homeOrAway)
            self.scoreboard.teams.append(team)
        else:
            print("Team {0} already taken care of".format(teamName))

    @staticmethod
    def __createNewTeam(team: Team, soup: BeautifulSoup, homeOrAway: str) -> None:
        activeSoup = soup.find("tbody", id="{0}_active".format(homeOrAway))
        ScoreboardParser.__processPlayers(team, activeSoup, True)
        reserveSoup = soup.find("tbody", id="{0}_reserve".format(homeOrAway))
        ScoreboardParser.__processPlayers(team, reserveSoup, False)

    @staticmethod
    def __processPlayers(team: Team, soup: BeautifulSoup, active: bool) -> None:
        activePlayers = soup.find_all("tr", align="left", class_="bg2", height="49", valign="middle")
        [ScoreboardParser.__addPlayerToTeam(team, playerSoup, active) for playerSoup in activePlayers]

    @staticmethod
    def __addPlayerToTeam(team: Team, activePlayerSoup: BeautifulSoup, active: bool) -> None:
        cbsId, name, positions = ScoreboardParser.__getPlayerInfo(activePlayerSoup)
        points = ScoreboardParser.__getPlayerPoints(activePlayerSoup)
        player = Player(name, cbsId, positions, points, active)
        print("Adding player {0} to team {1}".format(team.name, name))
        team.addPlayerToTeam(player)

    @staticmethod
    def __getPlayerInfo(soup: BeautifulSoup) -> Tuple[int, str, List[str]]:
        tag = soup.find("a", class_="playerLink")
        cbsId = ScoreboardParser.getPlayerId(tag)
        fullName = " ".join(tag["title"].split(" ")[:-2])
        tempPosition = tag["title"].split(" ")[-2]
        if "F" in tempPosition:
            position = tempPosition if tempPosition == "CF" else "OF"
            return cbsId, fullName, [position]
        else:
            return cbsId, fullName, [tempPosition]

    @staticmethod
    def getPlayerId(miniSoup: BeautifulSoup) -> int:
        idString = miniSoup["href"][len("/players/playerpage/"):]
        try:
            return int(idString)
        except ValueError:
            return 0

    @staticmethod
    def __getPlayerPoints(soup: BeautifulSoup) -> float:
        tag = soup.find("a", class_="scoreLink")
        return float(tag.string)
