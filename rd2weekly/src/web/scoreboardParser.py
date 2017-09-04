import re
from typing import List, Tuple

from bs4 import BeautifulSoup

from src.scoring.matchup import Matchup
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
        parser.scoreboard.syncTeamsWithMatchups()
        return parser.scoreboard

    @property
    def scoreboard(self) -> Scoreboard:
        return self.__scoreboard

    @property
    def browserSession(self) -> RD2BrowserSession:
        return self.__browserSession

    def __parseMatchups(self) -> List[str]:
        soup = BeautifulSoup(self.browserSession.getScoreboardBase(), "html.parser")
        parsedMatchups = []
        for matchup in soup.find_all("table", id=re.compile(r"^matchup_hilite_\d+$")):
            matchupSoup = matchup.find("a", href=re.compile(r"javascript:Atl.swap\(\d+\)"))
            if matchupSoup:
                parsedMatchups.append(matchupSoup["href"])
        return parsedMatchups

    def __scrapeMatchup(self, matchupLink: str) -> None:
        self.__loadMatchupInBrowser(matchupLink)
        team1 = self.__processTeam("away")
        team2 = self.__processTeam("home")
        self.__processMatchup(team1, team2)

    def __loadMatchupInBrowser(self, matchupLink: str) -> None:
        self.browserSession.getScoreboardBase()
        self.browserSession.clickOnCssElement("a[href='{0}']".format(matchupLink))

    def __processTeam(self, homeOrAway: str) -> Team:
        soup = BeautifulSoup(self.browserSession.getSource(), "html.parser")
        teamName = soup.find("td", class_="teamname", id="{0}_big_name".format(homeOrAway)).string.strip()
        team = self.scoreboard.getTeam(teamName)
        if teamName in Team.invalidOpponents():
            return Team(teamName)
        elif not team:
            team = Team(teamName)
            ScoreboardParser.__createNewTeam(team, soup, homeOrAway)
            self.scoreboard.teams.add(team)
        return team

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
        player = Player(name, cbsId, team.name, positions, points, active)
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
        return int(idString)

    @staticmethod
    def __getPlayerPoints(soup: BeautifulSoup) -> float:
        tag = soup.find("a", class_="scoreLink")
        return float(tag.string)

    def __processMatchup(self, team1: Team, team2: Team) -> None:
        matchup = Matchup(team1, team2)
        if matchup.pointDifference() == 0:
            result1 = result2 = "tie"
        else:
            result1 = "win"
            result2 = "loss"
        for team in self.scoreboard.teams:
            if team == matchup.team1:
                team.winLossTie.addResult(result1, matchup.team2.name)
                matchup.team1.winLossTie.addResult(result1, matchup.team2.name)
            if team == matchup.team2:
                team.winLossTie.addResult(result2, matchup.team1.name)
                matchup.team2.winLossTie.addResult(result2, matchup.team1.name)
        self.scoreboard.matchups.add(matchup)
