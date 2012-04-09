from BadgerState import *
from PrintHandler import *
from BadgerDispatcher import *
from LockMonitor import *
from SoundHandler import *
from EmailHandler import *
import time
import json
import wx

APP_NAME = "Badger"
VERSION = 0.2
TRAY_TOOLTIP = "Badger!"
TRAY_ICON = 'badger.png'

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

handler_map = {"SoundHandler": SoundHandler, "PrintHandler": PrintHandler, "EmailHandler": EmailHandler}
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
	state = BadgerState()
	printhandler = PrintHandler()
	dispatcher = BadgerDispatcher(state)
	#set up handlers
	for handler in handlers:
		handler_name = handler.get("name", "NO_HANDLER")
		if handler_name not in handler_map:
			print "Skipping unrecognized handler: %s" % (handler_name)
			continue
		handler_type = handler_map[handler_name]
		dispatcher.add_handler(handler_type(config = handler.get("config", None)))
		print "Added handler: %s" % handler_name
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

	TaskBarIcon()
	app.MainLoop()

	print "Shutting down..."

	lock.shutdown()

if __name__ == "__main__": main()