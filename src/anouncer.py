import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'packages'))
import pyttsx3

class Anouncer():
    def __init__(self):
        self.engine = pyttsx3.init()
    
    def announce_spread(self, spread):
        self.engine.say(str(spread))
        self.engine.runAndWait()
    
    def anounce_msg(self, msg):
        self.engine.say(msg)
        self.engine.runAndWait()

