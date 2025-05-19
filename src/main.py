#!/usr/bin/env python3


import itertools
import operator
import re
import statistics
from collections import OrderedDict, defaultdict
from dataclasses import dataclass, field
from enum import Enum
from itertools import groupby, product
import subprocess
from time import sleep
from types import TracebackType
from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple, TypeVar

import click
from bs4 import BeautifulSoup, Tag  # type: ignore
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.wait import WebDriverWait

LEAGUE_HOME: str = "https://reddit2.baseball.cbssports.com"

DIVISIONS: Dict[str, str] = {
    # AL East
    "Blue Jays": "AL East",
    "Guardians": "AL East",
    "Orioles": "AL East",
    "Rays": "AL East",
    "Red Sox": "AL East",
    "Tigers": "AL East",
    "Yankees": "AL East",
    # AL West
    "Angels": "AL West",
    "Astros": "AL West",
    "Athletics": "AL West",
    "Mariners": "AL West",
    "Rangers": "AL West",
    "Royals": "AL West",
    "Twins": "AL West",
    "White Sox": "AL West",
    # NL East
    "Braves": "NL East",
    "Marlins": "NL East",
    "Mets": "NL East",
    "Nationals": "NL East",
    "Phillies": "NL East",
    "Pirates": "NL East",
    "Reds": "NL East",
    # NL West
    "Brewers": "NL West",
    "Cardinals": "NL West",
    "Cubs": "NL West",
    "Diamondbacks": "NL West",
    "Dodgers": "NL West",
    "Giants": "NL West",
    "Padres": "NL West",
    "Rockies": "NL West",
}

ALL_STAR_POSITIONS: Dict[str, int] = {
    "C": 1,
    "1B": 1,
    "2B": 1,
    "3B": 1,
    "SS": 1,
    "CF": 1,
    "OF": 2,
    "U": 2,
}

NICKNAMES: Dict[int, str] = {
    530362: "Kate Upton",
    1232129: "Big Dick Rick",
    1630093: "DONGcarlo Stanton",
    1762602: 'Chris "Scissors" Sale',
    1794765: 'Matt "Parmalee" Carpenter',
    1805124: "Big Maple",
    1813268: "Khrush .247",
    2000025: "Pineapple",
    2210421: 'Willians "La Tortuga" Astudillo',
}


@dataclass(frozen=True)
class RosteredPlayer:
    name: str
    id: int
    active_points: float
    active_batter: bool
    active_pitcher: bool


@dataclass
class Team:
    name: str
    hitting_points: float = 0
    pitching_points: float = 0
    players: Set[RosteredPlayer] = field(default_factory=set, init=False)
    wins: List[str] = field(default_factory=list, init=False)
    losses: List[str] = field(default_factory=list, init=False)
    ties: List[str] = field(default_factory=list, init=False)

    @property
    def points(self) -> float:
        return self.hitting_points + self.pitching_points

    @property
    def opponents(self) -> List[str]:
        return [*self.losses, *self.ties, *self.wins]

    def add(self, player: RosteredPlayer) -> None:
        self.players.add(player)
        if player.active_batter:
            self.hitting_points += player.active_points
        if player.active_pitcher:
            self.pitching_points += player.active_points

    def __lt__(self, other: "Team") -> bool:
        return (self.points, self.name) < (other.points, other.name)


@dataclass
class ScoringPlayer:
    name: str
    id: int
    points: float
    team: str = field(init=False)


@dataclass
class PointLeaders:
    position: str
    max_scorers: int
    descending: bool
    players: List[ScoringPlayer] = field(default_factory=list, init=False)

    def add(self, player: ScoringPlayer) -> bool:
        if len(self.players) < self.max_scorers:
            self.players.append(player)
            return True

        compare = operator.ge if self.descending else operator.le
        if compare(player.points, self.players[-1].points):
            self.players.append(player)
            return True

        return False


