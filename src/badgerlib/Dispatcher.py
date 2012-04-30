# Copyright (c) 2012, Jeff Melville
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

	