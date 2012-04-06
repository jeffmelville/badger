from BadgerState import *
from PrintHandler import *
from BadgerDispatcher import *
from LockMonitor import *
from SoundHandler import *
import time
import json

handler_map = {"SoundHandler": SoundHandler, "PrintHandler": PrintHandler}
def main():
	try:
		config = json.loads(open("config.json", 'r').read())
	except:
		print "Configuration error. Quit"
		return
	if not "handlers" in config:
		print "Invalid configuration file. Quit"
		return
	handlers = config["handlers"]
	state = BadgerState()
	printhandler = PrintHandler()
	dispatcher = BadgerDispatcher(state)
	#set up handlers
	for handler in handlers:
		handler_name = handler.get("name", "NO_HANDLER")
		if handler_name not in handler_map:
			print "Skipping unrecognized handler: %s" % (handler_name)
			continue
		handler_type = handler_map[handler_name]
		dispatcher.add_handler(handler_type(config = handler.get("config", None)))
		print "Added handler: %s" % handler_name
	lock = LockMonitor(dispatcher)
	state.set_locked(lock.get_status())
	lock.monitor()
	try:
		from SmartCardMonitor import SmartCardMonitor
		sc = SmartCardMonitor(dispatcher)
		state.set_inserted(sc.get_status())
		sc.monitor()
	except ImportError: 
		print "Did not import smart card module"

	while 1:
		try: time.sleep(2)
		except:  #only wanted to catch KeyboardInterrupt, but was working weirdly with py2exe output
			print "Quitting."
			break

	lock.shutdown()

if __name__ == "__main__": main()