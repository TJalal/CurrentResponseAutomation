#!/usr/bin/python
# -*- coding: utf-8 -*-
#import objc
import sys
import traceback
import WakeOnLan
from time import gmtime, strftime, sleep
from datetime import datetime, timedelta
from beagle_py import *

import Tkinter
from Tkinter import *
import tkSimpleDialog
import fileinput

import pexpect 
from pexpect import popen_spawn
import subprocess
from subprocess import check_output

from tempfile import mkstemp
from shutil import move
from os import remove, close
from os import listdir
from os.path import isfile, join
import glob
#import easygui
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders

global Errorlogs
Errorlogs = ''

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
		self.Win7 = IntVar()
		self.Win8 = IntVar()
		self.Win10 = IntVar()

		self.orb3 = Checkbutton(master, text="Win7", onvalue=1, offvalue=0, variable=self.Win7)
		self.orb4 = Checkbutton(master, text="Win8", onvalue=1, offvalue=0, variable=self.Win8)
		self.orb5 = Checkbutton(master, text="Win10", onvalue=1, offvalue=0, variable=self.Win10)

		self.orb3.grid(row=7, columnspan=1,column=1, sticky=W)
		self.orb4.grid(row=7, columnspan=1,column=2, sticky=W)
		self.orb5.grid(row=7, columnspan=1,column=3, sticky=W)

		# Setting Win7, Win8 and Win10 as defaults
		self.orb3.select()
		self.orb4.select()
		self.orb5.select()

		# Labels on the UI
		Label(master, text="Device Info:").grid(row=0, sticky=W)
		Label(master, text="Accessory Comb:").grid(row=4, sticky=W)
		Label(master, text="Build:").grid(row=5, sticky=W)
		Label(master, text="Email Address:").grid(row=6, sticky=W)
		Label(master, text="Operating Systems:").grid(row=7, sticky=W)
		
		# Open the defaults file where the inforamtion is stored
		defaults = open(initialPath + 'defaults.txt', 'r+')
		lines = defaults.readlines()
		
		# Variables for each field on the UI
		
		# Automation path, Device Info, Accessory Combination, Build, Email Address
		dev, acc, build, ipAdd, macAdd, emailAdd = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()

		# Windows variables: Host Username, Host Password, OS Identifier
		w7_user, w7_pass, w7_osid = StringVar(), StringVar(), StringVar()
		w8_user, w8_pass, w8_osid = StringVar(), StringVar(), StringVar()
		w10_user, w10_pass, w10_osid = StringVar(), StringVar(), StringVar()
		
		# Collecting default information 
		self.eDev = Entry(master, textvariable=dev)
		dev.set(lines[0].rstrip())
		self.eAcc = Entry(master, textvariable=acc)
		acc.set(lines[1].rstrip())
		self.eBuild = Entry(master, textvariable=build)
		build.set(lines[2].rstrip())
		self.eIPAdd = Entry(master, textvariable=ipAdd)
		ipAdd.set(lines[3].rstrip())
		self.eMACAdd = Entry(master, textvariable=macAdd)
		macAdd.set(lines[4].rstrip())
		self.eEmail = Entry(master, textvariable=emailAdd)
		emailAdd.set(lines[5].rstrip())

		# Collecting default information on Win7, Win8 and Win10
		self.eW7User = Entry(master, textvariable=w7_user)
		w7_user.set(lines[8].rstrip())
		self.eW7Pass = Entry(master, textvariable=w7_pass)
		w7_pass.set(lines[9].rstrip())
		self.eW7OSID = Entry(master, textvariable=w7_osid)
		w7_osid.set(lines[10].rstrip())

		self.eW8User = Entry(master, textvariable=w8_user)
		w8_user.set(lines[13].rstrip())
		self.eW8Pass = Entry(master, textvariable=w8_pass)
		w8_pass.set(lines[14].rstrip())
		self.eW8OSID = Entry(master, textvariable=w8_osid)
		w8_osid.set(lines[15].rstrip())

		self.eW10User = Entry(master, textvariable=w10_user)
		w10_user.set(lines[18].rstrip())
		self.eW10Pass = Entry(master, textvariable=w10_pass)
		w10_pass.set(lines[19].rstrip())
		self.eW10OSID = Entry(master, textvariable=w10_osid)
		w10_osid.set(lines[20].rstrip())

		# Placing fields on UI
		self.eDev.grid(row=0, column=1, columnspan=2, sticky=W)
		self.eDev.focus_set()
		self.eAcc.grid(row=4, column=1, columnspan=2, sticky=W)
		self.eBuild.grid(row=5, column=1, columnspan=2, sticky=W)
		self.eEmail.grid(row=6, column=1, columnspan=2, sticky=W)	

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
		self.orb6 = Checkbutton(master, text="Docked", onvalue=1, offvalue=0, variable=self.docked, state=DISABLED)
		self.orb6.grid(row=1, columnspan=1,column=3, sticky=W)
		
		# Is it a Charging Port?
		self.chargingPort = IntVar()
		self.orb7 = Checkbutton(master, text="Charging Port", onvalue=1, offvalue=0, variable=self.chargingPort)
		self.orb7.grid(row=2, columnspan=1,column=3, sticky=W)

		# Is Apple Mobile Device Service enabled?
		self.amds = IntVar()
		self.orb8 = Checkbutton(master, text="AMDS", onvalue=1, offvalue=0, variable=self.amds)
		self.orb8.grid(row=3, columnspan=1,column=3, sticky=W)

		defaults.close()	
	
	def enableDocked(self):
		# When Apple Watch is selected, allow the use of the Docked option
		self.orb6.config(state=NORMAL)

	def disableDocked(self):
		# When Apple Watch is not selected, disable the use of the Docked option
		self.orb6.config(state=DISABLED)

	def buttonbox(self):
		# Setting buttons
		box = Frame(self)
		w = Button(box, text="Cancel", width=7, command=self.cancel)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Setup", width=7, command=self.setup)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="Save", width=7, command=self.setDefault)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="RUN", width=7, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()
	
	def setup(self):
		#import subprocess
		subprocess.call(['open', '-a', 'TextEdit', initialPath + 'defaults.txt'])
	
	def setDefault(self):
		# Setting defaults if an OS is selected
		# Only the selected OS will save the new default info
		defaults = open(initialPath + 'defaults.txt', 'r')
		with defaults as file:
			lines = file.readlines()				
				
		lines[0] = self.eDev.get()+ '\n'
		lines[1] = self.eAcc.get()+ '\n'
		lines[2] = self.eBuild.get()+ '\n'
		lines[5] = self.eEmail.get()+ '\n'
				
		with open(initialPath + 'defaults.txt', 'w') as file:
			file.writelines(lines)
		defaults.close()
		
	def apply(self):
		# Information that is collected are placed in tuples with their corressponding OS
		selectDevice = self.selectDevice.get()
		deviceConfig = self.eDev.get()
		accessories = self.eAcc.get()
		build = self.eBuild.get()
		ipAddress = self.eIPAdd.get()
		macAddress = self.eMACAdd.get()
		emailAddress = self.eEmail.get()
		docked = self.docked.get()
		chargingPort = self.chargingPort.get()
		amds = self.amds.get()
		
		if self.Win7.get():
			selectOS = 1
			hostUserID, hostPassword, OSID = self.eW7User.get(), self.eW7Pass.get(), self.eW7OSID.get()
			Win7Data = [selectOS, hostUserID, hostPassword, OSID]
		else:
			selectOS = 0
			Win7Data = [selectOS]
		
		if self.Win8.get():
			selectOS = 1
			hostUserID, hostPassword, OSID = self.eW8User.get(), self.eW8Pass.get(), self.eW8OSID.get()
			Win8Data = [selectOS, hostUserID, hostPassword, OSID]
		else:
			selectOS = 0
			Win8Data = [selectOS]

		if self.Win10.get():
			selectOS = 1
			hostUserID, hostPassword, OSID = self.eW10User.get(), self.eW10Pass.get(), self.eW10OSID.get()
			Win10Data = [selectOS, hostUserID, hostPassword, OSID]
		else:
			selectOS = 0
			Win10Data = [selectOS]
		
		self.result = [Win7Data, Win8Data, Win10Data], selectDevice, deviceConfig, accessories, build, ipAddress, macAddress, emailAddress, docked, chargingPort, amds

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

