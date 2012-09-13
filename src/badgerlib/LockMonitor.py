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
import ctypes
import threading

user32 = ctypes.windll.user32
OpenDesktop = user32.OpenDesktopA
SwitchDesktop = user32.SwitchDesktop
DESKTOP_SWITCHDESKTOP = 0x0100

#Modified from: http://wiki.wxpython.org/HookingTheWndProc
##########################################################################
##
##  This is a modification of the original WndProcHookMixin by Kevin Moore,
##  modified to use ctypes only instead of pywin32, so it can be used
##  with no additional dependencies in Python 2.5
##
##########################################################################


import sys
import ctypes
from ctypes import c_long, c_int, wintypes

import wx


GWL_WNDPROC = -4
WM_DESTROY  = 2
DBT_DEVTYP_DEVICEINTERFACE = 0x00000005  # device interface class
DBT_DEVICEREMOVECOMPLETE = 0x8004  # device is gone
DBT_DEVICEARRIVAL = 0x8000  # system detected a new device
WM_DEVICECHANGE = 0x0219
WM_WTSSESSION_CHANGE = 0x02b1

## It's probably not neccesary to make this distinction, but it never hurts to be safe
if 'unicode' in wx.PlatformInfo:
    SetWindowLong = ctypes.windll.user32.SetWindowLongW
    CallWindowProc = ctypes.windll.user32.CallWindowProcW
else:
    SetWindowLong = ctypes.windll.user32.SetWindowLongA
    CallWindowProc = ctypes.windll.user32.CallWindowProcA

## Create a type that will be used to cast a python callable to a c callback function
## first arg is return type, the rest are the arguments
#WndProcType = ctypes.WINFUNCTYPE(c_int, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
WndProcType = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int)

"""
if 'unicode' in wx.PlatformInfo:
    RegisterDeviceNotification = ctypes.windll.user32.RegisterDeviceNotificationW
else:
    RegisterDeviceNotification = ctypes.windll.user32.RegisterDeviceNotificationA
RegisterDeviceNotification.restype = wintypes.HANDLE
RegisterDeviceNotification.argtypes = [wintypes.HANDLE, wintypes.c_void_p, wintypes.DWORD]

UnregisterDeviceNotification = ctypes.windll.user32.UnregisterDeviceNotification
UnregisterDeviceNotification.restype = wintypes.BOOL
UnregisterDeviceNotification.argtypes = [wintypes.HANDLE]

class DEV_BROADCAST_DEVICEINTERFACE(ctypes.Structure):
    _fields_ = [("dbcc_size", ctypes.c_ulong),
                  ("dbcc_devicetype", ctypes.c_ulong),
                  ("dbcc_reserved", ctypes.c_ulong),
                  ("dbcc_classguid", GUID.GUID),
                  ("dbcc_name", ctypes.c_wchar * 256)]

class DEV_BROADCAST_HDR(ctypes.Structure):
    _fields_ = [("dbch_size", wintypes.DWORD),
                ("dbch_devicetype", wintypes.DWORD),
                ("dbch_reserved", wintypes.DWORD)]

"""

class WndProcHookMixin:
    """
    This class can be mixed in with any wxWindows window class in order to hook it's WndProc function. 
    You supply a set of message handler functions with the function addMsgHandler. When the window receives that
    message, the specified handler function is invoked. If the handler explicitly returns False then the standard 
    WindowProc will not be invoked with the message. You can really screw things up this way, so be careful. 
    This is not the correct way to deal with standard windows messages in wxPython (i.e. button click, paint, etc) 
    use the standard wxWindows method of binding events for that. This is really for capturing custom windows messages
    or windows messages that are outside of the wxWindows world.
    """
    def __init__(self):
        self.__msgDict = {}
        ## We need to maintain a reference to the WndProcType wrapper
        ## because ctypes doesn't
        self.__localWndProcWrapped = None
        self.rtnHandles = []

    def hookWndProc(self):
        self.__localWndProcWrapped = WndProcType(self.localWndProc)
        self.__oldWndProc = SetWindowLong(self.GetHandle(),
                                        GWL_WNDPROC,
                                        self.__localWndProcWrapped)
    def unhookWndProc(self):
        SetWindowLong(self.GetHandle(),
                        GWL_WNDPROC,
                        self.__oldWndProc)

        ## Allow the ctypes wrapper to be garbage collected
        self.__localWndProcWrapped = None

    def addMsgHandler(self,messageNumber,handler):
        self.__msgDict[messageNumber] = handler

    def localWndProc(self, hWnd, msg, wParam, lParam):
        # call the handler if one exists
        # performance note: "in" is the fastest way to check for a key
        # when the key is unlikely to be found
        # (which is the case here, since most messages will not have handlers).
        # This is called via a ctypes shim for every single windows message 
        # so dispatch speed is important
        if msg in self.__msgDict:
            # if the handler returns false, we terminate the message here
            # Note that we don't pass the hwnd or the message along
            # Handlers should be really, really careful about returning false here
            if self.__msgDict[msg](wParam,lParam) == False:
                return

        # Restore the old WndProc on Destroy.
        if msg == WM_DESTROY: self.unhookWndProc()

        return CallWindowProc(self.__oldWndProc,
                                hWnd, msg, wParam, lParam)

""""
    def registerDeviceNotification(self, guid, devicetype=DBT_DEVTYP_DEVICEINTERFACE):
        devIF = DEV_BROADCAST_DEVICEINTERFACE()
        devIF.dbcc_size = ctypes.sizeof(DEV_BROADCAST_DEVICEINTERFACE)
        devIF.dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE

        if guid:
            devIF.dbcc_classguid = GUID.GUID(guid)
        return RegisterDeviceNotification(self.GetHandle(), ctypes.byref(devIF), 0)

    def unregisterDeviceNotification(self, handle):
        if UnregisterDeviceNotification(handle) == 0:
            raise Exception("Unable to unregister device notification messages")
"""

class LockMonitor(wx.Frame,WndProcHookMixin):
    def __init__(self,dispatcher,parent=None):
        WndProcHookMixin.__init__(self)
        wx.Frame.__init__(self,parent,-1,"Badger Lock Monitor",size=(320,240))

        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.screen_locked = False
        self.monitoring = False
        self.dispatcher = dispatcher
        #self.dispatcher.update_locked(self.get_status(), initial=True)
        self.dispatcher.update_locked(False)

   	def get_status(self):
   		return self.screen_locked

   	def monitor(self):
   		self.monitoring = True
        self.addMsgHandler(WM_WTSSESSION_CHANGE, self.onSessionChange)
        self.hookWndProc()

    def shutdown(self):
    	if not self.monitoring: return
    	self.monitoring = False

    def onSessionChange(self,wParam,lParam):
        print "WM_WTSSESSION_CHANGE [WPARAM:%i][LPARAM:%i]"%(wParam,lParam)

        return True

    def onClose(self, event):
    	self.shutdown()
        event.Skip()

