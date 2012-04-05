class BadgerState:
	def __init__ (self, inserted=False, locked=False):
		self.inserted = inserted
		self.locked = locked

	def get_inserted(self): return self.inserted
	def set_inserted(self, inserted): self.inserted = inserted

	def get_locked (self): return self.locked
	def set_locked (self, locked): self.locked = locked
	