MatchupMode = Enum(
    "MatchupMode", "BLOWOUT CLOSEST STRONGEST_LOSS WEAKEST_WIN LUCKIEST UNLUCKIEST"
)


@dataclass
class Matchup:
    team1: Team
    team2: Team
    teams: Dict[str, Team] = field(compare=False)
    mode: Optional[MatchupMode] = field(compare=False)

    def __post_init__(self) -> None:
        team1, team2 = sorted((self.team1, self.team2), reverse=True)
        self.team1 = team1
        self.team2 = team2

    @property
    def points(self) -> float:
        return self.team1.points - self.team2.points

    def with_mode(self, mode: MatchupMode) -> "Matchup":
        if mode == MatchupMode.LUCKIEST:
            return Matchup(self.team1, self.team1, self.teams, mode)
        elif mode == MatchupMode.UNLUCKIEST:
            return Matchup(self.team2, self.team2, self.teams, mode)
        else:
            return Matchup(self.team1, self.team2, self.teams, mode)

    def __hash__(self) -> int:
        return hash((self.team1.name, self.team2.name))


class MarkdownType(Enum):
    BULLET = "BULLET"
    TABLE = "TABLE"


class WebDriver:
    def __init__(self):
        self.driver: str | None = None

    def __enter__(self) -> "WebDriver":
        subprocess.run("docker compose up --wait", check=True, shell=True)
        self.driver = subprocess.check_output(
            "docker compose port selenium 4444",
            shell=True,
            text=True,
        ).strip()
        return self

    def __exit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        subprocess.check_output("docker compose down", shell=True)
        if value:
            raise value


