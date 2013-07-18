#!/usr/bin/env python

# pyDayOne.py
# Made By - Nitin Khanna
# for NiKhCo
# On 7/17/2013
# GNU GPL License. Have fun! 

import pygtk
pygtk.require('2.0')
import gtk, gobject
import os
import getpass
import platform
import xml.etree.ElementTree as ET
import datetime
import uuid
import re

#os.environ['PATH'] += ";gtk/lib;gtk/bin"

class pyDayOneGTK:
	the_dict = {}
	uuid_dict = {}		# holds all the UUIDs with timestamps as keys
	the_list = []		# stores the timestamps as keys to show in the GUI CList
	sorted_dict = {}	# stores the entries with the timestamps as keys
	found_entry = False
	found_UUID = False
	directory = ''
	myUUID = ''
	timestamp = ''

	def close_application(self, widget):
		gtk.main_quit()

	def callback(self, widget):
		print self.textbuffer.get_text(self.textbuffer.get_start_iter() , self.textbuffer.get_end_iter())

	def reset(self):
		self.label.set_text("")

	def selection_made(self, clist, row, column, event, data=None):
		# Get the text that is stored in the selected row and column
		# which was clicked in. We will receive it as a pointer in the
		# argument text.
		self.timestamp = self.clist.get_text(row, column)
		self.myUUID = self.uuid_dict[self.timestamp]
		self.textbuffer.set_text(self.sorted_dict[self.timestamp])
		#print self.sorted_dict[self.timestamp]
		print self.myUUID
		# Just prints some information about the selected row
		print ("You selected row %d and the text is %s\n" % (row, self.timestamp))
		return

	def selected_new(self, widget):
		now = datetime.datetime.utcnow()
		theUUID = uuid.uuid4()
		self.myUUID = re.sub('[-]', '', str(theUUID))
		self.myUUID = self.myUUID.swapcase()
		print self.myUUID
		item = now.strftime("%Y-%m-%dT%H:%M:%SZ")
		print item
		pos = 0
		self.textbuffer.delete(self.textbuffer.get_start_iter() , self.textbuffer.get_end_iter())
		self.sorted_dict[item] = ""
		self.uuid_dict[item] = self.myUUID
		self.clist.insert(pos, [item])
		self.clist.select_row(0,0)


	def save(self, widget):
		self.label.set_text("Saving")
		try:
			with open(self.directory+self.myUUID+'.doentry', 'w+') as f:
				#print "came in with"
				#f.close()
				tree = ET.parse(self.directory+self.myUUID+'.doentry')
				#print "tree parse began"
				root = tree.getroot()
				if child.text == 'Entry Text':
					self.found_entry = True
				if child.tag == 'string' and self.found_entry:
					child.text = self.textbuffer.get_text(self.textbuffer.get_start_iter() , self.textbuffer.get_end_iter())
					self.found_entry = False
				tree.write(self.directory+self.myUUID+'.doentry')
		except:
			self.uuid_dict[self.timestamp] = self.myUUID
			self.sorted_dict[self.timestamp] = self.textbuffer.get_text(self.textbuffer.get_start_iter() , self.textbuffer.get_end_iter())
			#print self.textbuffer.get_text(self.textbuffer.get_start_iter() , self.textbuffer.get_end_iter())

			plist = ET.Element('plist')
			plist.attrib = {'version':"1.0"}
			b = ET.SubElement(plist, 'dict')
			
			c = ET.SubElement(b, 'key')
			c.text = 'Creation Date'
			d = ET.SubElement(b, 'date')
			d.text = str(self.timestamp)
				
			e = ET.SubElement(b, 'key')
			e.text = 'Entry Text'
			f = ET.SubElement(b, 'string')
			f.text = self.textbuffer.get_text(self.textbuffer.get_start_iter() , self.textbuffer.get_end_iter())
				
			g = ET.SubElement(b, 'key')
			g.text = 'Starred'
			h = ET.SubElement(b, 'false')
			
			i = ET.SubElement(b, 'key')
			i.text = 'UUID'
			j = ET.SubElement(b, 'string')
			j.text = self.myUUID
				
			file = open(self.directory+self.myUUID+'.doentry', 'w')
			XMLL = """<?xml version="1.0" encoding="UTF-8"?>"""
			DTD = """<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">"""
			file.write(XMLL + "\n")
			file.write(DTD + "\n")
			ET.ElementTree(plist).write(file)

		self.label.set_text("Saved")
		gobject.timeout_add_seconds(3, self.reset)

	def __init__(self):
		savefile = open('DayOne.sav', 'w+')
		try:
			tree = ET.parse(savefile)
			root = tree.getroot()
			self.directory = root.text
		except:
			#print "savefile not found"
			#print platform.system()
			if platform.system() == 'Windows':
				#print "system is windows"
				directory = 'C:\\Users\\'+getpass.getuser()+'\\Dropbox\\Apps\\Day One\\Journal.dayone\\entries\\'
				if os.path.exists(directory):
					self.directory = directory
				else:
					message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
					message.set_markup("Day One entries folder not found. Please select the entries directory of Day One. It should be under Dropbox -> Apps -> Day One -> Journal.dayone -> entries")
					response = message.run()
					message.destroy()
					dialog = gtk.FileChooserDialog("Choose entries directory:",action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
					response = dialog.run()
					if response == gtk.RESPONSE_OK:
						#print dialog.get_current_folder(), 'selected'
						self.directory = dialog.get_current_folder()
					elif response == gtk.RESPONSE_CANCEL:
						#print 'Closed, no files selected'
						message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
						message.set_markup("No folder was selected. I can't work like this!")
						response = message.run()
						message.destroy()
						gtk.main_quit()
					dialog.destroy()
			else:
				message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
				message.set_markup("Day One entries folder not found. Please select the entries directory of Day One. It should be under Dropbox->Apps->Day One->Journal.dayone->entries")
				message.run()
				dialog = gtk.FileChooserDialog("Choose entries directory:",action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
				response = dialog.run()
				if response == gtk.RESPONSE_OK:
					#print dialog.get_current_folder(), 'selected'
					self.directory = dialog.get_current_folder()
				elif response == gtk.RESPONSE_CANCEL:
					#print 'Closed, no files selected'
					message = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
					message.set_markup("No folder was selected. I can't work like this!")
					response = message.run()
					message.destroy()
					gtk.main_quit()
				dialog.destroy()
			dir = ET.Element('directory')
			dir.text = self.directory
			ET.ElementTree(dir).write(savefile)

		for root,dirs,files in os.walk(self.directory):
			for file in files:
				print file
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

		# for index, item in enumerate(self.the_list):
		# 	print index, item

		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_resizable(True)
		window.connect("destroy", self.close_application)
		window.set_title("pyDayOne - Your Day One, on Windows")
		window.set_border_width(0)
		window.set_size_request(500, 500)

		box1 = gtk.VBox(False, 0)
		window.add(box1)
		box1.show()

		box2 = gtk.HBox(False, 10)
		box2.set_border_width(10)
		box1.pack_start(box2, True, True, 0)
		box2.show()

		sw1 = gtk.ScrolledWindow()
		sw1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		
		title = ["Entries"]
		self.clist = gtk.CList( 1, title)
		self.clist.connect("select_row", self.selection_made)
		self.clist.set_selection_mode(gtk.SELECTION_SINGLE)
		self.clist.set_shadow_type(gtk.SHADOW_OUT)
		self.clist.set_column_width(0, 50)
		sw1.add(self.clist)
		sw1.show()
		self.clist.show()
		box2.pack_start(sw1)

		sw2 = gtk.ScrolledWindow()
		sw2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.textbuffer = gtk.TextBuffer()
		textview = gtk.TextView(self.textbuffer)
		textview.set_wrap_mode(gtk.WRAP_WORD)
		#textbuffer = textview.get_buffer()
		sw2.add(textview)
		sw2.show()
		textview.show()
		box2.pack_start(sw2)
		
		separator = gtk.HSeparator()
		box1.pack_start(separator, False, True, 0)
		separator.show()

		table = gtk.Table(2, 2, True)
		box1.pack_start(table, False, True, 0)

		self.label = gtk.Label('')
		table.attach(self.label, 0, 1, 0, 1)
		self.label.show()

		button1 = gtk.Button("New")
		button1.connect("clicked", self.selected_new)
		table.attach(button1, 0, 1, 1, 2)
		button1.show()

		button2 = gtk.Button("Save")
		button2.connect("clicked", self.save)
		table.attach(button2, 1, 2, 1, 2)
		button2.show()

		table.show()
		window.show()

		for index, item in enumerate(self.the_list):
			#print item
			self.clist.append([item])
			#clist.insert(index, item)
			#print clist.get_text(index, 0)

def main():
	gtk.main()
	return 0

if __name__ == "__main__":
	pyDayOneGTK()
	main()
