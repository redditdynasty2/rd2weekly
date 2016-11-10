from scoring import Player, Team

import re


def parse_teams_and_matchups(browser, teams_to_division):
    teams = {}
    for matchup_soup in browser.get_matchup_soups():
        away_team = parse_matchup_team("away", matchup_soup, teams_to_division)
        home_team = parse_matchup_team("home", matchup_soup, teams_to_division)
        if away_team is None and home_team is None:
            # This matchup exists only to fill out the CBS scoreboard grid.
            continue

        [
                teams.setdefault(team.name, team) 
                for team 
                in [away_team, home_team]
                if team is not None
        ]

        if home_team is not None and away_team is not None:
            Team.update_records(teams[away_team.name], teams[home_team.name])

    return teams


def parse_matchup_team(home_or_away, matchup_soup, teams_to_division):
    team_name = (
            matchup_soup
            .select_one(f"#{home_or_away}_big_name.teamname")
            .string
            .strip()
    )

    if Team.is_blank_team_name(team_name):
        return None
    elif team_name not in teams_to_division:
        raise Exception((
                f"Team {team.name} was not found in the league directory."
        ))

    team = Team(team_name, teams_to_division[team_name])

    player_tags = (
            matchup_soup
            .select_one(f"#{home_or_away}_team_roster")
            .find_all(id=re.compile(r"^player_(active|reserve)_\d+_\d+$"))
    )
    [process_player(tag.parent, team) for tag in player_tags]
    return team


def process_player(player_soup, team):
    active_points_tag = player_soup.select_one(
            "a.scoreLink[id^=score_total_active]")
    if active_points_tag is not None:
        active_points = float(active_points_tag.string.strip())
        # The scoreboard displays the fantasy position that the player occupied
        # for the period. In the soup this is shown as a sibling to the
        # player's name field. At the moment this is the only div tag in the
        # player soup; if this changes, this logic will have to change
        # significantly as selecting this tag on its own is non-trivial.
        #
        # Notably, reserve players still get a fantasy position assigned to
        # them even though they did not occupy a position for the period.
        is_active_pitcher = "P" in (
                player_soup
                .select_one("a.playerLink")
                .parent
                .div
                .string
        )
        if is_active_pitcher:
            team.pitching_points += active_points
        else:
            team.hitting_points += active_points

    name, cbs_id_number = parse_player_name_and_id(player_soup, "title")
    return team.players.append(Player(
            name,
            cbs_id_number,
            active_points_tag and is_active_pitcher is None,
            active_points_tag and is_active_pitcher is not None))


def parse_player_name_and_id(player_soup, name_tag):
    info_tag = player_soup.select_one("a.playerLink")

    try:
        # The name tag passed in looks something like: 
        # "Player Has Name CF SEA", with the format: 
        # "<player's full name> <display position> <real team>".
        #
        # <real_team> will always be 3 uppercase letters if the player is
        # currently on a major league team, but free agent behavior isn't well
        # defined.
        #
        # <display_position> does not correspond to fantasy position 
        # eligibility in the slightest but rather the player's real life, best
        # estimate (by CBS, so caveats there) position, such as "DH" or "P" or
        # "1B".
        #
        # While we use neither of the above fields, it is important to
        # understand that this regex relies on matching being greedy, and that
        # the last 2 non-whitespace sections of the player string correspond to
        # this unused data.
        #
        # Notably, we cannot rely on the display string for the name to give us
        # the player's full name. This information seems to only live in this
        # tag. The display name will often abbreviate the name even when using
        # a screen with infinite width. In the above example, the display name
        # for the player would likely be "Player H. Name".
        player_name_match = re.match(
                r"^\s*(.+)\s+[A-Z1-3]+\s+[A-Z]+\s*$",
                info_tag[name_tag])
        player_name = player_name_match.group(1)

        cbs_id_number_match = re.match(
                r"^/players/playerpage/(\d+)$",
                info_tag["href"])
        cbs_id_number = cbs_id_number_match.group(1)
        return player_name, cbs_id_number
    except AttributeError as root_exception:
        raise AttributeError((
                f"Failed to read player with soup:\n{player_soup.prettify()}"
        )) from root_exception