@click.command()
@click.option("-s", "--scoring-period", type=int, required=True)
@click.option("-u", "--username", type=str, prompt="Your CBS username")
@click.option("-p", "--password", type=str, prompt="Your CBS password")
def generate_summary(scoring_period: int, username: str, password: str) -> None:
    with WebDriver() as _:
        driver_options = Options()
        driver_options.add_argument("--headless=new")
        with Remote(options=driver_options) as browser:
            login(browser, username, password)

            try:
                teams = parse_matchups(browser, scoring_period)
                leaders = parse_point_leaders(browser, scoring_period)
            except Exception as ex:
                print(current_soup(browser).prettify())
                raise ex

    players_by_team = dict(
        (player.id, team.name) for team in teams for player in team.players
    )
    for point_leaders in leaders:
        for player in point_leaders.players:
            player.team = players_by_team.get(player.id, "FA")

    all_stars = dict(
        ((point_leaders.position, point_leaders.descending), point_leaders)
        for point_leaders in leaders
    )

    teams_by_name = dict((team.name, team) for team in teams)
    matchups = set(
        Matchup(team, teams_by_name[opponent], teams_by_name, None)
        for team in teams
        for opponent in team.opponents
    )

    markdown = [
        markdown_section(
            "Top Three Teams of the Week",
            MarkdownType.BULLET,
            top_scorers(teams),
        ),
        markdown_section(
            "Worst Three Teams of the Week",
            MarkdownType.BULLET,
            top_scorers(teams, False),
        ),
        markdown_section(
            "Offensive Powerhouses",
            MarkdownType.BULLET,
            top_scorers(teams, points=lambda t: t.hitting_points),
        ),
        markdown_section(
            "Forgot Their Bats",
            MarkdownType.BULLET,
            top_scorers(teams, descending=False, points=lambda t: t.hitting_points),
        ),
        markdown_section(
            "Pitching Factories",
            MarkdownType.BULLET,
            top_scorers(teams, points=lambda t: t.pitching_points),
        ),
        markdown_section(
            "Burnt Down Factories",
            MarkdownType.BULLET,
            top_scorers(teams, descending=False, points=lambda t: t.pitching_points),
        ),
        markdown_section(
            "Multi-Start Saviors",
            MarkdownType.BULLET,
            top_scorers(all_stars[("2SP", True)].players),
        ),
        markdown_section(
            "1 Start Gods",
            MarkdownType.BULLET,
            top_scorers(all_stars[("1SP", True)].players),
        ),
        markdown_section(
            "No Start Workhorses",
            MarkdownType.BULLET,
            top_scorers(all_stars[("RP", True)].players),
        ),
        markdown_section(
            "Had a Bad Day",
            MarkdownType.BULLET,
            top_scorers(all_stars[("SP", False)].players, descending=False),
        ),
        markdown_section(
            "The Bullpen Disasters",
            MarkdownType.BULLET,
            top_scorers(all_stars[("RP", False)].players, descending=False),
        ),
        markdown_section(
            "All Stars",
            MarkdownType.BULLET,
            all_star_lineup(all_stars.values()),
        ),
        markdown_section(
            "Blowout of the Week",
            MarkdownType.BULLET,
            top_scorers(
                set(matchup.with_mode(MatchupMode.BLOWOUT) for matchup in matchups),
                num_scorers=1,
            ),
        ),
        markdown_section(
            "Closest Matchup of the Week",
            MarkdownType.BULLET,
            top_scorers(
                set(matchup.with_mode(MatchupMode.CLOSEST) for matchup in matchups),
                descending=False,
                num_scorers=1,
            ),
        ),
        markdown_section(
            "Strongest Loss",
            MarkdownType.BULLET,
            top_scorers(
                set(
                    matchup.with_mode(MatchupMode.STRONGEST_LOSS)
                    for matchup in matchups
                    if matchup.points > 0
                ),
                num_scorers=1,
                points=lambda m: m.team2.points,
            ),
        ),
        markdown_section(
            "No Wins for the Effort",
            MarkdownType.BULLET,
            top_scorers(
                set(
                    matchup.with_mode(MatchupMode.UNLUCKIEST)
                    for matchup in matchups
                    if not matchup.team2.wins
                ),
                num_scorers=1,
                points=lambda m: m.team2.points,
            ),
        ),
        markdown_section(
            "Weakest Win",
            MarkdownType.BULLET,
            top_scorers(
                set(
                    matchup.with_mode(MatchupMode.WEAKEST_WIN)
                    for matchup in matchups
                    if matchup.points > 0
                ),
                descending=False,
                num_scorers=1,
                points=lambda m: m.team1.points,
            ),
        ),
        markdown_section(
            "Dirty Cheater",
            MarkdownType.BULLET,
            top_scorers(
                set(
                    matchup.with_mode(MatchupMode.LUCKIEST)
                    for matchup in matchups
                    if not matchup.team1.losses
                ),
                descending=False,
                num_scorers=1,
                points=lambda m: m.team1.points,
            ),
        ),
        markdown_section("Division Stats", MarkdownType.TABLE, division_table(teams)),
    ]

    print("\n\n".join(markdown))


def login(browser: Remote, username: str, password: str) -> None:
    browser.get(LEAGUE_HOME)
    WebDriverWait(browser, 10).until(expect.url_contains("/login"))

    username_field = browser.find_element(By.NAME, "email")
    username_field.clear()
    username_field.send_keys(username)

    password_field = browser.find_element(By.NAME, "password")
    password_field.clear()
    password_field.send_keys(password)

    browser.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    WebDriverWait(browser, 10).until(expect.url_contains(LEAGUE_HOME))
    browser.refresh()


