# RD2 Weekly
---

A scraper that generates weekly summaries for the Reddit Dynasty 2 fantasy
baseball league.

## Requirements

* Python 3.9 or newer
* Docker
* A CBS account with access to the Reddit Dynasty 2 fantasy baseball league
* An internet connection

## Running the weekly summary

1. Clone the repository
1. Create a Python virtual environment
  ```shell
  python3 -m venv .venv
  ```
1. Activate the virtual environment
  ```shell
  # instructions for bash; follow your shell's instructions
  source .venv/bin/activate
  ```
1. Install project dependencies
  ```shell
  pip install --upgrade . -c constraints.txt
  ```
1. Run the script. It takes a while to scrape data from CBS and compute the
   optimal all star lineups
  ```shell
  ./src/main.py -s <scoring period> -u <your CBS username> -p <your CBS password>
  ```
1. Resolve multiple all star lineups. Because of how the scraper gathers data,
   it will pull all optimal lineups and won't attempt to deduplicate them; this
   is up to you to do
1. Copy-paste the results into the league subreddit
