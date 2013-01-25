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

import json
import wx
import sys
import os
import shutil

import badgerlib
import appdirs

APP_NAME = "Badger"
APP_VENDOR = "jeffmelville"
APP_AUTHOR = "Jeff Melville"
VERSION = 0.7
TRAY_TOOLTIP = "Badger!"
TRAY_ICON = 'badger.png'
DEBUG = False


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class TaskBarIcon(wx.TaskBarIcon):

    def __init__(self, shutdown_func=None):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        if not shutdown_func:
            shutdown_func = self.Destroy
        self.shutdown_func = shutdown_func

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, "Options", self.on_options)
        create_menu_item(menu, 'About', self.on_about)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        pass

    def on_options(self, event):
        dlg = wx.MessageDialog(None, "Please restart Badger after updating config", APP_NAME, wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        os.system("notepad.exe \"%s\"" % Badger.get_user_config_path())

    def on_about(self, event):
        dlg = wx.MessageDialog(None, "%s v. %s by Jeff Melville" % (APP_NAME, VERSION), "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def on_exit(self, event):
        wx.CallAfter(self.shutdown_func)


class Badger:
    handler_map = {"SoundHandler": badgerlib.SoundHandler, "PrintHandler": badgerlib.PrintHandler, "EmailHandler": badgerlib.EmailHandler, "PopupHandler": badgerlib.PopupHandler}

    @classmethod
    def main(cls):
        cls.app = wx.PySimpleApp()
        try:
            cls.config = cls.load_config()
        except ValueError:
            print "Configuration error. Quit"
            return
        if not "handlers" in cls.config:
            print "Invalid configuration file. Quit"
            return
        cls.handlers = cls.config["handlers"]
        cls.state = badgerlib.State()
        cls.printhandler = badgerlib.PrintHandler()
        cls.dispatcher = badgerlib.Dispatcher(cls.state)
        #set up handlers
        for handler in cls.handlers:
            handler_name = handler.get("name", "NO_HANDLER")
            if handler_name not in cls.handler_map:
                print "Skipping unrecognized handler: %s" % (handler_name)
                continue
            handler_type = cls.handler_map[handler_name]
            cls.dispatcher.add_handler(handler_type(config = handler.get("config", None)))
            print "Added handler: %s" % handler_name
        cls.lock = badgerlib.LockMonitor(cls.dispatcher)
        cls.lock.monitor()
        if badgerlib.SmartCardMonitor:
            cls.sc = badgerlib.SmartCardMonitor(cls.dispatcher)
            cls.sc.monitor()
        else:
            print "Did not import smart card module"

        if DEBUG: cls.dispatcher.update_inserted(True)
        cls.taskbar = TaskBarIcon(shutdown_func=cls.shutdown)
        cls.app.MainLoop()

    @classmethod
    def get_user_config_path(cls):
        config_filename = "config.json"
        user_config_dir = appdirs.user_data_dir(APP_NAME, APP_AUTHOR)
        user_config_path = os.path.join(user_config_dir, config_filename)
        return user_config_path

    @classmethod
    def load_config(cls):
        config_filename = "config.json"
        user_config_dir = appdirs.user_data_dir(APP_NAME, APP_AUTHOR)
        default_config_dir = "."

        default_config_path = os.path.abspath(os.path.join(default_config_dir, config_filename))
        user_config_path = os.path.join(user_config_dir, config_filename)

        if not os.path.exists(user_config_dir):
            os.makedirs(user_config_dir)
        if not os.path.exists(user_config_path):
            shutil.copy(default_config_path, user_config_path)

        config_file = open(user_config_path, 'r')
        config_json = config_file.read()
        config = json.loads(config_json)

        return config

    @classmethod
    def shutdown(cls):
        print "Shutting down..."
        cls.taskbar.Destroy()
        cls.lock.shutdown()

if __name__ == "__main__":
    if (len(sys.argv) == 2 and sys.argv[1] == "inserted"):
        DEBUG = True
    Badger.main()
