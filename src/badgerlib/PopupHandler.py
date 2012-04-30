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

import badgerlib
import ctypes
import time

class PopupHandler(badgerlib.Handler):
    MB_ICONEXCLAMATION = 0x30
    MB_SYSTEMMODAL = 0x1000
    MB_SERVICE_NOTIFICATION = 0x200000L
    MB_SETFOREGROUND = 0x00010000L
    MB_TOPMOST = 0x00040000L
    def __init__ (self, config=None):
        badgerlib.Handler.__init__(self, config)
        self.enable = False
        self.delay = 0.5
        self.message = "Smartcard Still Inserted"
        if self.config:
            self.enable = self.config.get("enable", True)
            self.delay = self.config.get("delay", self.delay)
            self.message = self.config.get("message", self.message)

    def on_lock(self, state):
        if not state.get_inserted() or not self.enable:
            return
        time.sleep(self.delay)
        print "Messagebox: %d" % (ctypes.windll.User32.MessageBoxA(None, self.message, "Badger", self.MB_SERVICE_NOTIFICATION  | self.MB_ICONEXCLAMATION | self.MB_SYSTEMMODAL )) # | self.MB_SETFOREGROUND | self.MB_TOPMOST)