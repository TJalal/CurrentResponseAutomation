#!/usr/bin/python
# wol.py
# -*- coding: utf-8 -*-
import objc
import sys
import traceback
import WakeOnLan
#import sendMagicPacket
from time import gmtime, strftime, sleep
from datetime import datetime, timedelta
from beagle_py import *
from Tkinter import *
import tkSimpleDialog
import collections
import fileinput
import Tkinter
import pexpect 
from pexpect import popen_spawn
import subprocess

from tempfile import mkstemp
from shutil import move
from os import remove, close
from os import listdir
from os.path import isfile, join
import glob
import easygui
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

global Errorlogs
Errorlogs = ""
initialPath = os.getcwd() + '/Documents/Projects/CurrentResponseAutomation/'
sshPath = '/users/' + os.getlogin() + '/.ssh/'

# Color and Format for Terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.FAIL = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
																							
class MyDialog(tkSimpleDialog.Dialog):


	def body(self, master):
		
		# Check buttons for selecting OS to test
		self.WinXP = IntVar()
		self.WinVista = IntVar()
		self.Win7 = IntVar()
		self.Win8 = IntVar()
		self.Win10 = IntVar()
		#self.orb1 = Checkbutton(master, text="WinXP", onvalue=1, offvalue=0, variable=self.WinXP)
		#self.orb2 = Checkbutton(master, text="WinVista", onvalue=1, offvalue=0, variable=self.WinVista)
		self.orb3 = Checkbutton(master, text="Win7", onvalue=1, offvalue=0, variable=self.Win7)
		self.orb4 = Checkbutton(master, text="Win8", onvalue=1, offvalue=0, variable=self.Win8)
		self.orb5 = Checkbutton(master, text="Win10", onvalue=1, offvalue=0, variable=self.Win10)
		#self.orb1.grid(row=6, columnspan=1,column=1, sticky=W)
		#self.orb2.grid(row=6, columnspan=1,column=2, sticky=W)
		self.orb3.grid(row=7, columnspan=1,column=1, sticky=W)
		self.orb4.grid(row=7, columnspan=1,column=2, sticky=W)
		self.orb5.grid(row=7, columnspan=1,column=3, sticky=W)

		# Setting Win7, Win8 and Win10 as defaults
		self.orb3.select()
		self.orb4.select()
		self.orb5.select()

		# New Labels on the UI
		Label(master, text="Device Info:").grid(row=0, sticky=W)
		Label(master, text="Accessory Comb:").grid(row=4, sticky=W)
		Label(master, text="Build:").grid(row=5, sticky=W)
		Label(master, text="Email Address:").grid(row=6, sticky=W)
		Label(master, text="Operating Systems:").grid(row=7, sticky=W)
		
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
		self.e27.grid(row=0, column=1, columnspan=2, sticky=W)
		self.e27.focus_set()
		self.e28.grid(row=4, column=1, columnspan=2, sticky=W)
		self.e29.grid(row=5, column=1, columnspan=2, sticky=W)
		self.e30.grid(row=6, column=1, columnspan=2, sticky=W)	

		
		# Radio Buttons for selecting device		
		self.selectDevice=StringVar()
		self.selectDevice.set("iPhone")
		self.drb1 = Radiobutton(master, text="iPhone", value="iPhone", variable=self.selectDevice, command=self.disableDocked)
		self.drb2 = Radiobutton(master, text="iPod", value="iPod", variable=self.selectDevice, command=self.disableDocked)
		self.drb3 = Radiobutton(master, text="Apple Watch", value="Watch", variable=self.selectDevice, command=self.enableDocked)
		self.drb4 = Radiobutton(master, text="iPad", value="iPad", variable=self.selectDevice, command=self.disableDocked)
		self.drb5 = Radiobutton(master, text="iPad Mini", value="iPadMini", variable=self.selectDevice, command=self.disableDocked)
		self.drb6 = Radiobutton(master, text="iPad Pro", value="iPadPro", variable=self.selectDevice, command=self.disableDocked)

		self.drb1.grid(row=1, columnspan=1,column=1, sticky=W)
		self.drb2.grid(row=2, columnspan=1,column=1, sticky=W)
		self.drb3.grid(row=1, columnspan=1,column=2, sticky=W)
		self.drb4.grid(row=3, columnspan=1,column=1, sticky=W)
		self.drb5.grid(row=2, columnspan=1,column=2, sticky=W)
		self.drb6.grid(row=3, columnspan=1,column=2, sticky=W)
		
		# Is the Apple Watch docked?
		self.docked = IntVar()
		self.orb6 = Checkbutton(master, text="Docked", onvalue=1, offvalue=0, variable=self.docked, state= DISABLED)
		self.orb6.grid(row=1, columnspan=1,column=3, sticky=W)
		
		# Is it a Charging Port?
		self.chargingPort = IntVar()
		self.orb7 = Checkbutton(master, text="Charging Port", onvalue=1, offvalue=0, variable=self.chargingPort)
		self.orb7.grid(row=2, columnspan=1,column=3, sticky=W)

		self.amds = IntVar()
		self.orb8 = Checkbutton(master, text="AMDS", onvalue=1, offvalue=0, variable=self.amds)
		self.orb8.grid(row=3, columnspan=1,column=3, sticky=W)

		defaults.close()	
	
	
	def enableDocked(self):
		self.orb6.config(state=NORMAL)

	def disableDocked(self):
		self.orb6.config(state=DISABLED)


	def buttonbox(self):
		# Setting buttons
		box = Frame(self)
		w = Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Setup", width=10, command=self.setup)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="RUN", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()
		#w = Button(box, text="Set as Defaults", width=15, command=self.setDefault)
		#w.pack(side=LEFT, padx=5, pady=5)
	
	
	def setup(self):
		autoPath = self.e26.get()
		import subprocess
		subprocess.call(['open', '-a', 'TextEdit', autoPath + 'defaults.txt'])
	
	
	def setDefault(self):
		# Setting defaults if an OS is selected
		# Only the selected OS will save the new default info
		autoPath = self.e26.get()
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
		accessories = self.e28.get()
		deviceOS = self.e29.get()
		emailAddress = self.e30.get()
		docked = self.docked.get()
		chargingPort = self.chargingPort.get()
		amds = self.amds.get()
				
		# if self.WinXP.get() == 1:
		# 	selectOS=1
		# 	hostIPAdd, hostUserID, hostPassword, hostMacAdd, OSID, selectDevice = self.e1.get(), self.e2.get(), self.e3.get(), self.e4.get(), self.e5.get(), self.selectDevice.get()
		# 	WinXP = collections.namedtuple('WinXP', ['selected_OS', 'host_IP_address', 'host_user_ID', 'host_password', 'host_Mac_Address', 'OperatingSystem_ID', 'selected_device', 'is_docked', 'is_charging_port', 'device_build', 'device_config', 'email_address'])
		# 	WinXPData = WinXP(selectOS, hostIPAdd, hostUserID, hostPassword, hostMacAdd, 
		# 						OSID, selectDevice, docked, chargingPort, deviceOS, deviceConfig, emailAddress)
		# else:
		# 	selectOS=0
		# 	WinXP = collections.namedtuple('WinXP', ['selected_OS'])
		# 	WinXPData = WinXP(selectOS)
		
		# if self.WinVista.get() == 1:
		# 	selectOS=1
		# 	hostIPAdd, hostUserID, hostPassword, hostMacAdd, OSID, selectDevice = self.e6.get(), self.e7.get(), self.e8.get(), self.e9.get(), self.e10.get(), self.selectDevice.get()
		# 	WinVista = collections.namedtuple('WinVista', ['selected_OS', 'host_IP_address', 'host_user_ID', 'host_password', 'host_Mac_Address', 'OperatingSystem_ID', 'selected_device', 'is_docked', 'is_charging_port', 'device_build', 'device_config', 'email_address'])
		# 	WinVistaData = WinVista(selectOS, hostIPAdd, hostUserID, hostPassword, hostMacAdd, 
		# 								OSID, selectDevice, docked, chargingPort, deviceOS, deviceConfig, emailAddress)
		# else:
		# 	selectOS=0
		# 	WinVista = collections.namedtuple('WinVista', ['selected_OS'])
		# 	WinVistaData = WinVista(selectOS)
		
		if self.Win7.get() == 1:
			selectOS=1
			hostIPAdd, hostUserID, hostPassword, hostMacAdd, OSID, selectDevice = self.e11.get(), self.e12.get(), self.e13.get(), self.e14.get(), self.e15.get(), self.selectDevice.get()
			Win7 = collections.namedtuple('Win7', ['selected_OS', 'host_IP_address', 'host_user_ID', 'host_password', 'host_Mac_Address', 'OperatingSystem_ID', 'selected_device', 'is_docked', 'is_charging_port', 'device_build', 'device_config', 'email_address'])
			Win7Data = Win7(selectOS, hostIPAdd, hostUserID, hostPassword, hostMacAdd, 
								OSID, selectDevice, docked, chargingPort, deviceOS, deviceConfig, emailAddress)
		else:
			selectOS=0
			Win7 = collections.namedtuple('Win7', ['selected_OS'])
			Win7Data = Win7(selectOS)
		
		if self.Win8.get() == 1:
			selectOS=1
			hostIPAdd, hostUserID, hostPassword, hostMacAdd, OSID, selectDevice = self.e16.get(), self.e17.get(), self.e18.get(), self.e19.get(), self.e20.get(), self.selectDevice.get()
			Win8 = collections.namedtuple('Win8', ['selected_OS', 'host_IP_address', 'host_user_ID', 'host_password', 'host_Mac_Address', 'OperatingSystem_ID', 'selected_device', 'is_docked', 'is_charging_port', 'device_build', 'device_config', 'email_address'])
			Win8Data = Win8(selectOS, hostIPAdd, hostUserID, hostPassword, hostMacAdd, 
								OSID, selectDevice, docked, chargingPort, deviceOS, deviceConfig, emailAddress)
		else:
			selectOS=0
			Win8 = collections.namedtuple('Win8', ['selected_OS'])
			Win8Data = Win8(selectOS)
		
		if self.Win10.get() == 1:
			selectOS=1
			hostIPAdd, hostUserID, hostPassword, hostMacAdd, OSID, selectDevice = self.e21.get(), self.e22.get(), self.e23.get(), self.e24.get(), self.e25.get(), self.selectDevice.get()
			Win10 = collections.namedtuple('Win10', ['selected_OS', 'host_IP_address', 'host_user_ID', 'host_password', 'host_Mac_Address', 'OperatingSystem_ID', 'selected_device', 'is_docked', 'is_charging_port', 'device_build', 'device_config', 'email_address'])
			Win10Data = Win10(selectOS, hostIPAdd, hostUserID, hostPassword, hostMacAdd, 
								OSID, selectDevice, docked, chargingPort, deviceOS, deviceConfig, emailAddress)
		else:
			selectOS=0
			Win10 = collections.namedtuple('Win10', ['selected_OS'])
			Win10Data = Win10(selectOS)
		
		self.result = Win7Data, Win8Data, Win10Data

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(initialPath + "logfile.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    

#################################################################################################################		
# Miscellaneous variables and commands
hostPCDate = strftime("%m/%d/%Y", gmtime())
mins_from_now = datetime.now() + timedelta(minutes=7)
hostPCOldTime = '{:%H:%M:%S}'.format(datetime.now()) #strftime("%H:%M:%S", gmtime())
hostPCTime = '{:%H:%M}'.format(mins_from_now)

def timeStamp():
	hostPCDate = strftime("%m/%d/%Y", gmtime())
	hostPCTime = '{:%H:%M:%S}'.format(datetime.now())
	timeStamp = (bcolors.OKBLUE + "[" + str(hostPCDate) + " " + str(hostPCTime) + "] " + bcolors.ENDC)
	return timeStamp

def userInterface():
	# User Interface used to collect necessary information
	root = Tkinter.Tk()
	root.title("Current Response Automation")
	root.withdraw()
	dialog = MyDialog(root)
	#print dialog.result
	WinXPData = dialog.result[0]
	WinVistaData = dialog.result[1]
	Win7Data = dialog.result[2]
	Win8Data = dialog.result[3]
	Win10Data = dialog.result[4]
	#root.attributes("-topmost", True)
	#dialog.mainloop()
	#print "after main loop"
	return WinXPData, WinVistaData, Win7Data, Win8Data, Win10Data

def MainTest(OS, hostIPAddress, hostUserID, hostPassword, macAddress, OSID, selectDevice, docked, chargingPort, deviceOS, deviceConfig, entries):
	try:
		print timeStamp() + "Calling MainTest for OS ", OS
		removeKnownHosts(sshPath)
		sleep(3)
		stateCheck(hostUserID, hostIPAddress, hostPassword, "Awake")
		extractCurrent("Awake", OS, selectDevice, docked, chargingPort, deviceConfig, entries)
		sleepHibernate(hostUserID, hostIPAddress,hostPassword,0) #sleep
		sleep(60)
		stateCheck(hostUserID, hostIPAddress, hostPassword, "Sleep")
		extractCurrent("Sleep", OS, selectDevice, docked, chargingPort, deviceConfig, entries)
		wakeComputer(macAddress)
		sleep(30)
		sleepHibernate(hostUserID, hostIPAddress,hostPassword,1) #hibernate
		sleep(60)
		stateCheck(hostUserID, hostIPAddress, hostPassword, "Hibernate")
		extractCurrent("Hibernate", OS, selectDevice, docked, chargingPort, deviceConfig, entries)
		sleep(60)
	except SystemExit:
		sys.exit()
	except:
		print '-'*60 + '\n'
		e = sys.exc_info()[0]
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in sendCommand: ",  "%s" % e
		print "Exception in user code:"
		print traceback.format_exc()
		print '-'*60 + '\n'

def stateCheck(hostUserID, hostIPAddress, hostPassword, state):
	for j in range(3):
		try: 
			print timeStamp() + "SSHing into Host PC"
			ssh_newkey = 'Are you sure you want to continue connecting'
			child = pexpect.spawn('ssh ' + hostUserID + '@'+ hostIPAddress)

			i=child.expect([ssh_newkey,'password:',pexpect.EOF])
			if i==0:
			    print timeStamp() + "Continue connecting to host PC"
			    child.sendline('yes')
			    i=child.expect([ssh_newkey,'password:',pexpect.EOF])
			if i==1:
			    print timeStamp() + "Sending password\n",
			    child.sendline(hostPassword)
			    #child.expect(pexpect.EOF)
			elif i==2:
			    print timeStamp() + "I either got key or connection timeout"
			    pass

			# We expect any of these three patterns...
			i = child.expect (['Permission denied', 'Terminal type', '[#\$] '])
			if i==0:
			    print timeStamp() + 'Permission denied on host. Cant login'
			    child.kill(0)
			elif i==1:
			    print timeStamp() + 'Login OK... need to send terminal type.'
			    child.sendline('vt100')
			    child.expect ('[#\$] ')
			elif i==2:
				# Depending on state, send user info about host PC state and number of attempts
				# If the host is awake, then ssh is be normal
				# Else ssh connection is made when its not supposed to
				if state == "Awake":
				    print timeStamp() + '-- Login OK.'
				    print timeStamp() + 'Shell command prompt', child.after
				    child.close()
				    child.terminate()
				    break
				if state == "Sleep":
					print timeStamp() + (bcolors.WARNING + bcolors.BOLD + "[WARNING]" + bcolors.ENDC),  'Host PC is NOT SLEEPING\n\tSSH Attempted ' + str(j+1) + ' times'
					sleep(30)
				if state == "Hibernate":
					print timeStamp() + (bcolors.WARNING + bcolors.BOLD + "[WARNING]" + bcolors.ENDC),  'Host PC is NOT HIBERNATING\n\tSSH Attempted ' + str(j+1) + ' times'
					sleep(30)
		
		except pexpect.exceptions.TIMEOUT:
			if state == "Awake":
				print timeStamp() + (bcolors.WARNING + bcolors.BOLD + "[WARNING]" + bcolors.ENDC),  'Host PC is SLEEPING or HIBERNATING\n\tSSH Attempted ' + str(j+1) + ' times'
				sleep(30)
				continue
			elif state == "Sleep":
				print timeStamp() + 'Host PC is SLEEPING'
				break
			elif state == "Hibernate":
				print timeStamp() + 'Host PC is HIBERNATING'
				break

		except pexpect.exceptions.EOF:
			if state == "Awake":
				print timeStamp() + (bcolors.WARNING + bcolors.BOLD + "[WARNING]" + bcolors.ENDC), 'Host PC is SLEEPING or HIBERNATING\n\tSSH Attempted ' + str(j+1) + ' times'
				sleep(30)
				continue
			elif state == "Sleep":
				print timeStamp() + 'Host PC is SLEEPING'
				break
			elif state == "Hibernate":
				print timeStamp() + 'Host PC is HIBERNATING'
				break

		except:
			print '-'*60 + '\n'
			e = sys.exc_info()[0]
			print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in sendCommand: ",  "%s" % e
			print "Exception in user code:"
			print traceback.format_exc()
			print '-'*60 + '\n'
	
	if j == 2:
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), 'Host PC is not in correct state'
		global Errorlogs
		Errorlogs += '\nHost PC is not in correct state. Please check host PC and restart the automation'
		sys.exit()

