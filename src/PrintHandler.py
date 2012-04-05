from BadgerHandler import BadgerHandler
class PrintHandler (BadgerHandler):
	def on_insert (self): 
		print "Smartcard inserted"
	def on_remove (self): 
		print "Smartcard removed"
	def on_lock (self): 
		print "Locked"
	def on_unlock (self): 
		print "Unlocked"