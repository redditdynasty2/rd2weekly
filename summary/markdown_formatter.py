from collections import namedtuple
from itertools import groupby

import scoring
import statistics


DivisionStats = namedtuple(
        "DivisionStats",
        ["name", "points", "average", "stddev", "record"])


def get_points_string(points):
    return "point" if points == 1 else "points"


def get_rank_string(rank):
    """
        Because we only work with numbers less than 10, we only have to write
        out casing for the simplest of numbers.
    """
    return (
            "1st" if rank == 1
            else "2nd" if rank == 2
            else "3rd" if rank == 3
            else f"{rank}th"
    )


def get_markdown_for_section(header, bullets):
    """
        Just to make things easier, all headers are displayed at '###' level
        and all bullets are displayed in a non-numbered list format, but
        iteration order is preserved.
    """
    markdown_string = f"### {header}"
    bullet_string = "\n\n  * ".join(bullets)
    return f"{markdown_string}\n\n  * {bullet_string}"


def get_name_and_points_string(name, points):
    return f"{name}, {points} {get_points_string(points)}"


def get_name_team_and_points_string(name, team, points):
    return f"{name}, {team}, {points} {get_points_string(points)}"


class MarkdownFormatter:

    TEAM_SECTION_HEADERS = [
            "Top Three Teams of the Week",
            "Worst Three Teams of the Week",
            "Offensive Powerhouses",
            "Forgot Their Bats",
            "Pitching Factories",
            "Burned Down Factories",
    ]

    PITCHING_HEADERS = [
            "Multi-Start Saviors",
            "1 Start Gods",
            "No Start Workhorses",
            "Had a Bad Day",
            "The Bullpen Disasters",
    ]

    MATCHUP_HEADERS = [
            "Blowout of the Week",
            "Closest Matchup of the Week",
            "Strongest Loss",
            "No Wins for the Effort",
            "Weakest Win",
            "Dirty Cheater",
    ]

    def __init__(self, 
                 teams,
                 teams_to_divisions,
                 top_performers,
                 worst_performers,
                 nicknames):
        self._teams = teams
        self._teams_to_divisions = teams_to_divisions
        self._top_performers = top_performers
        self._worst_performers = worst_performers
        self._nicknames = nicknames

    @classmethod
    def get_markdown_weekly_summary(cls,
                                    teams,
                                    teams_to_divisions,
                                    top_performers,
                                    worst_performers,
                                    nicknames):
        formatter = cls(
                teams,
                teams_to_divisions,
                top_performers,
                worst_performers,
                nicknames)

        sections = []
        sections.extend(formatter._get_team_sections())
        sections.append(formatter._get_all_stars())
        sections.extend(formatter._get_pitcher_sections())
        sections.extend(formatter._get_matchup_sections())
        sections.append(formatter._get_division_table())
        return "\n\n".join(sections)

    def _get_team_sections(self):

        def sort_teams(section):
            if section in [
                    "Top Three Teams of the Week",
                    "Worst Three Teams of the Week"]:
                sort_key = lambda team: team.total_points
                reverse_sort = section == "Top Three Teams of the Week"
            elif section in ["Offensive Powerhouses", "Forgot Their Bats"]:
                sort_key = lambda team: team.hitting_points
                reverse_sort = section == "Offensive Powerhouses"
            elif section in ["Pitching Factories", "Burned Down Factories"]:
                sort_key = lambda team: team.pitching_points
                reverse_sort = section == "Pitching Factories"
            else:
                raise Exception((
                        f"Unrecognized team section header {section}."
                ))

            sorted_teams = sorted(
                    self._teams.values(),
                    key=sort_key,
                    reverse=reverse_sort)
            return [
                    (points, list(map(lambda team: team.name, group)))
                    for points, group in groupby(sorted_teams, key=sort_key)
            ]

        def get_team_bullet_string(team_name, points, rank, is_tied):
            team_string = get_name_and_points_string(team_name, points)
            return (
                    f"{team_string} (tied for {get_rank_string(rank)})"
                    if is_tied
                    else team_string
            )

        def get_team_section_bullets(section):
            index_adjustment = 1
            bullets = []
            for index, (points, teams) in enumerate(sort_teams(section)):
                for team in teams:
                    bullets.append(get_team_bullet_string(
                            team,
                            points,
                            index + index_adjustment,
                            len(teams) > 1))
                if len(bullets) >= 3:
                    break
                index_adjustment += len(teams) - 1
            return bullets

        return [
                get_markdown_for_section(
                        section,
                        get_team_section_bullets(section))
                for section in self.TEAM_SECTION_HEADERS
        ]

    def _get_all_stars(self):
        return ""

    def _get_pitcher_sections(self):

        def get_pitcher_bullet_string(pitcher, rank, is_tied):
            pitcher_name = self._nicknames.get(str(pitcher.name), pitcher.name)
            pitcher_string = get_name_team_and_points_string(
                    pitcher_name,
                    pitcher.team_name,
                    pitcher.points)
            
            if pitcher.team_name in self._teams:
                team_players = self._teams[pitcher.team_name].players
                was_active = any(
                        team_pitcher.active_pitcher
                        for team_pitcher in team_players
                        if pitcher.cbs_id_number == team_pitcher.cbs_id_number)
                if not was_active:
                    pitcher_string = f"{pitcher_string} (from the bench)"

            return (
                    f"{pitcher_string} (tied for {get_rank_string(rank)})"
                    if is_tied
                    else pitcher_string
            )

        def get_pitcher_section_bullets(section):
            if section == "Multi-Start Saviors":
                sorted_pitchers = self._top_performers["2SP"]
            elif section == "1 Start Gods":
                sorted_pitchers = self._top_performers["1SP"]
            elif section == "No Start Workhorses":
                sorted_pitchers = self._top_performers["RP"]
            elif section == "Had a Bad Day":
                sorted_pitchers = self._worst_performers["SP"]
            elif section == "The Bullpen Disasters":
                sorted_pitchers = self._worst_performers["RP"]

            index_adjustment = 1
            bullets = []
            for index, pitchers in enumerate(sorted_pitchers):
                for pitcher in pitchers:
                    bullets.append(get_pitcher_bullet_string(
                            pitcher,
                            index + index_adjustment,
                            len(pitchers) > 1))
                if len(bullets) >= 3:
                    break
                index_adjustment += len(pitchers) - 1
            return bullets

        return [
                get_markdown_for_section(
                        section,
                        get_pitcher_section_bullets(section))
                for section in self.PITCHING_HEADERS
        ]

    def _get_matchup_sections(self):
        winners = {}
        losers = {}
        ties = {}
        for team in self._teams.values():
            [
                    winners.setdefault(team.name, []).append(loser)
                    for loser in team.wins
            ]
            [
                    losers.setdefault(team.name, []).append(winner)
                    for winner in team.losses
            ]
            [
                    ties.setdefault(team.name, []).append(other_team)
                    for other_team in team.ties
                    if team.name not in ties.get(other_team, [])
            ]

        def get_team_points(team):
            return self._teams[team].total_points

        def get_multidict_entries(multidict):
            return [
                    (team, other_team)
                    for team, other_teams in multidict.items()
                    for other_team in other_teams
            ]

        def sort_matchups(section):
            reverse_sort = section in [
                    "Blowout of the Week",
                    "Strongest Loss",
                    "No Wins for the Effort",
            ]

            def filter_key(entry):
                team, other_team = entry
                if section == "Strongest Loss":
                    return other_team in losers.get(team, [])
                elif section == "No Wins for the Effort":
                    return team not in winners
                elif section == "Dirty Cheater":
                    return team not in losers
                else:
                    return other_team in winners.get(team, [])

            def sort_key(entry):
                team, other_team = entry
                if section in [
                        "Blowout of the Week",
                        "Closest Matchup of the Week"]:
                    return get_team_points(team) - get_team_points(other_team)
                else:
                    return get_team_points(team)

            if section == "Strongest Loss":
                entries = get_multidict_entries(losers)
            elif section == "No Wins for the Effort":
                entries = (
                        get_multidict_entries(losers)
                        + get_multidict_entries(ties)
                )
            elif section == "Dirty Cheater":
                entries = (
                        get_multidict_entries(winners)
                        + get_multidict_entries(ties)
                )
            else:
                entries = get_multidict_entries(winners)

            sorted_matchups = sorted(
                    filter(filter_key, entries),
                    key=sort_key,
                    reverse=reverse_sort)
            return [
                    list(group)
                    for points, group
                    in groupby(sorted_matchups, key=sort_key)
            ]

        def get_matchup_points_string(section, team, other_team):
            points = get_team_points(team)
            team_string = get_name_and_points_string(team, points)

            other_points = get_team_points(other_team)
            other_team_string = get_name_and_points_string(
                    other_team,
                    other_points)

            point_diff = points - other_points
            if point_diff < 0:
                point_diff = abs(point_diff)
                return (
                        f"By {point_diff} {get_points_string(point_diff)}:"
                        f" {team_string} to {other_team_string}"
                )
            elif point_diff > 0:
                return (
                        f"By {point_diff} {get_points_string(point_diff)}:"
                        f" {team_string} over {other_team_string}"
                )
            else:
                return f"{team_string} tied with {other_team_string}"

        def get_matchup_section_bullets(section):
            return [
                    get_matchup_points_string(section, team, other_team)
                    for team, other_team in sort_matchups(section)[0]
            ]

        return [
                get_markdown_for_section(
                        section,
                        get_matchup_section_bullets(section))
                for section in self.MATCHUP_HEADERS
        ]

    def _get_division_table(self):

        def get_division_stats(division_name, teams, use_record=True):
            scores = list(map(lambda team: team.total_points, teams))
            wins = sum(map(lambda team: len(team.wins), teams), 0)
            losses = sum(map(lambda team: len(team.losses), teams), 0)
            ties = sum(map(lambda team: len(team.ties), teams), 0)
            record_string = (
                    "" if not use_record
                    else f"{wins}-{losses}" if ties == 0
                    else f"{wins}-{losses}-{ties}"
            )
            return DivisionStats(
                    division_name,
                    sum(scores, 0),
                    round(statistics.mean(scores), 1),
                    round(statistics.stdev(scores), 1),
                    record_string)

        def get_all_division_stats():
            sort_key = lambda team: team.division
            all_teams = self._teams.values()
            division_stats = [
                    DivisionStats(
                            "Division",
                            "Points",
                            "Points/Team",
                            "Std. Dev.",
                            "Record")
            ]
            division_stats.extend(
                    get_division_stats(division, list(teams))
                    for division, teams
                    in groupby(
                            sorted(all_teams, key=sort_key),
                            key=sort_key))
            division_stats.append(get_division_stats("League", all_teams))
            return division_stats

        markdown_string = "### Division Stats\n"
        for index, entries in enumerate(list(zip(*get_all_division_stats()))):
            columns = [
                    f"**{entry}**" if index == 0 else f"{entry}"
                    for entry in entries
            ]
            markdown_string = f"{markdown_string}\n| {' | '.join(columns)} |"
            if index == 0:
                alignment = " | ".join(len(columns) * [":---:"])
                markdown_string = f"{markdown_string}\n| {alignment} |"

        return markdown_string

