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
import getpass
import platform
import xml.etree.ElementTree as ET
#import wx.lib.inspection
import datetime
import uuid
import re

ID_SAVE = 1
ID_DELETE = 2
ID_NEW = 3

plist_header = ["""<?xml version="1.0" encoding="UTF-8"?>\n""",
                """<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n"""]


class MyFrame(wx.Frame):
	the_dict = {}
	uuid_dict = {}
	the_list = []
	sorted_dict = {}
	found_entry = False
	found_UUID = False
	directory = ''
	myUUID = ''

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

		savefile = open(saveFileName, 'w+')
		try:
			tree = ET.parse(savefile)
			root = tree.getroot()
			self.directory = root.text
		except:
			if platform.system() == 'Windows':
				directory = 'C:\\Users\\'+getpass.getuser()+'\\Dropbox\\Apps\\Day One\\Journal.dayone\\entries\\'
				if os.path.exists(directory):
					self.directory = directory
				else:
					wx.MessageBox('Windows Dropbox folder not found. Please select the entries directory of Day One. It will be under Dropbox -> Apps -> Day One -> Journal.dayone -> entries', 'Error', wx.OK | wx.ICON_EXCLAMATION)
					dialog = wx.DirDialog(None, "Choose the Day One entries directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
					if dialog.ShowModal() == wx.ID_OK:
						self.directory = dialog.GetPath()
						self.directory = self.directory+'\\'
						self.directory.replace('\\','/')
				dir = ET.Element('directory')
				dir.text = self.directory
				ET.ElementTree(dir).write(savefile)
			elif platform.system() == 'Linux':
				directory = '~/Dropbox/Apps/Day One/Journal.dayone/entries/'
				if os.path.exists(directory):
					self.directory = directory
				else:
					wx.MessageBox('Linux Dropbox folder not found. Please select the entries directory of Day One. It will be under Dropbox -> Apps -> Day One -> Journal.dayone -> entries', 'Error', wx.OK | wx.ICON_EXCLAMATION)
					dialog = wx.DirDialog(None, "Choose the Day One entries directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
					if dialog.ShowModal() == wx.ID_OK:
						self.directory = dialog.GetPath()
						self.directory = self.directory+'\\'
						self.directory.replace('\\','/')
				dir = ET.Element('directory')
				dir.text = self.directory
				ET.ElementTree(dir).write(savefile)
			else:
				wx.MessageBox('Dropbox folder not found. Please select the entries directory of Day One. It will be under Dropbox -> Apps -> Day One -> Journal.dayone -> entries', 'Error', wx.OK | wx.ICON_EXCLAMATION)
				dialog = wx.DirDialog(None, "Choose the Day One entries directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
				if dialog.ShowModal() == wx.ID_OK:
					self.directory = dialog.GetPath()
					self.directory = self.directory+'\\'
					self.directory.replace('\\','/')
				dir = ET.Element('directory')
				dir.text = self.directory
				ET.ElementTree(dir).write(savefile)

		wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, (800, 800))
		fn = os.path.join(os.path.dirname(sys.argv[0]), 'pyDayOne.ico')
		self.icon = wx.Icon(fn, wx.BITMAP_TYPE_ICO)
		self.SetIcon(self.icon)

		for root,dirs,files in os.walk(self.directory):
			for file in files:
				#print file
				if file.endswith(".doentry"):
					tree = ET.parse(self.directory+file)
					root = tree.getroot()
					for child in root[0]:
						#print child.tag, child.text
						if child.tag == 'date':
							tempdate = child.text
						if child.text == 'Entry Text':
							self.found_entry = True
						if child.text == 'UUID':
							self.found_UUID = True
						if child.tag == 'string' and self.found_UUID and tempdate != '':
							self.uuid_dict[tempdate] = child.text
							self.found_UUID = False
						if child.tag == 'string' and self.found_entry and tempdate != '':
							self.the_dict[tempdate] = child.text
							self.found_entry = False
		keylist = self.the_dict.keys()
		keylist.sort(reverse=True)

		for key in keylist:
			self.sorted_dict[key] = self.the_dict[key]
			self.the_list.append(key)

		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		panel = wx.Panel(self, -1)
		self.entry_list = wx.ListBox(panel, 26, wx.DefaultPosition, (170, 630), self.the_list, wx.LB_SINGLE)
		self.text = wx.TextCtrl(panel, -1, '', size=(500, 630), style=wx.TE_MULTILINE)

		self.entry_list.SetSelection(0)
		single_entry = self.entry_list.GetString(0)
		self.text.SetValue(self.sorted_dict[single_entry])
		self.myUUID = self.uuid_dict[single_entry]

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
		now = datetime.datetime.utcnow()
		theUUID = uuid.uuid4()
		self.myUUID = re.sub('[-]', '', str(theUUID))
		self.myUUID = self.myUUID.swapcase()
		item = now.strftime("%Y-%m-%dT%H:%M:%SZ")
		pos = 0
		self.entry_list.Insert(item, pos)
		self.entry_list.SetSelection(0)
		self.text.Clear()

	def OnSave(self, event):

		try:
			tree = ET.parse(self.directory+self.myUUID+'.doentry')
			root = tree.getroot()
			self.found_entry = false
			for child in root[0]:
				if child.text == 'Entry Text':
					self.found_entry = True
				if child.tag == 'string' and self.found_entry:
					child.text = self.text.GetValue()
					self.found_entry = False
			tree.write(self.directory+self.myUUID+'.doentry')
		except:
			def indent(elem, level=0):
			    i = "\n" + level*"  "
			    if len(elem):
			        if not elem.text or not elem.text.strip():
			            elem.text = i + "  "
			        if not elem.tail or not elem.tail.strip():
			            elem.tail = i
			        for elem in elem:
			            indent(elem, level+1)
			        if not elem.tail or not elem.tail.strip():
			            elem.tail = i
			    else:
			        if level and (not elem.tail or not elem.tail.strip()):
			            elem.tail = i

			self.uuid_dict[self.entry_list.GetString(self.entry_list.GetSelection())] = self.myUUID
			self.sorted_dict[self.entry_list.GetString(self.entry_list.GetSelection())] = self.text.GetValue()

			plist = ET.Element('plist')
			plist.attrib = {'version': '1.0'}
			b = ET.SubElement(plist, 'dict')

			c = ET.SubElement(b, 'key')
			c.text = 'Creation Date'
			d = ET.SubElement(b, 'date')
			d.text = str(self.entry_list.GetString(self.entry_list.GetSelection()))

			e = ET.SubElement(b, 'key')
			e.text = 'Entry Text'
			f = ET.SubElement(b, 'string')
			f.text = self.text.GetValue()

			g = ET.SubElement(b, 'key')
			g.text = 'Starred'
			h = ET.SubElement(b, 'false')

			i = ET.SubElement(b, 'key')
			i.text = 'UUID'
			j = ET.SubElement(b, 'string')
			j.text = self.myUUID

			indent(plist)
			file = open(self.directory+self.myUUID+'.doentry', 'w')
			file.writelines(plist_header)
			file.writelines(ET.tostringlist(plist))
			file.close()

	def OnSelect(self, event):
		index = event.GetSelection()
		single_entry = self.entry_list.GetString(index)
		self.text.SetValue(self.sorted_dict[single_entry])
		self.myUUID = self.uuid_dict[single_entry]

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