def sleepHibernate(hostUserID, hostIPAddress, hostPassword, SorH):
	try: 
		print timeStamp() + "SSHing into Host PC"
		ssh_newkey = 'Are you sure you want to continue connecting'
		child = pexpect.spawn('ssh ' + hostUserID + '@'+ hostIPAddress)

		i=child.expect([ssh_newkey,'password:',pexpect.EOF])
		if i==0:
		    print timeStamp() + "Continue connecting to host PC"
		    child.sendline('yes')
		    i=child.expect([ssh_newkey,'password:',pexpect.EOF])
		if i==1:
		    print timeStamp() + "Sending password\n",
		    child.sendline(hostPassword)
		    #child.expect(pexpect.EOF)
		elif i==2:
		    print timeStamp() + "I either got key or connection timeout"
		    pass

		# We expect any of these three patterns...
		i = child.expect (['Permission denied', 'Terminal type', '[#\$] '])
		if i==0:
		    print timeStamp() + 'Permission denied on host. Cant login'
		    child.kill(0)
		elif i==1:
		    print timeStamp() + 'Login OK... need to send terminal type.'
		    child.sendline('vt100')
		    child.expect ('[#\$] ')
		elif i==2:
		    print '-- Login OK.'
		    print timeStamp() + 'Shell command prompt', child.after

		if SorH == 0:
			print timeStamp() + "Putting Host PC to SLEEP"
			child.sendline('cd /; ./cygdrive/c/pwrtest.exe /sleep /p:60 & exit')
			sleep(1)
		else:
			print timeStamp() + "Putting Host PC to HIBERNATE"
			child.sendline('cd /; ./cygdrive/c/pwrtest.exe /sleep /s:hibernate /p:90 & exit')
			sleep(1)

		child.close()
		child.terminate()
	
	except:
		print '-'*60 + '\n'
		e = sys.exc_info()[0]
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in sendCommand: ",  "%s" % e
		print "Exception in user code:"
		print traceback.format_exc()
		print '-'*60 + '\n'

