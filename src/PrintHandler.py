from BadgerHandler import BadgerHandler
class PrintHandler (BadgerHandler):
	def on_insert (self, state): 
		print "Smartcard inserted"
	def on_remove (self, state): 
		print "Smartcard removed"
	def on_lock (self, state): 
		print "Locked"
	def on_unlock (self, state): 
		print "Unlocked"