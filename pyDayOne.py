#!/usr/bin/python
# pyDayOne.py
# Made By - Nitin Khanna
# for NiKhCo
# On 1/11/2013
# GNU GPL License. Have fun!

import wx
from wxPython.wx import *
import os
import os.path
import sys
import platform
import datetime
import uuid
from plistlib import readPlist, writePlist

ID_SAVE = 1
ID_DELETE = 2
ID_NEW = 3
datetime_format =  '%Y-%m-%dT%H:%M:%SZ'

def _emptyEntry():
	return {'Creation Date': datetime.datetime.utcnow(),
	        'Entry Text':    '',
	        'Starred':       false,
	        'UUID':          str(uuid.uuid4()).replace('-', '').upper()}

class MyFrame(wx.Frame):
	all_tags = set()
	entries = {}
	timestamp_list = []
	directory = ''

	def __init__(self, parent, id, title):
		saveFileName = 'DayOne.sav'
		try:
			from win32com.shell import shell, shellcon
			saveFileDir = os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, None, 0), 'pyDayOne')
		except ImportError:
			saveFileDir = os.path.expanduser('~/.pyDayOne')

		if not(os.path.exists(saveFileDir)):
			os.makedirs(saveFileDir)
		saveFileName = os.path.join(saveFileDir, saveFileName)

		try:
			settings = readPlist(saveFileName)
			self.directory = settings['directory']
		except:
			if platform.system() == 'Windows':
				directory =  os.path.abspath(os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_PROFILE, None, 0),
				                                          r'Dropbox/Apps/Day One/Journal.dayone/entries/'))
				if os.path.exists(directory):
					self.directory = directory
				else:
					wx.MessageBox('Windows Dropbox folder not found. Please select the entries directory of Day One. It will be under Dropbox -> Apps -> Day One -> Journal.dayone -> entries', 'Error', wx.OK | wx.ICON_EXCLAMATION)
					dialog = wx.DirDialog(None, "Choose the Day One entries directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
					if dialog.ShowModal() == wx.ID_OK:
						self.directory = dialog.GetPath()
						self.directory = self.directory+'\\'
						self.directory.replace('\\','/')
				writePlist({'directory':directory}, saveFileName)
			elif platform.system() == 'Linux':
				directory = os.path.expanduser('~/Dropbox/Apps/Day One/Journal.dayone/entries/')
				if os.path.exists(directory):
					self.directory = directory
				else:
					wx.MessageBox('Linux Dropbox folder not found. Please select the entries directory of Day One. It will be under Dropbox -> Apps -> Day One -> Journal.dayone -> entries', 'Error', wx.OK | wx.ICON_EXCLAMATION)
					dialog = wx.DirDialog(None, "Choose the Day One entries directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
					if dialog.ShowModal() == wx.ID_OK:
						self.directory = dialog.GetPath()
						self.directory = self.directory+'\\'
						self.directory.replace('\\','/')
				writePlist({'directory':directory}, saveFileName)
			else:
				wx.MessageBox('Dropbox folder not found. Please select the entries directory of Day One. It will be under Dropbox -> Apps -> Day One -> Journal.dayone -> entries', 'Error', wx.OK | wx.ICON_EXCLAMATION)
				dialog = wx.DirDialog(None, "Choose the Day One entries directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
				if dialog.ShowModal() == wx.ID_OK:
					self.directory = dialog.GetPath()
					self.directory = self.directory+'\\'
					self.directory.replace('\\','/')
				writePlist({'directory':directory}, saveFileName)

		wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (800, 800))
		fn = os.path.join(os.path.dirname(sys.argv[0]), 'pyDayOne.ico')
		self.icon = wx.Icon(fn, wx.BITMAP_TYPE_ICO)
		self.SetIcon(self.icon)

		for root,dirs,files in os.walk(self.directory):
			del dirs[:]
			for file in files:
				(filename, _) = os.path.splitext(file)
				this_entry = readPlist(os.path.join(root, file))
				if (('Creation Date' in this_entry) and ('Entry Text' in this_entry) and
				    ('UUID' in this_entry) and (this_entry['UUID'] == filename)):
					self.entries[this_entry['Creation Date'].strftime(datetime_format)] = this_entry
					curr_tags = set(this_entry.get('Tags', []))
					self.all_tags |= curr_tags
		keylist = self.entries.keys()
		keylist.sort(reverse=True)

		for key in keylist:
			self.timestamp_list.append(key)

		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		panel = wx.Panel(self, -1)
		self.entry_list = wx.ListBox(panel, 26, wx.DefaultPosition, (170, 630), self.timestamp_list, wx.LB_SINGLE)
		self.text = wx.TextCtrl(panel, -1, '', size=(500, 630), style=wx.TE_MULTILINE)

		self.entry_list.SetSelection(0)
		selected_dt = self.entry_list.GetString(0)
		self.text.SetValue(self.entries[selected_dt]['Entry Text'])

		newBtn = wx.Button(panel, ID_NEW, "New")
		saveBtn = wx.Button(panel, ID_SAVE, "Save")
		btn = wx.Button(panel, wx.ID_CLOSE, 'Close')

		hbox1.Add(self.entry_list, 0, wx.LEFT | wx.TOP, 40)
		hbox1.Add(self.text, 1, wx.LEFT | wx.TOP, 40)

		hbox3.Add(newBtn, 0, wx.ALIGN_CENTER | wx.TOP, 20)
		hbox3.Add(saveBtn, 1, wx.ALIGN_CENTER | wx.TOP, 20)
		hbox3.Add(btn, 2, wx.ALIGN_CENTER | wx.TOP, 20)

		vbox.Add(hbox1, 0, wx.ALIGN_LEFT)
		vbox.Add(hbox3, 1, wx.ALIGN_CENTRE)
		panel.SetSizer(vbox)

		self.Bind(wx.EVT_BUTTON, self.OnNew, id=ID_NEW)
		self.Bind(wx.EVT_BUTTON, self.OnSave, id=ID_SAVE)
		self.Bind(wx.EVT_BUTTON, self.OnClose, id=wx.ID_CLOSE)
		self.Bind(wx.EVT_LISTBOX, self.OnSelect, id=26)

	def OnClose(self, event):
		self.Close()

	def OnNew(self, event):
		new_entry = _emptyEntry()
		entry_dt = new_entry['Creation Date'].strftime(datetime_format)
		self.entries[entry_dt] = new_entry
		self.entry_list.Insert(entry_dt, 0)
		self.text.Clear()
		self.entry_list.SetSelection(0)

	def OnSave(self, event):
		index = self.entry_list.GetSelection()
		if index == wxNOT_FOUND:
			return
		selected_time = self.entry_list.GetString(index)
		selected_entry = self.entries[selected_time]
		selected_entry['Entry Text'] = self.text.GetValue()
		saveToPath = os.path.join(self.directory, selected_entry['UUID']+'.doentry')
		writePlist(selected_entry, saveToPath)

	def OnSelect(self, event):
		index = event.GetSelection()
		selected_entry = self.entry_list.GetString(index)
		self.text.SetValue(self.entries[selected_entry]['Entry Text'])

	def OnTimer(self, event):
		ct = gmtime()
		print_time = (ct[0], ct[1], ct[2], ct[3]+self.diff, ct[4], ct[5], ct[6], ct[7], -1)
		self.time.SetLabel(strftime("%H:%M:%S", print_time))

class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, -1, 'pyDayOne')
		frame.Centre()
		frame.Show(True)
		return True

app = MyApp(0)
app.MainLoop()
