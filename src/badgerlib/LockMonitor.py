import time
import ctypes
import threading

user32 = ctypes.windll.user32
OpenDesktop = user32.OpenDesktopA
SwitchDesktop = user32.SwitchDesktop
DESKTOP_SWITCHDESKTOP = 0x0100
# http://timgolden.me.uk/python/win32_how_do_i/see_if_my_workstation_is_locked.html
class LockMonitor:
	def __init__ (self, dispatcher, poll_interval = 0.2):
		self.dispatcher = dispatcher
		self.running = True
		self.poll_interval = poll_interval

	def get_status (self): 
			hDesktop = OpenDesktop("default", 0, False, DESKTOP_SWITCHDESKTOP)
			result = SwitchDesktop (hDesktop)
			if result:
				#unlocked
				return False
			else:
				return True

	def monitor (self): 
		threading.Thread(target=self.thread_run).start()

	def shutdown (self): 
		self.running = False

	def thread_run(self): 
		while self.running:
			self.dispatcher.update_locked(self.get_status())
			time.sleep(self.poll_interval)