def parse_matchups(browser: Remote, scoring_period: int) -> List[Team]:
    browser.get(f"{LEAGUE_HOME}/scoring/completed/{scoring_period}")
    teams: Dict[str, Team] = {}
    for tag in browser.find_elements(By.CSS_SELECTOR, "table[id^='matchup_hilite_']"):
        browser.find_element(By.CSS_SELECTOR, f"table#{tag.get_property('id')}").click()

        matchup_soup = current_soup(browser)
        home = load_team("home", matchup_soup, teams)
        away = load_team("away", matchup_soup, teams)

        if home and away:
            if home.points < away.points:
                home.losses.append(away.name)
                away.wins.append(home.name)
            elif home.points > away.points:
                home.wins.append(away.name)
                away.losses.append(home.name)
            else:
                home.ties.append(away.name)
                away.ties.append(home.name)

    return [teams[name] for name in teams]


def current_soup(browser: Remote) -> BeautifulSoup:
    return BeautifulSoup(browser.page_source, "html.parser")


def load_team(
    home_or_away: str, soup: BeautifulSoup, teams: Dict[str, Team]
) -> Optional[Team]:
    team_name = soup.select_one(f".teamname #{home_or_away}_big_name").string.strip()
    if team_name not in DIVISIONS:
        return None
    if team_name in teams:
        return teams[team_name]

    team = Team(team_name)
    teams[team.name] = team

    player_tags = re.compile(r"^player_(active|reserve)_\d+_\d+$")
    for tag in soup.select_one(f"#{home_or_away}_team_roster").find_all(id=player_tags):
        player_tag = tag.parent

        active_batter = False
        active_pitcher = False
        active_points = 0.0
        if active_points_tag := player_tag.select_one(
            "a.scoreLink[id^=score_total_active]"
        ):
            active_points = float(active_points_tag.string.strip())
            active_pitcher = (
                "P" in player_tag.select_one("a.playerLink").parent.div.string
            )
            active_batter = not active_pitcher

        name, id_number = player_name_and_id(player_tag, "title")
        team.add(
            RosteredPlayer(
                name, id_number, active_points, active_batter, active_pitcher
            )
        )

    return team


def player_name_and_id(soup: Tag, name_tag: str) -> Tuple[str, int]:
    try:
        info_tag = soup.select_one("a.playerLink")
        name_match = re.match(r"^\s*(.+)\s+[A-Z1-3]+\s+[A-Z]+\s*$", info_tag[name_tag])
        id_number_match = re.match(r"^/players/playerpage/(\d+).*$", info_tag["href"])

        if not id_number_match:
            raise AttributeError("No id number found")

        return (
            name_match.group(1) if name_match else info_tag.text.strip(),
            int(id_number_match.group(1)),
        )
    except AttributeError as ex:
        raise AttributeError(
            f"Failed to read player from '{name_tag}'. Soup:\n{soup.prettify()}\n"
        ) from ex


def parse_point_leaders(browser: Remote, scoring_period: int) -> List[PointLeaders]:
    leaders = []

    num_all_stars = sum(ALL_STAR_POSITIONS.values())
    for position in ALL_STAR_POSITIONS:
        soups = point_leader_soups(browser, scoring_period, position)
        leaders.append(point_leaders(soups, position, num_all_stars, True))

    soups = point_leader_soups(browser, scoring_period, "SP:RP")
    for position in ["2SP", "1SP", "RP"]:
        leaders.append(point_leaders(soups, position, 3, True))
    for position in ["SP", "RP"]:
        leaders.append(point_leaders(soups, position, 3, False))

    return leaders


def point_leader_soups(
    browser: Remote, scoring_period: int, position: str
) -> List[Tag]:
    browser.get(
        f"{LEAGUE_HOME}/stats/data-stats-report/all"
        f":{position}/period-{scoring_period}/standard/stats?print_rows=9999"
    )
    return current_soup(browser).select("tbody > tr[valign='top']")


