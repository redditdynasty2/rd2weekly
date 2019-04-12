from collections import namedtuple
from itertools import groupby
from multidict import MultiDict

import abc
import statistics


def get_summary_string(teams, top_performers, worst_performers, nicknames):
    formatters = [
            TeamSectionFormatter(teams),
            PitcherSectionFormatter(
                    teams,
                    top_performers,
                    worst_performers,
                    nicknames),
            AllStarFormatter(),
            MatchupSectionFormatter(teams),
            DivisionTableFormatter(teams)
    ]
    return "\n\n".join(
            section
            for formatter in formatters
            for section in formatter.markdown())


def get_points_string(points):
    return f"{points} point" if points == 1 else f"{points} points"


def get_tied_at_rank_string(rank):
    """
        Because we only work with numbers less than 10, we only have to write
        out casing for the simplest of numbers.
    """
    return (
            "(tied for 1st)" if rank == 1
            else "(tied for 2nd)" if rank == 2
            else "(tied for 3rd)" if rank == 3
            else f"(tied for {rank}th)"
    )


def markdown_for_section(header, bullets):
    """
        Just to make things easier, all headers are displayed at '###' level
        and all bullets are displayed in a non-numbered list format, but
        iteration order is preserved.
    """
    markdown_string = f"### {header}"
    bullet_string = "\n\n  * ".join(bullets)
    return f"{markdown_string}\n\n  * {bullet_string}"


def team_string(name, points):
    return f"{name}, {get_points_string(points)}"


def get_name_team_and_points_string(name, team, points):
    return f"{name}, {team}, {get_points_string(points)}"


class AbstractThreeBulletFormatter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def sort_scorers(self, section):
        raise Exception((
                f"{self.__class__.__name__} has not implemented this method."
        ))

    @abc.abstractmethod
    def scorer_bullet_string(self, scorer, points):
        raise Exception((
                f"{self.__class__.__name__} has not implemented this method."
        ))

    @abc.abstractmethod
    def sections(self):
        raise Exception((
                f"{self.__class__.__name__} has not implemented this method."
        ))

    def markdown(self):

        def section_markdown(section):
            return markdown_for_section(
                    section,
                    self.section_bullets(section))

        return list(map(section_markdown, self.sections()))

    def section_bullets(self, section):
        index_adjustment = 1
        bullets = []

        for index, (points, scorers) in enumerate(self.sort_scorers(section)):
            for scorer in scorers:
                base_string = self.scorer_bullet_string(scorer, points)
                rank = index + index_adjustment
                bullets.append((
                        f"{base_string} {get_rank_string(rank)}"
                        if len(scorers) > 1
                        else base_string
                ))

            if len(bullets) >= 3:
                break
            index_adjustment += len(scorers) - 1

        return bullets


class TeamSectionFormatter(AbstractThreeBulletFormatter):

    TEAM_SECTION_HEADERS = [
            "Top Three Teams of the Week",
            "Worst Three Teams of the Week",
            "Offensive Powerhouses",
            "Forgot Their Bats",
            "Pitching Factories",
            "Burned Down Factories",
    ]

    def __init__(self, teams):
        self._teams = teams

    def sort_scorers(self, section):
        reverse_sort = section in [
                "Top Three Teams of the Week",
                "Offensive Powerhouses",
                "Pitching Factories",
        ]

        if section in ["Offensive Powerhouses", "Forgot Their Bats"]:
            sort_key = lambda team: team.hitting_points
        elif section in ["Pitching Factories", "Burned Down Factories"]:
            sort_key = lambda team: team.pitching_points
        else:
            sort_key = lambda team: team.total_points

        sorted_teams = sorted(
                self._teams.values(),
                key=sort_key,
                reverse=reverse_sort)
        return [
                (points, list(teams))
                for points, teams in groupby(sorted_teams, key=sort_key)
        ]

    def scorer_bullet_string(self, team, points):
        return team_string(team.name, points)

    def sections(self):
        return self.TEAM_SECTION_HEADERS


