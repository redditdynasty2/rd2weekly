import re

from bs4 import BeautifulSoup

from src.scoring.player import Player
from src.scoring.team import Team


class ScoreboardParser:
    def __init__(self, scoreboard, browserSession):
        self.__scoreboard = scoreboard
        self.__browserSession = browserSession

    @staticmethod
    def parseScoreboard(scoreboard, browserSession):
        parser = ScoreboardParser(scoreboard, browserSession)
        matchupLinks = parser.__parseMatchups()
        [parser.__scrapeMatchup(matchup) for matchup in matchupLinks]
        return parser

    @property
    def scoreboard(self):
        return self.__scoreboard

    @property
    def browserSession(self):
        return self.__browserSession

    def __parseMatchups(self):
        soup = BeautifulSoup(self.browserSession.getScoreboardBase(), "html.parser")
        matchups = soup.find_all("table", id=re.compile(r"^matchup_hilite_\d+$"))
        return [matchup.find("a", href=re.compile(r"javascript:Atl.swap\(\d+\)"))["href"] for matchup in matchups]

    def __scrapeMatchup(self, matchupLink):
        self.__loadMatchupInBrowser(matchupLink)
        self.__processTeam("away")
        self.__processTeam("home")

    def __loadMatchupInBrowser(self, matchupLink):
        cssSelector = "a[href={0}]".format(matchupLink["href"])
        self.browserSession.getScoreboardBase()
        self.browserSession.find_element_by_css_selector(cssSelector).click()

    def __processTeam(self, homeOrAway):
        soup = BeautifulSoup(self.browserSession.page_source, "html.parser")
        teamName = soup.find("td", class_="teamname", id="{0}_big_name".format(homeOrAway))
        if teamName not in [team.name for team in self.scoreboard.teams]:
            team = Team(teamName)
            ScoreboardParser.__createNewTeam(team, soup, homeOrAway)
            self.scoreboard.teams.append(team)

    @staticmethod
    def __createNewTeam(team, soup, homeOrAway):
        activeSoup = soup.find("tbody", id="{0}_active".format(homeOrAway))
        ScoreboardParser.__processPlayers(team, activeSoup, True)
        reserveSoup = soup.find("tbody", id="{0}_reserve".format(homeOrAway))
        ScoreboardParser.__processPlayers(team, reserveSoup, False)

    @staticmethod
    def __processPlayers(team, soup, active):
        activePlayers = soup.find_all("tr", align="left", class_="bg2", height="49", valign="middle")
        [ScoreboardParser.__addPlayerToTeam(playerSoup, team, active) for playerSoup in activePlayers]

    @staticmethod
    def __addPlayerToTeam(activePlayerSoup, team, active):
        cbsId, name, positions = ScoreboardParser.__getPlayerInfo(activePlayerSoup)
        points = ScoreboardParser.__getPlayerPoints(activePlayerSoup)
        team.addPlayer(Player(name, cbsId, positions, points, active))

    @staticmethod
    def __getPlayerInfo(soup):
        tag = soup.find("a.playerLink")
        cbsId = tag["href"][len("/players/playerpage/"):]
        fullName = " ".join(tag["title"].split(" ")[:-2])
        tempPosition = tag["title"].split(" ")[-2]
        if "F" in tempPosition:
            position = tempPosition if tempPosition == "CF" else "OF"
            return cbsId, fullName, [position]
        else:
            return cbsId, fullName, [tempPosition]

    @staticmethod
    def __getPlayerPoints(soup):
        tag = soup.find("a.scoreLink")
        return float(tag.string)
