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

import time
import threading
import psutil


class LockMonitor:

    LOCK_SCREEN_PROCESS = "ScreenSaverEngine"

    def __init__(self, dispatcher, parent=None):
        self.screen_locked = False
        self.monitoring = False
        self.dispatcher = dispatcher
        #self.dispatcher.update_locked(self.get_status(), initial=True)
        self.dispatcher.update_locked(False)

    def get_status(self):
        return self.screen_locked

    def monitor(self):
        self.proc_reader = threading.Thread(target=self.run)
        self.running = True
        self.proc_reader.start()

    def shutdown(self):
        self.running = False

    def run(self):
        lock_process = None
        while self.running:
            #try to find the process that signals the screen is locked
            lock_process = self.get_lock_process()
            #will return None if the screen is not locked
            #update state, and sleep before checking again
            #because for the process being created, we can only poll
            if lock_process is None:
                self.screen_locked = False
                self.dispatcher.update_locked(self.screen_locked)
                time.sleep(0.5)
            #once the process exists, there is an API to wait for it to complete
            #signal that the screen is locked, then wait until it ends to go back
            #through the loop.
            else:
                self.screen_locked = True
                self.dispatcher.update_locked(self.screen_locked)
                lock_process.wait()

    def get_lock_process(self):
        result = None
        for p in psutil.process_iter():
            if p.name == self.LOCK_SCREEN_PROCESS:
                result = p
                break
        return result
