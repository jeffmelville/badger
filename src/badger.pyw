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
import time
import json
import wx
import sys

APP_NAME = "Badger"
VERSION = 0.5
TRAY_TOOLTIP = "Badger!"
TRAY_ICON = 'badger.png'
DEBUG = False

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__ (self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'About', self.on_about)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event): pass
    def on_about(self, event): 
        dlg = wx.MessageDialog( None, "%s v. %s by Jeff Melville" % (APP_NAME, VERSION), "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    def on_exit (self, event):
        wx.CallAfter(self.Destroy)

handler_map = {"SoundHandler": badgerlib.SoundHandler, "PrintHandler": badgerlib.PrintHandler, "EmailHandler": badgerlib.EmailHandler, "PopupHandler": badgerlib.PopupHandler}
def main():
    app = wx.PySimpleApp()
    try:
        config = json.loads(open("config.json", 'r').read())
    except:
        print "Configuration error. Quit"
        return
    if not "handlers" in config:
        print "Invalid configuration file. Quit"
        return
    handlers = config["handlers"]
    state = badgerlib.State()
    printhandler = badgerlib.PrintHandler()
    dispatcher = badgerlib.Dispatcher(state)
    #set up handlers
    for handler in handlers:
        handler_name = handler.get("name", "NO_HANDLER")
        if handler_name not in handler_map:
            print "Skipping unrecognized handler: %s" % (handler_name)
            continue
        handler_type = handler_map[handler_name]
        dispatcher.add_handler(handler_type(config = handler.get("config", None)))
        print "Added handler: %s" % handler_name
    lock = badgerlib.LockMonitor(dispatcher)
    lock.monitor()
    if badgerlib.SmartCardMonitor:
        sc = badgerlib.SmartCardMonitor(dispatcher)
        sc.monitor()
    else: 
        print "Did not import smart card module"

    if DEBUG: dispatcher.update_inserted(True)
    TaskBarIcon()
    app.MainLoop()

    print "Shutting down..."

    lock.shutdown()

if __name__ == "__main__":
    if (len(sys.argv)==2 and sys.argv[1]=="inserted"): DEBUG=True
    main()