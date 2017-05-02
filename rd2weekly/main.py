#!/usr/bin/env python3
from getpass import getpass

import options
from src.rd2weekly import RD2Week

if __name__ == "__main__":
    opts = options.parse()
    credentials = opts.credentials if opts.credentials else [input("Username: "), getpass()]
    rd2Summary = RD2Week(opts.period, opts.divisionsFile, opts.recordsFile, credentials)
    rd2Summary.scrape()
    rd2Summary.print()
