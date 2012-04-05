from BadgerHandler import *
import winsound
DEBUG = False
class SoundHandler(BadgerHandler):

	def __init__ (self, state=None, path=None):
		BadgerHandler.__init__(self, state)
		self.path = path


	def on_lock(self):
		if self.state.get_inserted() or DEBUG:
			#winsound.Beep(1000, 1500)
			winsound.PlaySound(self.path, winsound.SND_FILENAME)

