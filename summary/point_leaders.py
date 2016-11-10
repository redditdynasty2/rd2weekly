from collections import namedtuple
from itertools import groupby

import matchup_parser
import operator


PositionPoints = namedtuple(
        "PositionPoints",
        ["position", "num_scorers", "has_worst"])


PointLeader = namedtuple(
        "PointLeader",
        ["name", "cbs_id_number", "team_name", "points"])


def parse_points_leaders(period, teams, browser):
    point_gathering_settings = [
            PositionPoints(position, 3, True)
            if position == "SP:RP"
            else PositionPoints(position, 10, False)
            for position
            in ["C", "1B", "2B", "3B", "SS", "CF", "OF", "U", "SP:RP"]
    ]

    # We need the mapping of player id to team name because the loaded player
    # rows only include the current fantasy the team is playing for. So if
    # there was a trade or waiver claim or drop that processed in the middle of
    # the week, the player rows would not show the correct team for the weekly
    # summary.
    players_to_team = dict((
            (player.cbs_id_number, team.name) 
            for team in teams
            for player in team.players
    ))

    leaders = PointsLeaders.create_with_settings(
            period,
            point_gathering_settings,
            players_to_team,
            browser)
    return leaders.top_scorers, leaders.worst_scorers


class PointsLeaders:

    def __init__(self, players_to_team):
        self._players_to_team = players_to_team
        self.top_scorers = {}
        self.worst_scorers = {}

    @classmethod
    def create_with_settings(cls,
                             period,
                             point_gathering_settings,
                             players_to_team,
                             browser):
        leaders = cls(players_to_team)
        [
                leaders._load_scorers_with_settings(settings, period, browser)
                for settings in point_gathering_settings
        ]
        return leaders

    def _load_scorers_with_settings(self, settings, period, browser):
        position = settings.position
        num_scorers = settings.num_scorers

        table_row_soups = browser.get_position_leader_rows_soup(
                position,
                period)

        self._load_top_scorers(table_row_soups, position, num_scorers)
        if settings.has_worst:
            self._load_worst_scorers(table_row_soups, position, num_scorers)

    def _load_top_scorers(self, rows, position, num_scorers):
        def get_scorers_for_position(fantasy_position):
            return self._get_scorers_by_position(
                    rows,
                    fantasy_position,
                    num_scorers,
                    operator.lt)

        positions = ["1SP", "2SP", "RP"] if position == "SP:RP" else [position]
        self.top_scorers.update(dict((
                (scorer_position, get_scorers_for_position(scorer_position))
                for scorer_position
                in positions
        )))

    def _get_scorers_by_position(self,
                                 rows,
                                 position,
                                 num_scorers,
                                 should_exclude):
        scorers = []
        for row in rows:
            player = self._read_row_as_point_leader(row, position)
            if not player:
                continue

            if len(scorers) >= num_scorers:
                if should_exclude(player.points, scorers[-1].points):
                    break

            scorers.append(player)

        return [
                list(group)
                for points, group
                in groupby(scorers, key=lambda player: player.points)
        ]

    def _read_row_as_point_leader(self, row_soup, position):
        if "P" in position:
            column_soups = row_soup.select("tr > td[align='right']")
            games_appeared = int(column_soups[1].string.strip())
            games_started = int(column_soups[2].string.strip())
            
            if games_appeared == 0:
                return None
            if position == "SP" and games_started == 0:
                return None
            if position == "2SP" and games_started < 2:
                return None
            if position == "1SP" and games_started != 1:
                return None
            if position == "RP" and games_started != 0:
                return None

        name, cbs_id_number = matchup_parser.parse_player_name_and_id(
                row_soup,
                "aria-label")
        points = float(row_soup.select_one("tr > td.bold").string.strip())
        team_name = self._players_to_team.get(cbs_id_number, "FA")
        return PointLeader(name, cbs_id_number, team_name, points)

    def _load_worst_scorers(self, rows, position, num_scorers):
        reversed_rows = rows[::-1]
        def get_scorers_for_position(fantasy_position):
            return self._get_scorers_by_position(
                    reversed_rows,
                    fantasy_position,
                    num_scorers,
                    operator.gt)

        positions = ["SP", "RP"] if position == "SP:RP" else [position]
        self.worst_scorers.update(dict((
                (scorer_position, get_scorers_for_position(scorer_position))
                for scorer_position
                in positions
        )))