def wakeComputer(macAddress):
	# Waking Host PC from sleep
	print timeStamp() + "Waking Host PC from SLEEP"
	WakeOnLan.wake_on_lan(macAddress)
	sleep(30)

def createResultsFile(OS, device, deviceConfig):
	# Creates a results file for a differnt OS
	resultsFile = open(initialPath + 'RESULTS_' + OS, 'w+')
	resultsFile.write('************************************************************\n')
	resultsFile.write('Date: ' + hostPCDate + '\n')
	resultsFile.write('Time: ' + hostPCOldTime + '\n')
	resultsFile.write('Operating System: ' + OS + '\n')
	resultsFile.write('Device: ' + device + ' ' + deviceConfig +'\n')
	resultsFile.write('======================================\n')
	resultsFile.write('State\t\tCurrent\t\tResult\n')
	resultsFile.write('======================================\n')

def captureCurrent():
	try:
		#print "in Capture Current"
		proc=subprocess.Popen('python ' + initialPath + 'capture_usb480_power.py 512', shell=True, stdout=subprocess.PIPE, )
		output=proc.communicate()[0]
		if output == "Unable to open Beagle device on port 0\nError code = -8\n":
			print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "Beagle device is not connected. Please make sure Beagle device is connected and restart the automation.\n"
			global Errorlogs
			Errorlogs += '\nBeagle device is not connected. Please make sure Beagle device is connected and restart the automation.'
			sys.exit()
			# msgbox("Beagle device is not connected.\nPlease make sure Beagle device is connected and restart the automation.\n",\
			#  title="Current Test Automation")
		else:
			# output.split('\n') makes a list and removes the '\n'
			# [1:512] gets rid of empty first and last elements in the string
			# The rest converts the list of strings to a list of float
			floatArray = [float(x) for x in output.split('\n')[1:512]]
			average = sum(floatArray)/len(floatArray)
			maxC = max(floatArray)
			minC = min(floatArray)
			print timeStamp() + "Measured Current = %.3f" %(average)
			return float("%.3f" %(average)), float(maxC), float(minC)
	except SystemExit:
		sys.exit()
		pass
	except:
		print '-'*60 + '\n'
		e = sys.exc_info()[0]
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in sendCommand: ",  "%s" % e
		print "Exception in user code:"
		print traceback.format_exc()
		print '-'*60 + '\n'