def timeStamp():
	hostPCDate = strftime("%m/%d/%Y", gmtime())
	hostPCTime = '{:%H:%M:%S}'.format(datetime.now())
	timeStamp = (bcolors.OKBLUE + "[" + str(hostPCDate) + " " + str(hostPCTime) + "] " + bcolors.ENDC)
	return timeStamp

def userInterface():
	# User Interface used to collect necessary information
	root = Tkinter.Tk()
	root.title("Current Response Automation")
	root.resizable(width=FALSE, height=FALSE)
	root.withdraw()
	dialog = MyDialog(root)
	return dialog.result

def MainTest(OS, hostIPAddress, hostUserID, hostPassword, OSID, macAddress, selectDevice, docked, chargingPort, amds, entries):
	try:
		if OS == 0:
			OSName = 'Windows 7'
		elif OS == 1:
			OSName = 'Windows 8.1'
		elif OS == 2:
			OSName = 'Windows 10'


		print timeStamp() + "Starting current extraction and analysis for ", OSName
		#removeKnownHosts(sshPath)
		sleep(1)
		stateCheck(hostUserID, hostIPAddress, hostPassword, "Awake")
		extractCurrent("Awake", OS, selectDevice, docked, chargingPort, amds, entries)
		sleepHibernate(hostUserID, hostIPAddress,hostPassword,0) #sleep
		sleep(30)
		#stateCheck(hostUserID, hostIPAddress, hostPassword, "Sleep")
		extractCurrent("Sleep", OS, selectDevice, docked, chargingPort, amds, entries)
		sleep(10)
		wakeComputer(macAddress)
		sleep(30)
		sleepHibernate(hostUserID, hostIPAddress,hostPassword,1) #hibernate
		sleep(30)
		#stateCheck(hostUserID, hostIPAddress, hostPassword, "Hibernate")
		extractCurrent("Hibernate", OS, selectDevice, docked, chargingPort, amds, entries)
		sleep(30)
		wakeComputer(macAddress)


	except SystemExit:
		sys.exit()
	except:
		print '-'*60 + '\n'
		e = sys.exc_info()[0]
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in MainTest(): ",  "%s" % e
		print "Exception in user code:"
		print traceback.format_exc()
		print '-'*60 + '\n'

