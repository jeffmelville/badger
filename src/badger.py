from BadgerState import *
from PrintHandler import *
from BadgerDispatcher import *
from LockMonitor import *
from SoundHandler import *
import time
def main():
	state = BadgerState()
	printhandler = PrintHandler(state)
	dispatcher = BadgerDispatcher(state)
	dispatcher.add_handler(printhandler)
	dispatcher.add_handler(SoundHandler(state, "freakingidiot.wav"))
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
		except KeyboardInterrupt: break

	lock.shutdown()

if __name__ == "__main__": main()