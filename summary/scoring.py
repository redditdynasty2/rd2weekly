from collections import namedtuple
from itertools import groupby


Player = namedtuple("Player", "name cbs_id_number in_lineup active_pitcher")


class Team:

    def __init__(self, name, division):
        self.name = name
        self.division = division
        self.players = []
        self.wins = []
        self.losses = []
        self.ties = []
        self.hitting_points = 0
        self.pitching_points = 0

    @staticmethod
    def update_records(away_team, home_team):
        if away_team.total_points > home_team.total_points:
            away_team.wins.append(home_team.name)
            home_team.losses.append(away_team.name)
        elif away_team.total_points < home_team.total_points:
            away_team.losses.append(home_team.name)
            home_team.wins.append(away_team.name)
        else:
            away_team.ties.append(home_team.name)
            home_team.ties.append(away_team.name)

    @staticmethod
    def is_blank_team_name(team_name):
        return team_name in ["TBA", "BYE", "FA"]

    @property
    def total_points(self):
        return self.hitting_points + self.pitching_points

    def __eq__(self, other):
        return (
                isinstance(self, type(other))
                and self.name == other.name
                and self.division == other.division
        )

    def __hash__(self):
        return hash((self.name, self.division))