def point_leaders(
    soups: List[Tag], position: str, max_scorers: int, descending: bool
) -> PointLeaders:
    point_leaders = PointLeaders(position, max_scorers, descending)

    for soup in soups if descending else reversed(soups):
        if "P" in position:
            columns = soup.select("tr > td[align='right']")
            games = int(columns[1].string.strip())
            games_started = int(columns[2].string.strip())

            if games == 0:
                continue
            if position == "2SP" and games_started < 2:
                continue
            if position == "1SP" and games_started != 1:
                continue
            if "SP" in position and games_started == 0:
                continue
            if position == "RP" and games_started > 0:
                continue

        name, id_number = player_name_and_id(soup, "aria-label")
        points = float(soup.select_one("tr > td.bold").string.strip())
        if not point_leaders.add(ScoringPlayer(name, id_number, points)):
            break

    return point_leaders


def markdown_section(header: str, type: MarkdownType, lines: List[str]) -> str:
    if not lines:
        return ""
    delimiter = "\n"
    if type == MarkdownType.BULLET:
        delimiter += "* "
    return f"### {header}{delimiter}{delimiter.join(lines)}"


T = TypeVar("T", Matchup, ScoringPlayer, Team)


def top_scorers(
    scorers: Iterable[T],
    descending: bool = True,
    num_scorers: int = 3,
    points: Callable[[T], float] = lambda s: s.points,
) -> List[str]:
    lines = []

    index_adjustment = 1
    for index, (group_points, group) in enumerate(
        ranked_scorers(scorers, descending, num_scorers, points)
    ):
        for scorer in group:
            scorer_line = scorer_string(scorer, group_points)
            if len(group) > 1:
                rank = rank_string(index + index_adjustment)
                scorer_line = f"{scorer_line} (tied for {rank})"
            lines.append(scorer_line)
        index_adjustment += len(group) - 1

    return lines


def ranked_scorers(
    scorers: Iterable[T],
    descending: bool,
    num_scorers: int,
    points: Callable[[T], float],
) -> List[Tuple[float, List[T]]]:
    return sorted(
        [
            (group_points, list(group))
            for group_points, group in groupby(sorted(scorers, key=points), key=points)
        ],
        reverse=descending,
    )[:num_scorers]


def scorer_string(scorer: T, points: float) -> str:
    def team_string(team: Team) -> str:
        return scorer_string(team, team.points)

    if isinstance(scorer, Team):
        return f"{scorer.name}, {points_string(points)}"
    elif isinstance(scorer, ScoringPlayer):
        return f"{scorer.name}, {scorer.team}, {points_string(points)}"
    elif scorer.mode in [MatchupMode.LUCKIEST, MatchupMode.UNLUCKIEST]:
        opponents = "; and ".join(
            [
                team_string(scorer.teams[opponent])
                for opponent in sorted(
                    scorer.team1.opponents, key=lambda o: scorer.teams[o], reverse=True
                )
            ]
        )
        join_string = "over" if scorer.mode == MatchupMode.LUCKIEST else "lost to"
        return f"{team_string(scorer.team1)}: {join_string} {opponents}"
    elif scorer.points == 0:
        return (
            f"Tied at {points_string(scorer.team1.points)}:"
            f" {scorer.team1.name} and {scorer.team2.name}"
        )
    elif scorer.mode == MatchupMode.WEAKEST_WIN:
        return f"{team_string(scorer.team1)}: over {team_string(scorer.team2)}"
    elif scorer.mode == MatchupMode.STRONGEST_LOSS:
        return f"{team_string(scorer.team2)}: lost to {team_string(scorer.team1)}"
    else:
        return (
            f"By {points_string(points)}:"
            f" {team_string(scorer.team1)} over"
            f" {team_string(scorer.team2)}"
        )


def rank_string(rank: int) -> str:
    if rank < 1:
        raise ValueError(f"{rank}: cannot count lower than 1")
    if rank > 10 and str(rank)[-2] == "1":
        return f"{rank}th"
    if str(rank)[-1] == "1":
        return f"{rank}st"
    if str(rank)[-1] == "2":
        return f"{rank}nd"
    if str(rank)[-1] == "3":
        return f"{rank}rd"
    else:
        return f"{rank}th"


