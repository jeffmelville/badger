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

import subprocess
import threading

class LockMonitor:
    def __init__(self, dispatcher, parent=None):

        self.screen_locked = False
        self.monitoring = False
        self.dispatcher = dispatcher
        #self.dispatcher.update_locked(self.get_status(), initial=True)
        self.dispatcher.update_locked(False)
        self.proc = None
        self.running = False

    def get_status(self):
        return self.screen_locked

    def monitor(self):
        if self.proc: self.shutdown()
        self.proc = subprocess.Popen("xscreensaver-command -watch",shell=True, stdout=subprocess.PIPE)
        self.proc_reader = threading.Thread(target=self.run)
        self.running = True
        self.proc_reader.start()


    def shutdown(self):
        #TODO: Not sure this will terminate correctly
        if self.proc: self.proc.terminate()
        self.running = False
        self.proc = None

    def run(self):
        for line in iter(self.proc.stdout.readline,''):
            if "UNBLANK" in line:
                self.screen_locked = False
            elif "LOCK" in line:
                self.screen_locked = True
            else:
                continue
            self.dispatcher.update_locked(self.screen_locked)

