#!/usr/bin/env python3
import options
from src.rd2weekly import RD2Week

if __name__ == "__main__":
    opts = options.parse()
    rd2Summary = RD2Week(opts.week, opts.divisionsFile, opts.recordsFile, opts.credentials)
    rd2Summary.generateSummary()
