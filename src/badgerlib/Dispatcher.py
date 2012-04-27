import badgerlib

class Dispatcher:
	def __init__ (self, state=None): 
		self.handlers = []
		if state is None:
			state = badgerlib.State()
		self.state = state

	def add_handler (self, handler):
		if handler not in self.handlers: 
			self.handlers.append (handler)

	def remove_handler (self, handler):
		self.handlers.remove(handler)

	def update_param(self, param, value, initial=False):
		if param=="inserted":
			self.update_inserted(value,initial)
		elif param=="locked": 
			self.update_locked(value, initial)
		else:
			raise ValueError

	def update_inserted (self, inserted, initial=False): 
		if initial:
			self.state.set_inserted(inserted)
			return
		last_inserted = self.state.get_inserted()
		self.state.set_inserted(inserted)
		if last_inserted == inserted: return
		for handler in self.handlers:
			if inserted: 
				handler.on_insert(self.state)
			else:
				handler.on_remove(self.state)


	def update_locked (self, locked, initial=False): 
		if initial:
			self.state.set_locked(locked)
			return
		last_locked = self.state.get_locked()
		self.state.set_locked(locked)
		if last_locked == locked: return
		for handler in self.handlers:
			if locked: 
				handler.on_lock(self.state)
			else:
				handler.on_unlock(self.state)

	