class PitcherSectionFormatter(AbstractThreeBulletFormatter):

    PITCHING_HEADERS = [
            "Multi-Start Saviors",
            "1 Start Gods",
            "No Start Workhorses",
            "Had a Bad Day",
            "The Bullpen Disasters",
    ]

    def __init__(self, teams, top_performers, worst_performers, nicknames):
        self._teams = teams
        self._top_performers = top_performers
        self._worst_performers = worst_performers
        self._nicknames = nicknames

    def sort_scorers(self, section):

        def get_scorer_entries(scorers):
            return [
                    (scorers_at_rank[0].points, scorers_at_rank)
                    for scorers_at_rank in scorers
            ]

        if section == "Multi-Start Saviors":
            return get_scorer_entries(self._top_performers["2SP"])
        elif section == "1 Start Gods":
            return get_scorer_entries(self._top_performers["1SP"])
        elif section == "No Start Workhorses":
            return get_scorer_entries(self._top_performers["RP"])
        elif section == "Had a Bad Day":
            return get_scorer_entries(self._worst_performers["SP"])
        elif section == "The Bullpen Disasters":
            return get_scorer_entries(self._worst_performers["RP"])
        raise Exception(f"Unrecognized pitcher section '{section}'")

    def scorer_bullet_string(self, pitcher, points):
        base_string = get_name_team_and_points_string(
                self._nicknames.get(str(pitcher.cbs_id_number), pitcher.name),
                pitcher.team_name,
                pitcher.points)

        if pitcher.team_name in self._teams:
            was_active = any(
                    team_pitcher.active_pitcher
                    for team_pitcher in self._teams[pitcher.team_name].players
                    if pitcher.cbs_id_number == team_pitcher.cbs_id_number)
            if not was_active:
                return f"{base_string} (from the bench)"

        return base_string

    def sections(self):
        return self.PITCHING_HEADERS


class AllStarFormatter:

    def markdown(self):
        return []


