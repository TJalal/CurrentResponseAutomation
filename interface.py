#!/usr/bin/python
# wol.py
# -*- coding: utf-8 -*-
import objc
import sys
import WakeOnLan
#import sendMagicPacket
from time import gmtime, strftime
from datetime import datetime, timedelta
from beagle_py import *
#from Tkinter import *
#import tkSimpleDialog
import Tkinter as tk
import collections
import fileinput

from tempfile import mkstemp
from shutil import move
from os import remove, close

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

initialPath = '/users/tasfinjalal/Desktop/CTA/CTA_Old/python/'
						
																		
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)   
        self.grid()                       
        self.createWidgets()

	def createWidgets(self):
		
		# Check buttons for selecting OS to test
		self.WinXP = IntVar()
		self.WinVista = IntVar()
		self.Win7 = IntVar()
		self.Win8 = IntVar()
		self.Win10 = IntVar()
		self.orb1 = Checkbutton(master, text="WinXP", onvalue=1, offvalue=0, variable=self.WinXP)
		self.orb2 = Checkbutton(master, text="WinVista", onvalue=1, offvalue=0, variable=self.WinVista)
		self.orb3 = Checkbutton(master, text="Win7", onvalue=1, offvalue=0, variable=self.Win7)
		self.orb4 = Checkbutton(master, text="Win8", onvalue=1, offvalue=0, variable=self.Win8)
		self.orb5 = Checkbutton(master, text="Win10", onvalue=1, offvalue=0, variable=self.Win10)
		self.orb1.grid(row=6, columnspan=1,column=1, sticky=W)
		self.orb2.grid(row=6, columnspan=1,column=2, sticky=W)
		self.orb3.grid(row=7, columnspan=1,column=1, sticky=W)
		self.orb4.grid(row=7, columnspan=1,column=2, sticky=W)
		self.orb5.grid(row=7, columnspan=1,column=3, sticky=W)

		# New Labels on the UI
		Label(master, text="Device Info").grid(row=0, sticky=W)
		Label(master, text="Accessory Comb:").grid(row=3, sticky=W)
		Label(master, text="Build:").grid(row=4, sticky=W)
		Label(master, text="Email Address:").grid(row=5, sticky=W)
		Label(master, text="Operating System(s):").grid(row=6, sticky=W)
		
		# Open the defaults file where the inforamtion is stored
		defaults = open(initialPath + 'defaults.txt', 'r+')
		lines = defaults.readlines()
		
		# Variables for each field on the UI
		
		# Windows XP variables: Host IP Address, Host Username, Host Password, Host Mac Address, OS Identifier
		v1, v2, v3, v4, v5 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
		
		# Windows Vista variables: Host IP Address, Host Username, Host Password, Host Mac Address, OS Identifier
		v6, v7, v8, v9, v10 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
		
		# Windows 7 variables: Host IP Address, Host Username, Host Password, Host Mac Address, OS Identifier
		v11, v12, v13, v14, v15 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
		
		# Windows 8 variables: Host IP Address, Host Username, Host Password, Host Mac Address, OS Identifier
		v16, v17, v18, v19, v20 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
		
		# Windows 10 variables: Host IP Address, Host Username, Host Password, Host Mac Address, OS Identifier
		v21, v22, v23, v24, v25 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
		
		# Automation path, Device Info, Accessory Combination, Build, Email Address
		v26, v27, v28, v29, v30 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
		
		# Collecting default information - WindowsXP
		self.e1 = Entry(master, textvariable=v1)
		v1.set(lines[1].rstrip())
		self.e2 = Entry(master, textvariable=v2)
		v2.set(lines[2].rstrip())
		self.e3 = Entry(master, textvariable=v3)
		v3.set(lines[3].rstrip())
		self.e4 = Entry(master, textvariable=v4)
		v4.set(lines[4].rstrip())
		self.e5 = Entry(master, textvariable=v5)
		v5.set(lines[5].rstrip())

		# Collecting default information - Windows Vista
		self.e6 = Entry(master, textvariable=v6)
		v6.set(lines[8].rstrip())
		self.e7 = Entry(master, textvariable=v7)
		v7.set(lines[9].rstrip())
		self.e8 = Entry(master, textvariable=v8)
		v8.set(lines[10].rstrip())
		self.e9 = Entry(master, textvariable=v9)
		v9.set(lines[11].rstrip())
		self.e10 = Entry(master, textvariable=v10)
		v10.set(lines[12].rstrip())
		
		# Collecting default information - Windows 7
		self.e11 = Entry(master, textvariable=v11)
		v11.set(lines[15].rstrip())
		self.e12 = Entry(master, textvariable=v12)
		v12.set(lines[16].rstrip())
		self.e13 = Entry(master, textvariable=v13)
		v13.set(lines[17].rstrip())
		self.e14 = Entry(master, textvariable=v14)
		v14.set(lines[18].rstrip())
		self.e15 = Entry(master, textvariable=v15)
		v15.set(lines[19].rstrip())
		
		# Collecting default information - Windows 8
		self.e16 = Entry(master, textvariable=v16)
		v16.set(lines[22].rstrip())
		self.e17 = Entry(master, textvariable=v17)
		v17.set(lines[23].rstrip())
		self.e18 = Entry(master, textvariable=v18)
		v18.set(lines[24].rstrip())
		self.e19 = Entry(master, textvariable=v19)
		v19.set(lines[25].rstrip())
		self.e20 = Entry(master, textvariable=v20)
		v20.set(lines[26].rstrip())

		# Collecting default information - Windows 10
		self.e21 = Entry(master, textvariable=v21)
		v21.set(lines[29].rstrip())
		self.e22 = Entry(master, textvariable=v22)
		v22.set(lines[30].rstrip())
		self.e23 = Entry(master, textvariable=v23)
		v23.set(lines[31].rstrip())
		self.e24 = Entry(master, textvariable=v24)
		v24.set(lines[32].rstrip())
		self.e25 = Entry(master, textvariable=v25)
		v25.set(lines[33].rstrip())
		
		# Collecting default information - autoPath, Device Config, Accessories, Device Build, email address
		self.e26 = Entry(master, textvariable=v26)
		v26.set(lines[35].rstrip())
		self.e27 = Entry(master, textvariable=v27)
		v27.set(lines[36].rstrip())
		self.e28 = Entry(master, textvariable=v28)
		v28.set(lines[37].rstrip())
		self.e29 = Entry(master, textvariable=v29)
		v29.set(lines[38].rstrip())
		self.e30 = Entry(master, textvariable=v30)
		v30.set(lines[39].rstrip())

		# Placing fields on UI
		self.e27.grid(row=0, column=1, columnspan=5, sticky=W)
		self.e28.grid(row=3, column=1, columnspan=5, sticky=W)
		self.e29.grid(row=4, column=1, columnspan=5, sticky=W)
		self.e30.grid(row=5, column=1, columnspan=5, sticky=W)	

		
		# Radio Buttons for selecting device		
		self.selectDevice=StringVar()
		self.selectDevice.set("iPhone")
		self.drb1 = Radiobutton(master, text="iPhone", value="iPhone", variable=self.selectDevice)
		self.drb2 = Radiobutton(master, text="iPod", value="iPod", variable=self.selectDevice)
		self.drb3 = Radiobutton(master, text="iPad", value="iPad", variable=self.selectDevice)
		self.drb4 = Radiobutton(master, text="Apple Watch", value="Watch", variable=self.selectDevice)
		self.drb1.grid(row=1, columnspan=1,column=1, sticky=W)
		self.drb2.grid(row=1, columnspan=1,column=2, sticky=W)
		self.drb3.grid(row=1, columnspan=1,column=3, sticky=W)
		self.drb4.grid(row=2, columnspan=1,column=1, sticky=W)
		
		# Is the Apple Watch docked?
		self.Docked = IntVar()
		self.orb6 = Checkbutton(master, text="Docked", onvalue=1, offvalue=0, variable=self.Docked)
		self.orb6.grid(row=2, columnspan=1,column=2, sticky=W)
		
		defaults.close()	
	
	
	def buttonbox(self):
		# Setting buttons
		box = Frame(self)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)
