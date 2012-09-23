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

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.ReaderMonitoring import ReaderMonitor, ReaderObserver
from smartcard.util import *
from smartcard.Exceptions import NoCardException
from smartcard.System import readers

class CallbackReaderObserver(ReaderObserver):
    def __init__(self, target=None):
        self._target = target

    def update(self, observable, (addedreaders, removedreaders)):
        self._target(observable, (addedreaders, removedreaders))

class SmartCardMonitor(CardObserver):
    def __init__ (self, dispatcher): 
        self.cards = 0
        self.n_readers = 0
        self.monitoring = False #card observer is being monitored
        self.dispatcher = dispatcher
        self.dispatcher.update_inserted(self.get_status(), initial=True)

    def get_status(self): 
        cards = 0
        self.n_readers = len(readers())
        for reader in readers():
            try: 
                connection = reader.createConnection()
                connection.connect()
                cards = cards + 1
            except NoCardException: pass
        self.cards = cards
        return (self.cards > 0)


    def monitor (self): 
        self.readermonitor = ReaderMonitor()
        self.readerobserver = CallbackReaderObserver(self.update_readers)
        self.readermonitor.addObserver(self.readerobserver)
        self.cardmonitor = CardMonitor()
        if self.n_readers > 0:
            self.monitoring = True
            self.cardmonitor.addObserver(self)


    def shutdown (self): 
        if self.monitoring:
            self.cardmonitor.deleteObserver(self)

    def update_readers(self, observable, (addedreaders, removedreaders)):
        self.n_readers = len(readers())
        if self.n_readers == 0 and self.monitoring:
            self.cardmonitor.deleteObserver(self)
            self.monitoring = False
        elif self.n_readers > 0 and not self.monitoring:
            self.cardmonitor.addObserver(self)
            self.monitoring = True


    def update (self, observable, (addedcards, removedcards)):
        #update the number of cards currently inserted in the system
        self.cards = self.cards + len(addedcards) - len(removedcards)
        if self.cards > 0: 
            self.dispatcher.update_inserted(True)
        else:
            self.dispatcher.update_inserted(False)