def points_string(points: float) -> str:
    return f"{points} point" if points == 1 else f"{points} points"


def all_star_lineup(all_stars: Iterable[PointLeaders]) -> List[str]:
    scorers = {}
    scorer_positions = defaultdict(set)
    position_scorers = defaultdict(set)
    lineup_candidates: Dict[str, List[int]] = defaultdict(list)

    for leaders in all_stars:
        if leaders.position not in ALL_STAR_POSITIONS:
            continue

        for scorer in leaders.players:
            scorers[scorer.id] = scorer
            scorer_positions[scorer.id].add(leaders.position)
            position_scorers[leaders.position].add(scorer.id)

    def add_new_scorers(base_scorers: Iterable[int], number: int) -> None:
        players = [
            scorers[scorer]
            for scorer in set(base_scorers)
            if scorer not in set(itertools.chain(*lineup_candidates.values()))
        ]

        for _, group in ranked_scorers(players, True, number, lambda s: s.points):
            for scorer in group:
                for position in scorer_positions[scorer.id]:
                    lineup_candidates[position].append(scorer.id)

    add_new_scorers(scorers.keys(), 10)

    while lacking_positions := [
        position
        for position, count in ALL_STAR_POSITIONS.items()
        if len(lineup_candidates[position]) < count
    ]:
        lacking_position_scorers = [
            scorer
            for position in lacking_positions
            for scorer in position_scorers[position]
        ]
        add_new_scorers(lacking_position_scorers, 1)

    lineup_options: List[List[int]] = [
        list(lineup_candidates[position])
        for position, count in ALL_STAR_POSITIONS.items()
        for _ in range(0, count)
    ]

    points = 0.0
    lineups = []
    known_lineups = set()
    for lineup in product(*lineup_options):
        if len(lineup_set := frozenset(lineup)) != len(lineup):
            continue
        if lineup_set in known_lineups:
            continue
        known_lineups.add(lineup_set)

        lineup_points: float = sum(scorers[scorer].points for scorer in lineup)
        if lineup_points < points:
            continue
        elif lineup_points == points:
            lineups.append(lineup)
        else:
            points = lineup_points
            lineups = [lineup]

    positions = [
        position_string
        for position, count in ALL_STAR_POSITIONS.items()
        for position_string in [position] * count
    ]

    return [
        f"{position}: {scorer_string(scorers[player], scorers[player].points)}"
        for lineup in lineups
        for position, player in zip(positions, lineup)
    ]


def division_table(teams: List[Team]) -> List[str]:
    divisions: Dict[str, List[Team]] = OrderedDict()
    for team in teams:
        divisions.setdefault(DIVISIONS[team.name], []).append(team)

    if any(len(division) < 2 for division in divisions.values()):
        return []

    scores = [
        [team.points for team in division_teams]
        for division_teams in list(divisions.values()) + [teams]
    ]

    records = [
        (
            len([r for t in div_teams for r in t.wins if DIVISIONS[r] != division]),
            len([r for t in div_teams for r in t.losses if DIVISIONS[r] != division]),
            len([r for t in div_teams for r in t.ties if DIVISIONS[r] != division]),
        )
        for division, div_teams in divisions.items()
    ]


    table = [
        [f"**{name}**" for name in ["Division"] + list(divisions.keys()) + ["League"]],
        [":---:"] * (len(divisions) + 2),
        ["**Points**"] + [str(sum(points)) for points in scores],
        ["**Points/Team**"] + [str(round(statistics.mean(s), 1)) for s in scores],
        ["**Std. Deviation**"] + [str(round(statistics.stdev(s), 1)) for s in scores],
        ["**Record**"]
        + [
            f"{wins}-{losses}-{ties}".removesuffix("-0")
            for wins, losses, ties in records
        ]
        + [""],
    ]
    return [f"| {' | '.join(row)} |" for row in table]


if __name__ == "__main__":
    generate_summary()
