# riot_lol_games_scrape

Script to pull down large numbers of league of legand game logs. 

Relient on [RiotWatcher](https://riot-watcher.readthedocs.io/en/latest/)
and you having a riot developer API key https://developer.riotgames.com/

## Output

A dump of game file can be fouud in this repo: https://github.com/bbc0093/lol_game_logs

## Installation and Setup Instructions

The project relies on a development branch of riot-watcher. As of (10/7/2021) full implementation of matches endpoint has not be pulled into HEAD. At the time of writing, this implementation is availible in [this pull request](https://github.com/pseudonym117/Riot-Watcher/pull/191). 

The local_template.py file is a template of a required file used to store local parameters. In order to run this  script you will have to copy it to a file called local.py and populate it with values appropreate for your local environment. 
