class BadgerHandler:
	def __init__ (self, config=None):
		self.config = config

	def on_insert(self, state): pass
	def on_remove(self, state): pass
	def on_lock(self, state): pass
	def on_unlock(self, state): pass
	