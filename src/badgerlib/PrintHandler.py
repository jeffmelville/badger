import badgerlib
import ctypes

class PrintHandler (badgerlib.Handler):
	def on_insert (self, state): 
		print "Smartcard inserted"
        print ctypes.windll.User32.MessageBoxA(None, "Smartcard Still Inserted", "Badger", 0x30 | 0x1000 | 0x200000)
	def on_remove (self, state): 
		print "Smartcard removed"
	def on_lock (self, state): 
		print "Locked, and printing"
        print ctypes.windll.User32.MessageBoxA(None, "Smartcard Still Inserted", "Badger", 0x30 | 0x1000 | 0x200000)
	def on_unlock (self, state): 
		print "Unlocked"        
        print ctypes.windll.User32.MessageBoxA(None, "Smartcard not Inserted", "Badger", 0x30 | 0x1000 | 0x200000)