#		w = Button(box, text="Set as Defaults", width=15, command=self.setDefault)
#		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Setup", width=10, command=self.setup)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="RUN", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()
	
	
	def setup(self):
		autoPath = self.e26.get()
		import subprocess
		subprocess.call(['open', '-a', 'TextEdit', autoPath + 'defaults.txt'])
	
	
	def setDefault(self):
		# Setting defaults if an OS is selected
		# Only the selected OS will save the new default info
		autoPath = self.e27.get()
		defaults = open(autoPath + 'defaults.txt', 'r')
		with defaults as file:
			lines = file.readlines()				
				
		if self.WinXP.get() == 1:
			lines[1] = self.e1.get()+ '\n'
			lines[2] = self.e2.get()+ '\n'
			lines[3] = self.e3.get()+ '\n'
			lines[4] = self.e4.get()+ '\n'
			lines[5] = self.e5.get()+ '\n'

		if self.WinVista.get() == 1:
			lines[8] = self.e6.get()+ '\n'
			lines[9] = self.e7.get()+ '\n'
			lines[10] = self.e8.get()+ '\n'
			lines[11] = self.e9.get()+ '\n'
			lines[12] = self.e10.get()+ '\n'
			
		if self.Win7.get() == 1:
			lines[15] = self.e11.get()+ '\n'
			lines[16] = self.e12.get()+ '\n'
			lines[17] = self.e13.get()+ '\n'
			lines[18] = self.e14.get()+ '\n'
			lines[19] = self.e15.get()+ '\n'
			
		if self.Win8.get() == 1:
			lines[22] = self.e16.get()+ '\n'
			lines[23] = self.e17.get()+ '\n'
			lines[24] = self.e18.get()+ '\n'
			lines[25] = self.e19.get()+ '\n'
			lines[26] = self.e20.get()+ '\n'
		
		if self.Win10.get() == 1:
			lines[29] = self.e21.get()+ '\n'
			lines[30] = self.e22.get()+ '\n'
			lines[31] = self.e23.get()+ '\n'
			lines[32] = self.e24.get()+ '\n'
			lines[33] = self.e25.get()+ '\n'
		
		lines[35] = self.e26.get()+ '\n'
		lines[36] = self.e27.get()+ '\n'
		lines[37] = self.e28.get()+ '\n'
		lines[38] = self.e29.get()+ '\n'
		lines[39] = self.e30.get()+ '\n'
		
		
		with open(autoPath + 'defaults.txt', 'w') as file:
			file.writelines(lines)
		defaults.close()
			
		#tkMessageBox.showinfo("Saving Defaults", "Inforamtion has been saved as defaults")	
		#master = Tk()
		#w = Message(master, text="Inforamtion has been saved as defaults", width= 300)
		#w.pack(side=LEFT, padx=5, pady=5)
		#w = Button(master, text="OK", width=10, command=self.ok, default=ACTIVE)
		#w.pack(side=LEFT, padx=5, pady=5)
		
		
	def apply(self):
		# Information that is collected are placed in tuples with their corressponding OS
		selectDevice = self.selectDevice.get()
		autoPath = self.e26.get()
		deviceConfig = self.e27.get()
		deviceOS = self.e29.get()
		emailAddress = self.e30.get()
				
		if self.WinXP.get() == 1:
			selectOS=1
			hostIPAdd, hostUserID, hostPassword, hostMacAdd, OSID, selectDevice = self.e1.get(), self.e2.get(), self.e3.get(), self.e4.get(), self.e5.get(), self.selectDevice.get()
			WinXP = collections.namedtuple('WinXP', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
			WinXPData = WinXP(selectOS, hostIPAdd, hostUserID, hostPassword, hostMacAdd, 
								OSID, selectDevice, deviceOS, deviceConfig, emailAddress)
		else:
			selectOS=0
			WinXP = collections.namedtuple('WinXP', ['a'])
			WinXPData = WinXP(selectOS)
		
		if self.WinVista.get() == 1:
			selectOS=1
			hostIPAdd, hostUserID, hostPassword, hostMacAdd, OSID, selectDevice = self.e6.get(), self.e7.get(), self.e8.get(), self.e9.get(), self.e10.get(), self.selectDevice.get()
			WinVista = collections.namedtuple('WinVista', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
			WinVistaData = WinVista(selectOS, hostIPAdd, hostUserID, hostPassword, hostMacAdd, 
										OSID, selectDevice,deviceOS, deviceConfig, emailAddress)
		else:
			selectOS=0
			WinVista = collections.namedtuple('WinVista', ['a'])
			WinVistaData = WinVista(selectOS)
		
		if self.Win7.get() == 1:
			selectOS=1
			hostIPAdd, hostUserID, hostPassword, hostMacAdd, OSID, selectDevice = self.e11.get(), self.e12.get(), self.e13.get(), self.e14.get(), self.e15.get(), self.selectDevice.get()
			Win7 = collections.namedtuple('Win7', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
			Win7Data = Win7(selectOS, hostIPAdd, hostUserID, hostPassword, hostMacAdd, 
								OSID, selectDevice, deviceOS, deviceConfig, emailAddress)
		else:
			selectOS=0
			Win7 = collections.namedtuple('Win7', ['a'])
			Win7Data = Win7(selectOS)
		
		if self.Win8.get() == 1:
			selectOS=1
			hostIPAdd, hostUserID, hostPassword, hostMacAdd, OSID, selectDevice = self.e16.get(), self.e17.get(), self.e18.get(), self.e19.get(), self.e20.get(), self.selectDevice.get()
			Win8 = collections.namedtuple('Win8', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
			Win8Data = Win8(selectOS, hostIPAdd, hostUserID, hostPassword, hostMacAdd, 
								OSID, selectDevice, deviceOS, deviceConfig, emailAddress)
		else:
			selectOS=0
			Win8 = collections.namedtuple('Win8', ['a'])
			Win8Data = Win8(selectOS)
		
		if self.Win10.get() == 1:
			selectOS=1
			hostIPAdd, hostUserID, hostPassword, hostMacAdd, OSID, selectDevice = self.e21.get(), self.e22.get(), self.e23.get(), self.e24.get(), self.e25.get(), self.selectDevice.get()
			Win10 = collections.namedtuple('Win10', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
			Win10Data = Win10(selectOS, hostIPAdd, hostUserID, hostPassword, hostMacAdd, 
								OSID, selectDevice, deviceOS, deviceConfig, emailAddress)
		else:
			selectOS=0
			Win10 = collections.namedtuple('Win10', ['a'])
			Win10Data = Win10(selectOS)
		
		self.result = WinXPData, WinVistaData, Win7Data, Win8Data, Win10Data
		
		
def userInterface():
	print "Calling userInterface() "
	# User Interface used to collect necessary information
	dialog = Application()
	#dialog = MyDialog(self)
	WinXPData = dialog.result[0]
	WinVistaData = dialog.result[1]
	Win7Data = dialog.result[2]
	Win8Data = dialog.result[3]
	Win10Data = dialog.result[4]
	dialog.mainloop()

	return WinXPData, WinVistaData, Win7Data, Win8Data, Win10Data


userInterface()