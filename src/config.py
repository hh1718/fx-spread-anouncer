import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'packages'))
import json

class Config():
    def __init__(self, path):
        with open(path, 'r') as f:
            json_loaded = json.load(f)
            self.json = json_loaded
            print("config:")
            print(self.json)
            self.anounce_order = json_loaded["announce_order"]
            self.pair = json_loaded["target_pair"]
            force_anounce_per = json_loaded["force_anounce_per"]
            if force_anounce_per < 1:
                self.force_anounce_per = 5
            else:
                self.force_anounce_per = force_anounce_per
            self.force_anounce_per = json_loaded["force_anounce_per"]
            self.time_interval = json_loaded["time_interval"]
            self.logging = json_loaded["logging"]

    def get_json(self):
        return self.json

