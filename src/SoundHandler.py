from BadgerHandler import *
import winsound
DEBUG = False
class SoundHandler(BadgerHandler):

	def __init__ (self, config=None):
		BadgerHandler.__init__(self, config)
		if self.config:
			self.path = self.config.get("path", "freakingidiot.wav")

	def on_lock(self, state):
		if state.get_inserted() or DEBUG:
			#winsound.Beep(1000, 1500)
			winsound.PlaySound(self.path, winsound.SND_FILENAME)