def stateCheck(hostUserID, hostIPAddress, hostPassword, state):
	for j in range(3):
		try: 
			print timeStamp() + "Connecting to host PC via SSH"
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
			    print timeStamp() + "Retrieved key or connection timeout"
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
				    print timeStamp() + 'Login OK'
				    #print timeStamp() + 'Shell command prompt', child.after
				    child.close()
				    child.terminate()
				    break
				if state == "Sleep":
					print timeStamp() + (bcolors.WARNING + bcolors.BOLD + "[WARNING]" + bcolors.ENDC),  'Host PC is NOT SLEEPING -- SSH Attempted ' + str(j+1) + ' times'
					sleep(30)
				if state == "Hibernate":
					print timeStamp() + (bcolors.WARNING + bcolors.BOLD + "[WARNING]" + bcolors.ENDC),  'Host PC is NOT HIBERNATING -- SSH Attempted ' + str(j+1) + ' times'
					sleep(30)
		
		except pexpect.exceptions.TIMEOUT:
			if state == "Awake":
				print timeStamp() + (bcolors.WARNING + bcolors.BOLD + "[WARNING]" + bcolors.ENDC),  'Host PC is SLEEPING or HIBERNATING -- SSH Attempted ' + str(j+1) + ' times'
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
				print timeStamp() + (bcolors.WARNING + bcolors.BOLD + "[WARNING]" + bcolors.ENDC), 'Host PC is SLEEPING or HIBERNATING -- SSH Attempted ' + str(j+1) + ' times'
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
			print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in stateCheck(): ",  "%s" % e
			print "Exception in user code:"
			print traceback.format_exc()
			print '-'*60 + '\n'
	
	if j == 2:
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), 'Host PC is not in correct state'
		global Errorlogs
		Errorlogs += '\nHost PC is not in correct state. Please check host PC and restart the automation.'
		sys.exit()

def sleepHibernate(hostUserID, hostIPAddress, hostPassword, SorH):
	try: 
		print timeStamp() + "Connecting to host PC via SSH"
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
		    print timeStamp() + "Retrieved key or connection timeout"
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
		    print timeStamp() + 'Login OK'
		    #print timeStamp() + 'Shell command prompt', child.after

		if SorH == 0:
			print timeStamp() + "Setting Host PC to SLEEP"
			child.sendline('cd /; ./cygdrive/c/pwrtest.exe /sleep /p:90 & exit')
			sleep(1)
		else:
			print timeStamp() + "Setting Host PC to HIBERNATE"
			child.sendline('cd /; ./cygdrive/c/pwrtest.exe /sleep /s:hibernate /p:90 & exit')
			sleep(1)

		child.close()
		child.terminate()
	
	except:
		print '-'*60 + '\n'
		e = sys.exc_info()[0]
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in sleepHibernate(): ",  "%s" % e
		print "Exception in user code:"
		print traceback.format_exc()
		print '-'*60 + '\n'

