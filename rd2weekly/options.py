import argparse
import datetime

import version


def parse():
    parser = argparse.ArgumentParser(description="Scrapes the CBS fantasy baseball site for weekly summaries")
    parser.add_argument("-c", "--credentials",
                        nargs=2,
                        required=True,
                        help="Credentials to use to sign into CBS")
    parser.add_argument("-p", "--period",
                        type=int,
                        help="Scoring period to examine. Default is the current scoring session")
    parser.add_argument("-v", "--version",
                        action="version",
                        version="%(prog)s: {0}".format(version.__version__),
                        help="Print tool's version and exit")

    # TODO: get reasonable place for config files to live
    leagueConfigGroup = parser.add_argument_group("League Configuration")
    leagueConfigGroup.add_argument("-d", "--divisionsFile",
                                   type=argparse.FileType("r"),
                                   default="???",
                                   help="JSON file of the league's teams and divisions. Defaults to ???")
    leagueConfigGroup.add_argument("-r", "--recordsFile",
                                   type=argparse.FileType("r+"),
                                   default="???",
                                   help="JSON file of the league's records. Defaults to ???")

    return parser.parse_args()
