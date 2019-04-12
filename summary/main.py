#!/usr/bin/env python3

from browser import CBSBrowserSession

import argparse
import json
import markdown_formatter
import matchup_parser
import point_leaders


def parse_args():
    parser = argparse.ArgumentParser(description=(
            "Generates a weekly summary for a CBS fantasy baseball"
            " league."
    )) 

    parser.add_argument(
            "-p",
            "--period",
            type=int,
            default=0,
            required=True,
            help=(
                    "The period to generate a summary for. Values less"
                    " than 0 will pull the current scoreboard"
                    " information instead of a given period."
            ))
    parser.add_argument(
            "-l",
            "--league",
            required=False,
            type=argparse.FileType("r+"),
            default="config/leagueDivisions.json",
            help="JSON file of the league layout.")
    parser.add_argument(
            "-n",
            "--nicknames",
            required=False,
            type=argparse.FileType("r+"),
            default="config/nicknames.json",
            help=(
                    "JSON file for custom nicknames, mapping CBS id"
                    " number to desired player name."
            ))

    parser.add_argument(
            "-c",
            "--credentials",
            nargs=2,
            metavar=("<username>", "<password>"),
            help=(
                    "Credentials to use to sign into CBS. If not"
                    " provided (maybe you want to keep your bash"
                    " history clear of passwords?), the user will be"
                    " prompted to enter their credentials."
            ))

    return parser.parse_args()


def parse_period(league_home, teams_to_division, args):
    with CBSBrowserSession(league_home, args) as browser:
        teams = matchup_parser.parse_teams_and_matchups(
                browser,
                teams_to_division)
        top_scorers, worst_scorers = point_leaders.parse_points_leaders(
                args.period,
                teams.values(),
                browser)
        return teams, top_scorers, worst_scorers


def main():
    args = parse_args()
    league_info = json.load(args.league)
    teams_to_division = dict(
            (team_name, division["division"])
            for division in league_info["divisions"]
            for team_name in division["teams"])

    teams, top_scorers, worst_scorers = parse_period(
            league_info["league_url"],
            teams_to_division,
            args)

    nicknames = json.load(args.nicknames)
    print(markdown_formatter.get_summary_string(
            teams,
            top_scorers,
            worst_scorers,
            nicknames))

if __name__ == "__main__":
    main()

