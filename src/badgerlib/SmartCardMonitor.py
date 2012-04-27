from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *
from smartcard.Exceptions import NoCardException
from smartcard.System import readers

class SmartCardMonitor(CardObserver):
	def __init__ (self, dispatcher): 
		self.dispatcher = dispatcher

	def get_status(self): 
		cards = 0
		for reader in readers():
			try: 
				connection = reader.createConnection()
				connection.connect()
				cards = cards + 1
			except NoCardException: pass
		return (cards > 0)


	def monitor (self): 
		self.cardmonitor = CardMonitor()
		self.cardmonitor.addObserver(self)

	def shutdown (self): 
		self.cardmonitor.deleteObserver(self)

	def update (self, observable, (addedcards, removedcards)):
		if addedcards: 
			self.dispatcher.update_inserted(True)
		elif removedcards:
			self.dispatcher.update_inserted(False)