from watcher import watcher
import datetime
import json
import os

from local import game_log_loc

class scraper():
    def __init__(self):
        
        self.start_time = int(datetime.datetime(2021, 9, 23, 0, 0).timestamp())
        self.stop_time = int(datetime.datetime(2021, 10, 5, 23, 59).timestamp())
        
        # It would be fairly easy to create this directory if it did not exist
        # but considering how easy it is for this dump to be multiple Gigabytes
        # I am leaving the directory creation as manual just as a safty precaution 
        self.game_log_directory = game_log_loc + "/games/"
        self.sets_dump_file = "sets.json"
        
        self.games_indexed = set() # Set not a list
        self.puuids_indexed = set() # Set not a list
        self.games_not_indexed = set() # Set not a list
        self.puuids_not_indexed = set() # Set not a list
        
        # init riot watcher
        self.watcher = watcher()
        
        # get seed puuid of arbitrary challenger player
        self.seed_puuid = self.watcher.get_challenger_id()
        
        self.puuids_not_indexed.add(self.seed_puuid)
    
    def _dump_sets(self):
        json_obj = {
            "Games Indexed" : list(self.games_indexed),
            "Games Not Indexed" : list(self.games_not_indexed),
            "Players Indexed" : list(self.puuids_indexed), 
            "Players Not Indexed" : list(self.puuids_not_indexed)}
        with open(self.sets_dump_file, "w") as file:
            json.dump(json_obj, file)

    
    def parse_new_games(self, games):
        for game in games:
            if game in self.games_indexed:
                continue
            if game in self.games_not_indexed:
                continue
            
            # This is a new game ID
            self.games_not_indexed.add(game)
            
    def parse_new_puuids(self, puuids):
        for puuid in puuids:
            if puuid in self.puuids_indexed:
                continue
            if puuid in self.puuids_not_indexed:
                continue
            
            # This is a new puuid
            self.puuids_not_indexed.add(puuid)
    
    def get_games(self):
        if len(self.puuids_not_indexed) == 0:
            print("No more players")
            return
        
        puuid = self.puuids_not_indexed.pop()
        self.puuids_indexed.add(puuid)
        print("Getting Player:", puuid)
        games = self.watcher.get_games_of_id(puuid, self.start_time, self.stop_time)
        self.parse_new_games(games)
        
    
    def get_next_game(self):
        if len(self.games_not_indexed) == 0:
            self.get_games()
        game_id = self.games_not_indexed.pop()
        self.games_indexed.add(game_id)
        
        return self.watcher.get_game(game_id)
    
    def game_get_participants(self, game):
        return game["metadata"]["participants"]
        
    
    def game_get_match_id(self, game):
        return game["metadata"]["matchId"]
    
    def write_game(self, game):
        game_id = self.game_get_match_id(game)
        name = self.game_log_directory + "{}.json".format(game_id)
        print("Writing file:", name)
        with open(name, 'w') as file:
            json.dump(game, file)
            
    def _process_game(self, game):
        participants = self.game_get_participants(game)
        self.parse_new_puuids(participants)
        
    
    def process_next_game(self):
        game = self.get_next_game()
        self._process_game(game)
        self.write_game(game)
        
    
    def run(self):
        # Recover from last run. This should prevent duplicate game data from being captured
        # To prevent this, comment out this line or delete sets.json 
        self.recover_sets()
        
        fails = 0
        while fails < 5:
            try:
                self.process_next_game()
                fails = 0
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(type(e))
                print(e.args)
                print(e)
                fails += 1
                
        self._dump_sets()
        
    def import_game_to_sets(self, file_name):
        try:
            with open(file_name) as file:
                json_obj = json.load(file)
        except: 
            return -1;  
        # when importing from game logs we are only populating 2 sets
        # the not indexed players and the indexed games
        # This will result in a number of players having their game history pulled, 
        # and no games bing imported, but there is not a great way around that, 
        # and it is still significantly better than re-pulling all of the games
        
        game_id = self.game_get_match_id(json_obj)
        self.games_indexed.add(game_id)
        print("Recovering game:", game_id)
        self._process_game(json_obj)
        return 0
        
    # Populates the sets from a directory of game logs.
    # Hopefully dumping the sets to a json makes this redundant
    # but I see no reason to discard the functionality
    def recover_from_game_files(self):
        
        failed = []
        
        for file_name in os.scandir(self.game_log_directory):
            if file_name.path.endswith(".json") and file_name.is_file():
                if self.import_game_to_sets(file_name) < 0:
                    failed.append(str(file_name))
                    
        print("Failed to recover fails:", failed)
        self._dump_sets()
        
    def recover_sets(self):
        with open(self.sets_dump_file) as file:
            sets = json.load(file)
            
        self.games_indexed.update(sets["Games Indexed"])
        self.games_not_indexed.update(sets["Games Not Indexed"])
        self.puuids_indexed.update(sets["Players Indexed"])
        self.puuids_not_indexed.update(sets["Players Not Indexed"])
        
if __name__ == "__main__":
    s = scraper()
    s.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   