from BadgerHandler import *
import winsound
class SoundHandler(BadgerHandler):

    def __init__ (self, config=None):
        BadgerHandler.__init__(self, config)
        if self.config:
            self.path = self.config.get("path", "freakingidiot.wav")
            self.enable = self.config.get("enable", True)

    def on_lock(self, state):
        if not state.get_inserted() or not self.enable:
            return
        winsound.PlaySound(self.path, winsound.SND_FILENAME)

