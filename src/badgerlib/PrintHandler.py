import badgerlib

class PrintHandler (badgerlib.Handler):
    def on_insert (self, state): 
        print "Smartcard inserted"
    def on_remove (self, state): 
        print "Smartcard removed"
    def on_lock (self, state): 
        print "Locked, and printing"
    def on_unlock (self, state): 
        print "Unlocked"        
