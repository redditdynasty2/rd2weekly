import argparse
from argparse import Namespace

import version


def parse() -> Namespace:
    parser = argparse.ArgumentParser(description="Scrapes the CBS fantasy baseball site for weekly summaries")
    parser.add_argument("-c", "--credentials",
                        nargs=2,
                        metavar=("<username>", "<password>"),
                        help="Credentials to use to sign into CBS")
    parser.add_argument("-p", "--period",
                        type=int,
                        metavar="<scoring_period>",
                        required=True,
                        help="Scoring period to examine. Default is the current scoring session. Currently must be a completed scoring period")
    parser.add_argument("-v", "--version",
                        action="version",
                        version="%(prog)s: {0}".format(version.__version__),
                        help="Print tool's version and exit")

    leagueConfigGroup = parser.add_argument_group("League Configuration")
    leagueConfigGroup.add_argument("-d", "--divisionsFile",
                                   type=argparse.FileType("r"),
                                   metavar="<json_file>",
                                   default="sampleConfig/leagueDivisions.template",
                                   help="JSON file of the league's teams and divisions. Defaults to sampleConfig/leagueDivisions.template")
    leagueConfigGroup.add_argument("-r", "--recordsFile",
                                   type=argparse.FileType("r+"),
                                   metavar="<json_file>",
                                   default="sampleConfig/leagueRecords.template",
                                   help="JSON file of the league's records. Defaults to sampleConfig/leagueRecords.template")

    return parser.parse_args()
