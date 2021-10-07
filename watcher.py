from riotwatcher import LolWatcher
from library import Log_Mode, error_handler

from local import my_key

challenger_name = "GeneralSn1per"

ranked_queue_id = 420  # From https://static.developer.riotgames.com/docs/lol/queues.json 

class watcher:
    def __init__(self):
        self.watcher = LolWatcher(my_key)
        self.tag_line = "na1"
        self.region = "americas"
        self.queue = "RANKED_SOLO_5x5"
        self.debug = Log_Mode.USER
     
    @error_handler
    def test(self):
        print("Test: ", self.watcher.summoner.by_name(self.region, 'bbc0093'))

    @error_handler
    def get_challenger_id(self):
        player = self.watcher.summoner.by_name(self.tag_line, challenger_name)
        return player["puuid"]
    
    @error_handler
    def get_games_of_id(self, puuid, start_time_epoc, stop_time_epoc):
        return self.watcher.match_v5.matchlist_by_puuid(self.region, puuid, queue = ranked_queue_id, start_time = start_time_epoc, end_time = stop_time_epoc)
    
    def get_game(self, game_id):
        return self.watcher.match_v5.timeline_by_match(self.region, game_id)
    
if __name__ == "__main__":
    w = watcher()
    print(w.get_challenger_id())