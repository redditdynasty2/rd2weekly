#!/usr/bin/env python3
import options
from src.rd2weekly import RD2Week

if __name__ == "__main__":
    opts = options.parse()
    with RD2Week(opts.week, opts.divisionsFile, opts.recordsFile, opts.credentials) as rd2Summary:
        rd2Summary.scrape()
        rd2Summary.generateSummary()