class MatchupSectionFormatter:

    MATCHUP_HEADERS = [
            "Blowout of the Week",
            "Closest Matchup of the Week",
            "Strongest Loss",
            "No Wins for the Effort",
            "Weakest Win",
            "Dirty Cheater",
    ]

    def __init__(self, teams):
        self._teams = teams
        self._winners = MultiDict()
        self._losers = MultiDict()
        self._ties = MultiDict()
        for team in teams.values():
            [self._winners.add(team.name, loser) for loser in team.wins]
            [self._losers.add(team.name, winner) for winner in team.losses]
            [self._ties.add(team.name, other_team) for other_team in team.ties]

    def markdown(self):

        def section_markdown(section):
            sorted_matchups = self._sort_matchups(section)[0]
            bullets = (
                    self._comparison_matchup_bullets(section, *sorted_matchups)
                    if section in [
                            "Blowout of the Week",
                            "Closest Matchup of the Week",
                    ]
                    else self._multi_matchup_bullets(section, *sorted_matchups)
            )
            return markdown_for_section(section, bullets)

        return list(map(section_markdown, self.MATCHUP_HEADERS))

    def _sort_matchups(self, section):

        def filter_key(matchup_entry):
            primary_team, opponent = matchup_entry
            if section == "Strongest Loss":
                return opponent in self._losers.getall(primary_team, [])
            elif section == "No Wins for the Effort":
                return primary_team not in self._winners
            elif section == "Dirty Cheater":
                return primary_team not in self._losers
            else:
                return opponent in self._winners.getall(primary_team, [])

        def groupby_key(matchup_entry):
            primary_team, opponent = matchup_entry
            primary_points = self._team_points(primary_team)
            opponent_points = self._team_points(opponent)
            if section in [
                    "Blowout of the Week",
                    "Closest Matchup of the Week"]:
                return primary_points - opponent_points
            else:
                return primary_points

        def sort_key(matchup_entry):
            primary_team, opponent = matchup_entry
            return (
                    groupby_key(matchup_entry),
                    self._team_points(primary_team),
                    self._team_points(opponent),
            )

        if section == "Strongest Loss":
            entries = self._losers
        elif section == "No Wins for the Effort":
            entries = MultiDict(self._losers, **self._ties)
        elif section in ["Closest Matchup", "Dirty Cheater"]:
            entries = MultiDict(self._winners, **self._ties)
        else:
            entries = self._winners

        sorted_matchups = sorted(
                filter(filter_key, entries.items()),
                key=sort_key,
                reverse=self._reverse_sort(section))
        return [
                (points, list(group))
                for points, group in groupby(sorted_matchups, key=groupby_key)
        ]

    def _team_points(self, team):
        return self._teams[team].total_points

    @staticmethod
    def _reverse_sort(section):
        return section in [
                "Blowout of the Week",
                "Strongest Loss",
                "No Wins for the Effor",
        ]

    def _comparison_matchup_bullets(self, section, points, matchups):

        def comparison_matchup_string(matchup_entry):
            primary_team, opponent = matchup_entry

            primary_points = self._team_points(primary_team)
            opponent_points = self._team_points(opponent)

            point_diff = primary_points - opponent_points
            if point_diff == 0:
                return (
                        f"Tied at {get_points_string(primary_points)}:"
                        f" {primary_team} and {opponent}"
                )

            return (
                    f"{self._team_string(primary_team)}"
                    f" over {self._team_string(opponent)}"
                    f" by {get_points_string(point_diff)}."
            )

        deduplicated = []
        [
                deduplicated.append((primary_team, opponent))
                for primary_team, opponent in matchups
                if (opponent, primary_team) not in deduplicated
        ]
        return list(map(comparison_matchup_string, deduplicated))

    def _team_string(self, team):
        return team_string(team, self._team_points(team))

    def _multi_matchup_bullets(self, section, points, matchups):

        def multi_matchup_string(primary_team, opponents):
            opponent_string = opponent_matchup_string(
                    self._team_points(primary_team),
                    opponents)
            return f"{self._team_string(primary_team)}; {opponent_string}"

        def opponent_matchup_string(primary_points, opponents):
            opponent_strings = [
                    f"over {self._team_string(opponent)}"
                    if self._team_points(opponent) < primary_points
                    else f"to {self._team_string(opponent)}"
                    if self._team_points(opponent) > primary_points
                    else f"tied with {self._team_points(opponent)}"
                    for opponent in opponents
            ]

            if len(opponent_strings) == 1:
                return opponent_strings[0]
            elif len(opponent_strings) > 2:
                first_string = "; ".join(opponent_strings[:-2])
                last_string = "; and ".join(opponent_strings[-2:])
                return f"{first_string}; {last_string}"

            return ", and ".join(opponent_strings)

        matchup_dict = MultiDict(matchups)
        return [
                multi_matchup_string(team, matchup_dict.getall(team))
                for team in list(dict.fromkeys(matchup_dict.keys()))
        ]


DivisionStats = namedtuple(
        "DivisionStats",
        ["name", "points", "average", "stddev", "record"])


class DivisionTableFormatter:

    def __init__(self, teams):
        self._divisions = MultiDict(
                (team.division, team) for team in teams.values()
        )

    def markdown(self):
        markdown_string = "### Division Stats\n"
        all_stats = self._all_division_stats()
        for index, entries in enumerate(list(zip(*all_stats))):
            columns = [
                    f"**{entry}**" if index == 0 else f"{entry}"
                    for entry in entries
            ]
            markdown_string = f"{markdown_string}\n| {' | '.join(columns)} |"
            if index == 0:
                alignment = " | ".join(len(columns) * [":---:"])
                markdown_string = f"{markdown_string}\n| {alignment} |"

        return [markdown_string]

    def _all_division_stats(self):
        stats = [
                DivisionStats(
                        "Division",
                        "Points",
                        "Points/Team",
                        "Std. Dev.",
                        "Record")
        ]

        stats.extend(
                self._division_stats(division)
                for division 
                in sorted(list(dict.fromkeys(self._divisions.keys()))))

        stats.append(self._division_stats("League"))
        return stats

    def _division_stats(self, division_name):
        teams = (
                self._divisions.values() if division_name == "League"
                else self._divisions.getall(division_name)
        )
        use_record = division_name != "League"

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