def extractCurrent(state, operatingSystem, dev, dock, charpo, devConfig, entries):
	device, docked, chargePort, deviceConfig = dev, dock, charpo, devConfig

	sleep(2)
	
	# Setting correct current boundaries for each device
	if operatingSystem == 0:
		OS = "Windows XP"
	elif operatingSystem == 1:
		OS = "Windows Vista"
	elif operatingSystem == 2:
		OS = "Windows 7"
	elif operatingSystem == 3:
		OS = "Windows 8"
	elif operatingSystem == 4:
		OS = "Windows 10"

	if dev == "iPhone":
		initExpRsltUB = 500.000
		initExpRsltLB = 450.000
	elif dev == "iPod":
		initExpRsltUB = 500.000
		initExpRsltLB = 450.000
	elif dev == "iPad":
		initExpRsltUB = 1000.000
		initExpRsltLB = 450.000
	elif dev == "iPadMini":
		initExpRsltUB = 1000.000
		initExpRsltLB = 450.000
	elif dev == "iPadPro":
		initExpRsltUB = 1000.000
		initExpRsltLB = 450.000
	elif dev == "Watch" and docked == 1:
		initExpRsltUB = 500.000
		initExpRsltLB = 100.000
	elif dev == "Watch" and docked == 0:
		initExpRsltUB = 15.000
		initExpRsltLB = 5.000

	if state == "Awake":
		if chargePort == 1:
			iUpperBound = 1500.000
		else:
			iUpperBound = 500.00
		iLowerBound = initExpRsltLB
	elif state == "Sleep":
		if chargePort == 1:
			iUpperBound = 2100.000
		else:
			iUpperBound = 2.5
		iLowerBound = 0
	elif state == "Hibernate":
		if chargePort == 1:
			iUpperBound = 2100.000
		else:
			iUpperBound = 2.5
		iLowerBound = 0
	
	print timeStamp() + "Extracting current"
	avgC, maxC, minC = captureCurrent()
	if tmp == False:
	 	sys.exit()
	avgCurrentValue = str(avgC)
	maxCurrentValue = str(maxC)
	minCurrentValue = str(minC)
	print timeStamp() + "Extraction complete"

	# Evaluating Average current
	if (avgC < iUpperBound and avgC > iLowerBound):
		for i in range(len(entires)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state:
				entries[i]['Current'] = avgCurrentValue
				entries[i]['CurrentResult'] = 'PASS'
		print timeStamp() + "Entries matrix updated - Average Current for ", OS, " in ", state, " state: PASS (", avgCurrentValue, ")"
	else:
		for i in range(len(entires)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state:
				entries[i]['Current'] = avgCurrentValue
				entries[i]['CurrentResult'] = 'FAIL'
		print timeStamp() + "Entries matrix updated - Average Current for ", OS, " in ", state, " state: FAIL (", avgCurrentValue, ")"

	# Evaluating Max Current
	if (maxC < iUpperBound):
		for i in range(len(entires)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state:
				entries[i]['MaxCurrent'] = maxCurrentValue
				entries[i]['MaxCurrentResult'] = 'PASS'
		print timeStamp() + "Entries matrix updated - Max Current for ", OS, " in ", state, " state: PASS (", maxCurrentValue, ")"
	else:
		for i in range(len(entires)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state:
				entries[i]['MaxCurrent'] = maxCurrentValue
				entries[i]['MaxCurrentResult'] = 'FAIL'
		print timeStamp() + "Entries matrix updated - Max Current for ", OS, " in ", state, " state: FAIL (", maxCurrentValue, ")"

	# Evaluating Min Current
	if (minC > 100.000):
		for i in range(len(entires)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state:
				entries[i]['MinCurrent'] = minCurrentValue
				entries[i]['MinCurrentResult'] = 'PASS'
		print timeStamp() + "Entries matrix updated - Min Current for ", OS, " in ", state, " state: PASS (", minCurrentValue, ")"
	else:
		for i in range(len(entires)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state:
				entries[i]['MinCurrent'] = minCurrentValue
				entries[i]['MinCurrentResult'] = 'FAIL'
		print timeStamp() + "Entries matrix updated - Min Current for ", OS, " in ", state, " state: FAIL (", minCurrentValue, ")"

def changeOS(hostIPAddress, hostUserID, hostPassword, OSID):
	try:
		print timeStamp() + "SSHing into Host PC"
		ssh_newkey = 'Are you sure you want to continue connecting'
		child = pexpect.spawn('ssh ' + hostUserID + '@'+ hostIPAddress)

		i=child.expect([ssh_newkey,'password:',pexpect.EOF])
		if i==0:
		    print timeStamp() + "Continue connecting to host PC"
		    child.sendline('yes')
		    i=child.expect([ssh_newkey,'password:',pexpect.EOF])
		if i==1:
		    print timeStamp() + "Sending password\n",
		    child.sendline(hostPassword)
		    #child.expect(pexpect.EOF)
		elif i==2:
		    print timeStamp() + "I either got key or connection timeout"
		    pass

		# We expect any of these three patterns...
		i = child.expect (['Permission denied', 'Terminal type', '[#\$] '])
		if i==0:
		    print timeStamp() + 'Permission denied on host. Cant login'
		    child.kill(0)
		elif i==1:
		    print timeStamp() + 'Login OK... need to send terminal type.'
		    child.sendline('vt100')
		    child.expect ('[#\$] ')
		elif i==2:
		    print timeStamp() + 'Login OK.'
		    print timeStamp() + 'Shell command prompt', child.after

		print timeStamp() + "Sending next OS command"
		sleep(2)
		child.sendline('cd /; ./cygdrive/c/users/desktop/')
		sleep(2)
		child.sendline('bcdedit /timeout 5')
		sleep(2)
		child.sendline('bcdedit /default {' + OSID + '}')
		sleep(2)
		child.sendline('Shutdown.exe -r -t 05; exit')
		sleep(2)
		child.close()
		child.terminate()
		sleep(120)

	except SystemExit:
		print "EXITING"

def deleteFiles(autoPath):
	# Delete Results file, so the new results does not get appeneded
	import os

	for operatingSystem in range (0, 5):
		if operatingSystem == 0:
			OS = "WinXP"
		elif operatingSystem == 1:
			OS = "WinVista"
		elif operatingSystem == 2:
			OS = "Win7"
		elif operatingSystem == 3:
			OS = "Win8"
		elif operatingSystem == 4:
			OS = "Win10"

		try:
		 	with open(autoPath + 'RESULTS_'+ OS, 'r'):
				fp = autoPath + 'RESULTS_'+ OS
  				os.remove(fp)
		except IOError:
			pass

def removeKnownHosts(sshPath):
	try:
		proc=subprocess.Popen('rm ' + sshPath + 'known_hosts', shell=True, stdout=subprocess.PIPE, )
		output=proc.communicate()[0]
		if output == 'rm: ' + sshPath + 'known_hosts: No such file or directory\n':
			print "test"
			pass
	except:
		print '-'*60 + '\n'
		e = sys.exc_info()[0]
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in sendCommand: ",  "%s" % e
		print "Exception in user code:"
		print traceback.format_exc()
		print '-'*60 + '\n'

def email(email_addresss, autoPath, Errorlogs):
	# Send an email of the results
	SENDMAIL = "/usr/sbin/sendmail" # sendmail location

	p = os.popen("%s -t" % SENDMAIL, "w")
  	p.write("To: " + email_addresss + "\n")
  	p.write("Subject: CURRENT AUTOMATION RESULTS\n")
  	p.write("\n") # blank line separating headers from body
	
	if 'Host PC is not in correct state.' in Errorlogs:
		p.write("\n\nError log:\n" + Errorlogs)
	elif 'Beagle device is not connected. Please make sure Beagle device is connected and restart the automation.' in Errorlogs:
		p.write("\n\nError log:\n" + Errorlogs)
	else:
		for operatingSystem in range (0, 5):
			if operatingSystem == 0:
				OS = "WinXP"
			elif operatingSystem == 1:
				OS = "WinVista"
			elif operatingSystem == 2:
				OS = "Win7"
			elif operatingSystem == 3:
				OS = "Win8"
			elif operatingSystem == 4:
				OS = "Win10"

			try:
			 	#with open(autoPath + 'RESULTS_'+ OS, 'r'):
				fp = open(autoPath + 'RESULTS_'+ OS, 'r')
				print autoPath + 'RESULTS_'+ OS
	  			
				while 1:
					line  = fp.read()
					print timeStamp() + "Emailing..."
					print line
					print timeStamp() + "Reading line for email"
					if not line:
						print timeStamp() + "no lines"
						break 
					p.write(line + '\n')
				if Errorlogs != "":
					p.write("\nError log:\n" + "-"*13 + "\n")
					p.write(Errorlogs)	
				fp.close()
			except IOError:
				print "Issue reading files for ", OS
				pass
			except:
				print '-'*60 + '\n'
				e = sys.exc_info()[0]
				print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in sendCommand: ",  "%s" % e
				print "Exception in user code:"
				print traceback.format_exc()
				print '-'*60 + '\n'



  	sts = p.close()
  	if sts != 0:
  		pass
		#print "Sendmail exit status ", sts

def send_mail(email_address, entries, accessories, dock, charpo, devOS, devConfig, Errorlogs, server="relay.apple.com"):

	proc=subprocess.Popen('scutil --get LocalHostName', shell=True, stdout=subprocess.PIPE, )
	localHostName=proc.communicate()[0]

	proc=subprocess.Popen('id -un', shell=True, stdout=subprocess.PIPE, )
	localUserName=proc.communicate()[0]

	fromAddress = str(localUserName.strip('\n') + "@" + localHostName.strip('\n') + ".local")

	# results = []
	# for i in range(len(entries)):
	# 	entries[i]['iteration'] = entries[i]['iteration'] / 2
	# 	results.append(entries[i]['result'])

	date = strftime("%m/%d/%Y", gmtime())
	device = devConfig
	acc = accessories
	build = devOS
	
	if charpo:
		port = 'Charging'
	else:
		port = 'Non-Charging'

	results = ['PASS']*9

	resultsclr = []
	for i in results:
		if i == 'PASS':
			resultsclr.append('green')
		elif i == 'FAIL':
			resultsclr.append('red')
		elif i == 'ISSUE':
			resultsclr.append('orange')

	if 'FAIL' in results:
		overallResult = 'FAIL'
		overallResultclr = 'red'
	elif 'ISSUE' in results:
		overallResult = 'PASS WITH ISSUES'
		overallResultclr = 'orange'
	else:
		overallResult = 'PASS'
		overallResultclr = 'green'



	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "CURRENT RESPONSE AUTOMATION RESULTS" + " -- " + overallResult
	# msg['From'] = me
	# msg['To'] = you
	
	# Create the body of the message (a plain-text and an HTML version).
	html = """\
	<html>
		<head></head>
			<body>
			<p>
			<b>Date: </b>{date}<br>
			<b>Device: </b>{device}<br>
			<b>Accessories: </b>{acc}<br>
			<b>Build: </b>{build}<br>
			<b>Host: </b>Lenovo L540 | Intel Core i5 CPU 2.60GHz | 4GB RAM | Charging Port Max current: Active - 1.5A, Sleep/Hibernation - 2.1A<br>
			<b>Port Type: </b>{port}<br>
			<b>Protocol Analyzer: </b>Beagle USB 480 Power Protocal Analyzer, Ultimate Edition<br><br>
			<b>Overall Result: <font color={overallResultclr}>{overallResult}</font></b><br>
			<table border="1" width="800"><tr><th><b>Result</th><th><b>OS</th><th><b>State</th><th><b>Avg Current (mA)</th><th><b>Max Current (mA)</th><th><b>Min Current (mA)</th><th><b>Comments</th></tr>
	""".format(**locals())

	for i in range(len(entries)):
		html += """\
		<tr><td align="center"><b><font color={0}>{1}</font></b></td><td>{2}</td><td>{3}</td><td align="right">{4}</td><td align="right">{5}</td><td align="right">{6}</td><td>{7}</td></tr>
		""".format(resultsclr[i],results[i], entries[i]['OS'], entries[i]['HostState'], entries[i]['Current'], entries[i]['MaxCurrent'], entries[i]['MinCurrent'], entries[i]['Comments'], **locals())
	
	if Errorlogs != "":
		html += """\
		</table><br>
		<i>Error Log:</i><br><br>
		{Errorlogs}
		""".format(**locals())

	html += """\

			</p>
		</body>
	</html>
	""".format(**locals())

    # Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
	msg.attach(part1)
   
    # part = MIMEBase('application', "octet-stream")
    # part.set_payload( open(file_path,"rb").read() )
    # Encoders.encode_base64(part)
    # part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file_path))
    # msg.attach(part)

    # Send the message via local SMTP server.
	s = smtplib.SMTP('relay.apple.com')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
	s.sendmail(fromAddress, email_address, msg.as_string())
	s.quit()


################################################################################################################################

if __name__ == '__main__':
	#sys.stdout = Logger()
	print (bcolors.HEADER + bcolors.BOLD + "\n******************** [TEST STARTING] ********************\n" + bcolors.ENDC)

	#deleteFiles(initialPath)
	removeKnownHosts(sshPath)
	#email_address = 'carlos_moreno@apple.com'
	#email('carlos_moreno@apple.com', '/users/carlos/Desktop/python/')

	sleep(1)
	selectedOS = [0]*5
	Data = userInterface()
	print timeStamp() + "User has entered information"
	# WinXPData = Data[0] 
	# WinVistaData = Data[1]
	Win7Data = Data[1]
	Win8Data = Data[2]
	Win10Data = Data[3]

	entries = []

	OperatingSystems = ['Windows 7', 'Windows 8.1', 'Windows 10']
	for i in range(len(OperatingSystems)):
		entries.append({'OS': OperatingSystems[i], 
						'HostState': 'Awake',
						'Current': 0, 
						'CurrentResult': '',
						'MaxCurrent': 0,
						'MaxCurrentResult': '',
						'MinCurrent': 0,
						'MinCurrentResult': '',
						'Comments': ''})
		entries.append({'OS': OperatingSystems[i], 
						'HostState': 'Sleep',
						'Current': 0, 
						'CurrentResult': '',
						'MaxCurrent': 0,
						'MaxCurrentResult': '',
						'MinCurrent': 0,
						'MinCurrentResult': '',
						'Comments': ''})
		entries.append({'OS': OperatingSystems[i], 
						'HostState': 'Hibernate',
						'Current': 0, 
						'CurrentResult': '',
						'MaxCurrent': 0,
						'MaxCurrentResult': '',
						'MinCurrent': 0,
						'MinCurrentResult': '',
						'Comments': ''})

	#print Data
	try:
		for i in range(len(selectedOS)):
			try:
				if Data[i][0] != 0:
					email_address = Data[i][11]
					selectedOS[i]= 1
			except:
				print '-'*60 + '\n'
				e = sys.exc_info()[0]
	 			print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in sendCommand: ",  "%s" % e
	 			print "Exception in user code:"
				print traceback.format_exc()
				print '-'*60 + '\n'
				pass
		

		for j in range(len(selectedOS)):
			if selectedOS[j] == 1:
				print timeStamp() + 'Resetting to first OS'
				changeOS(Data[j][1], Data[j][2], Data[j][3], Data[j][5])
				break

		for j in range(len(selectedOS)):
			try:
				if selectedOS[j] == 1:
					MainTest(j, Data[j][1], Data[j][2], Data[j][3], Data[j][4], Data[j][5], Data[j][6], Data[j][7], Data[j][8], Data[j][9], Data[j][10], Data[j][11], Data[j][12], entries)
					sleep(5)
					if j == 4:
						pass
					else:
						changeOS(Data[j][1], Data[j][2], Data[j][3], Data[j+1][5])
				else:
					OSName = ['Windows 7', 'Windows 8.1', 'Windows 10']
					print timeStamp() + "Operating System " + OSName[j] + " not selected."
					pass
			except SystemExit:
				sys.exit()
			except:
				print '-'*60 + '\n'
				e = sys.exc_info()[0]
	 			print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in sendCommand: ",  "%s" % e
	 			print "Exception in user code:"
				print traceback.format_exc()
				print '-'*60 + '\n'

		# for j in range(len(selectedOS)):
		# 	if selectedOS[j] == 1:
		# 		print timeStamp() + 'Resetting to first OS'
		# 		changeOS(Data[j][1], Data[j][2], Data[j][3], Data[j][5])
		# 		break
	
	except SystemExit:
		print timeStamp() + "Exiting application..."
		pass

	except:
		print '-'*60 + '\n'
		e = sys.exc_info()[0]
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in sendCommand: ",  "%s" % e
		print "Exception in user code:"
		print traceback.format_exc()
		print '-'*60 + '\n'

	#email(email_address, initialPath, Errorlogs)
	send_mail(email_address, entries, Errorlogs, server="relay.apple.com")

	#sshToHostAgain(hostUserID, hostIPAddress, hostPassword)
	print (bcolors.HEADER + bcolors.BOLD + "******************** [TEST COMPLETED] ********************" + bcolors.ENDC)

################################################################################################################################