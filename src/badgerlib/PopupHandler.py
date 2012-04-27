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