def wakeComputer(macAddress):
	# Waking Host PC from sleep
	print timeStamp() + "Waking Host PC from SLEEP"
	WakeOnLan.wake_on_lan(macAddress)
	sleep(30)

def captureCurrent():
	try:
		#print "in Capture Current"
		proc=subprocess.Popen('python ' + initialPath + 'capture_usb480_power.py 512', shell=True, stdout=subprocess.PIPE, )
		output=proc.communicate()[0]
		if output == "Unable to open Beagle device on port 0\nError code = -8\n":
			print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "Beagle device is not connected. Please make sure Beagle device is connected and restart the automation.\n"
			global Errorlogs
			Errorlogs += '\nBeagle Analyzer is not connected. Please ensure Beagle Analyzer is connected and restart the automation.'
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
			return float("%.1f" %(average)), float(maxC), float(minC)
	except SystemExit:
		sys.exit()
		pass
	except:
		print '-'*60 + '\n'
		e = sys.exc_info()[0]
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in captureCurrent(): ",  "%s" % e
		print "Exception in user code:"
		print traceback.format_exc()
		print '-'*60 + '\n'

def extractCurrent(state, operatingSystem, dev, dock, charpo, amds, entries):
	device, docked, chargePort, AMDS = dev, dock, charpo, amds
	sleep(2)
	
	# Setting correct current boundaries for each device
	if operatingSystem == 0:
		OS = "Windows 7"
	elif operatingSystem == 1:
		OS = "Windows 8.1"
	elif operatingSystem == 2:
		OS = "Windows 10"

	if dev == "iPhone":
		initExpRsltUB = 500.000
		initExpRsltLB = 100.000
	elif dev == "iPod":
		initExpRsltUB = 500.000
		initExpRsltLB = 100.000
	elif dev == "iPad":
		initExpRsltUB = 1000.000
		initExpRsltLB = 100.000
	elif dev == "iPadMini":
		initExpRsltUB = 1000.000
		initExpRsltLB = 100.000
	elif dev == "iPadPro":
		initExpRsltUB = 1000.000
		initExpRsltLB = 100.000
	elif dev == "Watch": 
		if docked:
			initExpRsltUB = 500.000
			initExpRsltLB = 100.000
		else:
			initExpRsltUB = 15.000
			initExpRsltLB = 5.000

	# if state == "Awake":
	# 	if chargePort:
	# 		iUpperBound = 1500.000
	# 	else:
	# 		iUpperBound = 500.00
	# 	iLowerBound = initExpRsltLB
	# elif state == "Sleep":
	# 	if chargePort:
	# 		iUpperBound = 2100.000
	# 	else:
	# 		iUpperBound = 2.5
	# 	iLowerBound = 0
	# elif state == "Hibernate":
	# 	if chargePort:
	# 		iUpperBound = 2100.000
	# 	else:
	# 		iUpperBound = 2.5
	# 	iLowerBound = 0

	# if amds:
	# 	iUpperBound = 500.00
	# 	iLowerBound = initExpRsltLB

	if chargePort:
		if state == "Awake":
			iUpperBound = 1500.00
			iLowerBound = initExpRsltLB
		else:
			iUpperBound = 2100.00
			iLowerBound = 100.00
	else:
		if state == "Awake":
			iUpperBound = 500.00
			iLowerBound = initExpRsltLB
		elif amds and dev != "Watch": #to fix Watch + amds issue
			iUpperBound = 500.00
			iLowerBound = initExpRsltLB
		else:
			iUpperBound = 2.5
			iLowerBound = 0
	
	print timeStamp() + "Extracting current..."
	avgC, maxC, minC = captureCurrent()
	if not avgC:
	 	sys.exit()
	avgCurrentValue = str(avgC)
	maxCurrentValue = str(maxC)
	minCurrentValue = str(minC)
	print timeStamp() + "Extraction complete"

	# Evaluating Min Current
	if (minC > 2.5 and minC < 100.00):
		for i in range(len(entries)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state and entries[i]['AMDS'] == amds:
				entries[i]['MinCurrent'] = minCurrentValue
				entries[i]['MinCurrentResult'] = 'ISSUE'
				entries[i]['Comments'] = 'Possible Un-configured state'
		print timeStamp() + "Entries matrix updated - Min Current for", OS, "in", state, "state: " + (bcolors.WARNING + bcolors.BOLD + "ISSUE" + bcolors.ENDC) + " (" + minCurrentValue + "mA)"
	elif (minC > iLowerBound):
		for i in range(len(entries)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state and entries[i]['AMDS'] == amds:
				entries[i]['MinCurrent'] = minCurrentValue
				entries[i]['MinCurrentResult'] = 'PASS'
		print timeStamp() + "Entries matrix updated - Min Current for", OS, "in", state, "state: " + (bcolors.OKGREEN + bcolors.BOLD + "PASS" + bcolors.ENDC) + " (" + minCurrentValue + "mA)"
	else:
		if amds == 0 and (state == 'Sleep' or state == 'Hibernate'):
			for i in range(len(entries)):
				if entries[i]['OS'] == OS and entries[i]['HostState'] == state and entries[i]['AMDS'] == amds:
					entries[i]['MinCurrent'] = minCurrentValue
					entries[i]['MinCurrentResult'] = 'PASS'
			print timeStamp() + "Entries matrix updated - Min Current for", OS, "in", state, "state: " + (bcolors.OKGREEN + bcolors.BOLD + "PASS" + bcolors.ENDC) + " (" + minCurrentValue + "mA)"
		else:
			for i in range(len(entries)):
				if entries[i]['OS'] == OS and entries[i]['HostState'] == state and entries[i]['AMDS'] == amds:
					entries[i]['MinCurrent'] = minCurrentValue
					entries[i]['MinCurrentResult'] = 'FAIL'
					entries[i]['Comments'] = 'Min Current below limit'
			print timeStamp() + "Entries matrix updated - Min Current for", OS, "in", state, "state: " + (bcolors.FAIL + bcolors.BOLD + "FAIL" + bcolors.ENDC) + " (" + minCurrentValue + "mA)"

	# Evaluating Max Current
	if (maxC > 2.5 and maxC < 100.00):
		for i in range(len(entries)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state and entries[i]['AMDS'] == amds:
				entries[i]['MaxCurrent'] = maxCurrentValue
				entries[i]['MaxCurrentResult'] = 'ISSUE'
				entries[i]['Comments'] = 'Possible Un-configured state'
		print timeStamp() + "Entries matrix updated - Max Current for", OS, "in", state, "state: " + (bcolors.WARNING + bcolors.BOLD + "ISSUE" + bcolors.ENDC) + " (" + maxCurrentValue + "mA)"
	elif (maxC < iUpperBound and maxC > iLowerBound):
		for i in range(len(entries)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state and entries[i]['AMDS'] == amds:
				entries[i]['MaxCurrent'] = maxCurrentValue
				entries[i]['MaxCurrentResult'] = 'PASS'
		print timeStamp() + "Entries matrix updated - Max Current for", OS, "in", state, "state: " + (bcolors.OKGREEN + bcolors.BOLD + "PASS" + bcolors.ENDC) + " (" + maxCurrentValue + "mA)"
	else:
		for i in range(len(entries)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state and entries[i]['AMDS'] == amds:
				entries[i]['MaxCurrent'] = maxCurrentValue
				entries[i]['MaxCurrentResult'] = 'FAIL'
				entries[i]['Comments'] = 'Max Current exceeded limit'
		print timeStamp() + "Entries matrix updated - Max Current for", OS, "in", state, "state: " + (bcolors.FAIL + bcolors.BOLD + "FAIL" + bcolors.ENDC) + " (" + maxCurrentValue + "mA)"

	# Evaluating Average current
	if (avgC > 2.5 and avgC < 100.00):
		for i in range(len(entries)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state and entries[i]['AMDS'] == amds:
				entries[i]['Current'] = avgCurrentValue
				entries[i]['CurrentResult'] = 'ISSUE'
				entries[i]['Comments'] = 'Possible Un-configured state'
		print timeStamp() + "Entries matrix updated - Avg Current for", OS, "in", state, "state: " + (bcolors.WARNING + bcolors.BOLD + "ISSUE" + bcolors.ENDC) + " (" + avgCurrentValue + "mA)"
	elif (avgC < iUpperBound and avgC > iLowerBound):
		for i in range(len(entries)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state and entries[i]['AMDS'] == amds:
				entries[i]['Current'] = avgCurrentValue
				entries[i]['CurrentResult'] = 'PASS'
		print timeStamp() + "Entries matrix updated - Avg Current for", OS, "in", state, "state: " + (bcolors.OKGREEN + bcolors.BOLD + "PASS" + bcolors.ENDC) + " (" + avgCurrentValue + "mA)"
	else:
		for i in range(len(entries)):
			if entries[i]['OS'] == OS and entries[i]['HostState'] == state and entries[i]['AMDS'] == amds:
				entries[i]['Current'] = avgCurrentValue
				entries[i]['CurrentResult'] = 'FAIL'
		print timeStamp() + "Entries matrix updated - Avg Current for", OS, "in", state, "state: " + (bcolors.FAIL + bcolors.BOLD + "FAIL" + bcolors.ENDC) + " (" + avgCurrentValue + "mA)"

def amdsToggle(hostIPAddress, hostUserID, hostPassword, amds):
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

		if amds:
			print timeStamp() + "Turning on Apple Mobile Device Service"
			child.sendline("sc config \"Apple Mobile Device Service\" start= auto")
			sleep(10)
			child.sendline("sc start \"Apple Mobile Device Service\"")
			sleep(1)
		else:
			print timeStamp() + "Turning off Apple Mobile Device Service"
			child.sendline("sc config \"Apple Mobile Device Service\" start= disabled")
			sleep(10)
			child.sendline("sc stop \"Apple Mobile Device Service\"")
			sleep(1)

		child.close()
		child.terminate()
	except pexpect.exceptions.EOF:
		print timestamp() + "EOF found in amdsToggle()"
		sleep(5)
		amdsToggle(hostIPAddress, hostUserID, hostPassword, amds)
	except:
		print '-'*60 + '\n'
		e = sys.exc_info()[0]
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in amdsToggle(): ",  "%s" % e
		print "Exception in user code:"
		print traceback.format_exc()
		print '-'*60 + '\n'

def changeOS(hostIPAddress, hostUserID, hostPassword, OSID):
	try:
		print timeStamp() + "Connecting to Host PC via SSH"
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
		    print timeStamp() + "Retrieved key or connection timeout"
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
		    print timeStamp() + 'Login OK'
		    #print timeStamp() + 'Shell command prompt', child.after

		print timeStamp() + "Sending command to boot to next operating system"
		sleep(2)
		# child.sendline('cd /; ./cygdrive/c/users/desktop/')
		# sleep(2)
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

def removeKnownHosts(sshPath):
	try:
		with open(sshPath + '/known_hosts', 'r'):
			proc=subprocess.Popen('rm ' + sshPath + 'known_hosts', shell=True, stdout=subprocess.PIPE,)
			output=proc.communicate()[0]
			print timeStamp() + "Removing known_hosts from SSH path"
	except IOError:			
		pass

		# proc=subprocess.Popen('rm ' + sshPath + 'known_hosts', shell=True, stdout=subprocess.PIPE,)
		# output=proc.communicate()[0]
		# print timeStamp() + "Removing known_hosts from SSH path"
		#output = check_output(['rm ' + sshPath + 'known_hosts'])
	except OSError:
		pass
	except:
		print '-'*60 + '\n'
		e = sys.exc_info()[0]
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in removeKnownHosts(): ",  "%s" % e
		print "Exception in user code:"
		print traceback.format_exc()
		print '-'*60 + '\n'

def send_mail(email_address, entries, accessories, charpo, amds, devOS, devConfig, Errorlogs, server="relay.apple.com"):
	print timeStamp() + "Sending email to " + email_address

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

	results = []
	for i in range(len(entries)):
		results.append(entries[i]['CurrentResult'])
		if entries[i]['AMDS']:
			entries[i]['AMDS'] = 'On'
		else:
			entries[i]['AMDS'] = 'Off'

	resultsclr = []
	for i in results:
		if i == 'PASS':
			resultsclr.append('green')
		elif i == 'FAIL':
			resultsclr.append('red')
		elif i == 'ISSUE':
			resultsclr.append('orange')
		else:
			resultsclr.append('black')

	maxCResultCLR = []
	minCResultCLR = []

	for i in range(len(entries)):
		if entries[i]['MaxCurrentResult'] == 'PASS':
			maxCResultCLR.append('green')
		elif entries[i]['MaxCurrentResult'] == 'FAIL':
			maxCResultCLR.append('red')
		elif entries[i]['MaxCurrentResult'] == 'ISSUE':
			maxCResultCLR.append('orange')
		else:
			maxCResultCLR.append('black')

		if entries[i]['MinCurrentResult'] == 'PASS':
			minCResultCLR.append('green')
		elif entries[i]['MinCurrentResult'] == 'FAIL':
			minCResultCLR.append('red')
		elif entries[i]['MinCurrentResult'] == 'ISSUE':
			minCResultCLR.append('orange')
		else:
			minCResultCLR.append('black')



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
			<b>Host: </b>Lenovo L540 | Intel Core i5 CPU 2.60GHz | 4GB RAM | 
				Charging Port Max current: Active - 1.5A, Sleep/Hibernation - 2.1A<br>
			<b>Port Type: </b>{port}<br>
			<b>Protocol Analyzer: </b>Beagle USB 480 Power Protocal Analyzer, Ultimate Edition<br><br>
			<b>Overall Result: <font color={overallResultclr}>{overallResult}</font></b><br>
			<table border="1" width="1000"><tr><th><b>Result</th><th><b>OS</th><th><b>State</th><th><b>AMDS</th>
				<th><b>Avg Current (mA)</th><th><b>Max Current (mA)</th><th><b>Min Current (mA)</th><th><b>Comments</th></tr>
	""".format(**locals())

	for i in range(len(entries)):
		html += """\
		<tr><td align="center"><b><font color={0}>{1}</font></b></td><td>{2}</td><td>{3}</td><td>{4}</td>
		<td align="right"><font color={0}>{5}</font></td><td align="right"><font color={6}>{7}</font></td>
		<td align="right"><font color={8}>{9}</font></td><td>{10}</td></tr>
		""".format(resultsclr[i],
					results[i], 
					entries[i]['OS'], 
					entries[i]['HostState'], 
					entries[i]['AMDS'], 
					entries[i]['Current'], 
					maxCResultCLR[i],
					entries[i]['MaxCurrent'],
					minCResultCLR[i], 
					entries[i]['MinCurrent'], 
					entries[i]['Comments'], 
					**locals())


	if Errorlogs != "":
		html += """\
		</table><br>
		<i><u><font color=red>Error Log:</u></i></font><br>
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
	print timeStamp() +  "Email sent"

################################################################################################################################

if __name__ == '__main__':
	#sys.stdout = Logger()
	print (bcolors.HEADER + bcolors.BOLD + "\n******************************************** [TEST STARTING] ********************************************\n" + bcolors.ENDC)

	try:
		removeKnownHosts(sshPath)
	except:
		pass

	sleep(1)

	selectedOS = [0]*3
	Data = userInterface()
	print timeStamp() + "User has entered required information, starting test"

	Win7Data = Data[0][0]
	Win8Data = Data[0][1]
	Win10Data = Data[0][2]
	selectDevice = Data[1]
	deviceConfig = Data[2]
	accessories = Data[3]
	build = Data[4]
	ipAddress = Data[5]
	macAddress = Data[6]
	emailAddress = Data[7]
	docked = Data[8]
	chargingPort = Data[9]
	amds = Data[10]
	#amds = chargingPort

	entries = []
	OSName = ['Windows 7', 'Windows 8.1', 'Windows 10']
	OperatingSystems = []

	for i in range(len(selectedOS)):
		if Data[0][i][0] != 0:
			selectedOS[i] = 1

	if selectedOS[0]:
		OperatingSystems.append('Windows 7')
	if selectedOS[1]:
		OperatingSystems.append('Windows 8.1')
	if selectedOS[2]:
		OperatingSystems.append('Windows 10')

	if chargingPort:
		amds = 0

	# Create Entires array
	for i in range(len(OperatingSystems)):
		entries.append({'OS': OperatingSystems[i], 
						'HostState': 'Awake',
						'AMDS': 0,
						'Current': 0, 
						'CurrentResult': '',
						'MaxCurrent': 0,
						'MaxCurrentResult': '',
						'MinCurrent': 0,
						'MinCurrentResult': '',
						'Comments': ''})
		entries.append({'OS': OperatingSystems[i], 
						'HostState': 'Sleep',
						'AMDS': 0,
						'Current': 0, 
						'CurrentResult': '',
						'MaxCurrent': 0,
						'MaxCurrentResult': '',
						'MinCurrent': 0,
						'MinCurrentResult': '',
						'Comments': ''})
		entries.append({'OS': OperatingSystems[i], 
						'HostState': 'Hibernate',
						'AMDS': 0,
						'Current': 0, 
						'CurrentResult': '',
						'MaxCurrent': 0,
						'MaxCurrentResult': '',
						'MinCurrent': 0,
						'MinCurrentResult': '',
						'Comments': ''})
		if amds:
			entries.append({'OS': OperatingSystems[i], 
							'HostState': 'Awake',
							'AMDS': 1,
							'Current': 0, 
							'CurrentResult': '',
							'MaxCurrent': 0,
							'MaxCurrentResult': '',
							'MinCurrent': 0,
							'MinCurrentResult': '',
							'Comments': ''})
			entries.append({'OS': OperatingSystems[i], 
							'HostState': 'Sleep',
							'AMDS': 1,
							'Current': 0, 
							'CurrentResult': '',
							'MaxCurrent': 0,
							'MaxCurrentResult': '',
							'MinCurrent': 0,
							'MinCurrentResult': '',
							'Comments': ''})
			entries.append({'OS': OperatingSystems[i], 
							'HostState': 'Hibernate',
							'AMDS': 1,
							'Current': 0, 
							'CurrentResult': '',
							'MaxCurrent': 0,
							'MaxCurrentResult': '',
							'MinCurrent': 0,
							'MinCurrentResult': '',
							'Comments': ''})

	try:
		for i in range(len(selectedOS)):
			if selectedOS[i]:
				print timeStamp() + 'Resetting to first operating system - ', OperatingSystems[0]
				changeOS(ipAddress, Data[0][i][1], Data[0][i][2], Data[0][i][3])
				break

		for i in range(len(selectedOS)):
			try:
				if selectedOS[i]:
					if chargingPort:
						removeKnownHosts(sshPath)
						MainTest(i, ipAddress, Data[0][i][1], Data[0][i][2], Data[0][i][3], macAddress, selectDevice, docked, chargingPort, amds, entries)
						sleep(5)
					else:
						amds1 = 0
						removeKnownHosts(sshPath)
						amdsToggle(ipAddress, Data[0][i][1], Data[0][i][2], amds1)
						MainTest(i, ipAddress, Data[0][i][1], Data[0][i][2], Data[0][i][3], macAddress, selectDevice, docked, chargingPort, amds1, entries)
						sleep(10)
						if amds:
							amds1 = 1
							removeKnownHosts(sshPath)
							amdsToggle(ipAddress, Data[0][i][1], Data[0][i][2], amds1)
							MainTest(i, ipAddress, Data[0][i][1], Data[0][i][2], Data[0][i][3], macAddress, selectDevice, docked, chargingPort, amds1, entries)
							sleep(5)
					if i == 2:
						pass
					else:
						changeOS(ipAddress, Data[0][i][1], Data[0][i][2], Data[0][i+1][3])
				else:
					print timeStamp() + OSName[i] + " was not selected. Skipping test for " + OSName[i]
					pass
			except IndexError:
				print "index error"
				pass
			except SystemExit:
				sys.exit()
			except:
				print '-'*60 + '\n'
				e = sys.exc_info()[0]
	 			print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in __main__: ",  "%s" % e
	 			print "Exception in user code:"
				print traceback.format_exc()
				print '-'*60 + '\n'
	
	except SystemExit:
		print timeStamp() + "Exiting application..."
		pass

	except:
		print '-'*60 + '\n'
		e = sys.exc_info()[0]
		print timeStamp() + (bcolors.FAIL + bcolors.BOLD + "[ERROR]" + bcolors.ENDC), "in __main__: ",  "%s" % e
		print "Exception in user code:"
		print traceback.format_exc()
		print '-'*60 + '\n'

	send_mail(emailAddress, entries, accessories, chargingPort, amds, build, deviceConfig, Errorlogs, server="relay.apple.com")

	print (bcolors.HEADER + bcolors.BOLD + "******************************************** [TEST COMPLETED] ********************************************" + bcolors.ENDC)

################################################################################################################################