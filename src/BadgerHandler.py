class BadgerHandler:
	def __init__ (self, state):
		self.state = state

	def on_insert(self): pass
	def on_remove(self): pass
	def on_lock(self): pass
	def on_unlock(self): pass
	