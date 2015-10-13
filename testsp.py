import subprocess
import sys
import traceback
#import sh
import time
import easygui
from easygui import *
#!/usr/bin/python

import pty, sys
from subprocess import Popen, PIPE, STDOUT
from time import sleep
from os import fork, waitpid, execv, read, write



# https://bitbucket.org/OPiMedia/simpleguics2pygame
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

#import simpleguitk as simplegui

chargingPort = 0

def captureCurrent():
	try:
		proc=subprocess.Popen('python ./capture_usb480_power.py 512', shell=True, stdout=subprocess.PIPE, )
		output=proc.communicate()[0]
		if output == "Unable to open Beagle device on port 0\nError code = -8\n":
			print "\nBeagle device is not connected.\nPlease make sure Beagle device is connected and restart the automation.\n"
			msgbox("Beagle device is not connected.\nPlease make sure Beagle device is connected and restart the automation.\n",\
			 title="Current Test Automation")
		else:
			# output.split('\n') makes a list and removes the '\n'
			# [1:512] gets rid of empty first and last elements in the string
			# The rest converts the list of strings to a list of float
			floatArray = [float(x) for x in output.split('\n')[1:512]]
			average = sum(floatArray)/len(floatArray)
			print "%.3f" %(average)
			return average
	except:
		pass

def test1():
	proc=subprocess.Popen('whoami', shell=True, stdout=subprocess.PIPE, )
	output=proc.communicate()[0]
	print output
	if output == "tasfinjalal\n":
		print "Success"
	else:
		print "Failure"

def sshToHost3(hostUserID, hostIPAddress, hostPassword):
	# SSH into the Host	
	print "SSHing into Host PC"
	proc=subprocess.Popen("ssh -t -t " + hostUserID + "@" + hostIPAddress, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,)
	proc.stdin.write(hostPassword)
	proc.stdin.flush()
	output=proc.communicate()
	print output

def sshToHost2():
	HOST="17.208.130.222"
	# Ports are handled in ~/.ssh/config since we use OpenSSH
	COMMAND="uname -a"
	user = "dti@17.208.130.222"
	ssh = subprocess.Popen(["ssh ", user, COMMAND],
	                       shell=True,
	                       stdout=subprocess.PIPE,
	                       stderr=subprocess.PIPE)
	ssh.stdin.writeline("desktopqa")
	result = ssh.stdout.readlines()

	if result == []:
	    error = ssh.stderr.readlines()
	    print >>sys.stderr, "ERROR: %s" % error
	else:
	    print result

def test():
	raftlibs.sui.launchApplicationByName("Terminal")
	keyboard.typeString_("ssh " + hostUserID + "@" + hostIPAddress)
	keyboard.typeVirtualKey_(kVK_Return)
	target.delayForTimeInterval_(2)
	if hostPassword != "NULL":
		keyboard.typeString_(hostPassword)
	keyboard.typeVirtualKey_(kVK_Return)
	sshd = 1

def uitesting():
	msg = "Enter device details and email"
	title = "Current Test Automation"
	fieldNames = ["Device","Accessories","Build","Email"]
	fieldValues = []  # we start with blanks for the values
	fieldValues = multenterbox(msg,title, fieldNames)

	# make sure that none of the fields was left blank
	while 1:
	    if fieldValues == None: break
	    errmsg = ""
	    for i in range(len(fieldNames)):
	      if fieldValues[i].strip() == "":
	        errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
	    if errmsg == "": break # no problems found
	    fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
	print "Reply was:", fieldValues
	operatingSystems = multchoicebox("Choose which operating system(s) to test:", "Operating Systems", 
		["Windows XP", "Windows Vista", "Windows 7", "Windows 8", "Windows 10"])

	devices = choicebox("Choose which devices(s) to test:", "Devices", ["iPod", "iPhone", "iPad", "Apple Watch"])

	if ynbox("Charging Port?", "", ["Yes", "No"]):
		chargingPort = 1
	else:
		chargingPort = 0
	




	return operatingSystems, devices, chargingPort
	#sys.exit(0)           # user chose Cancel

def uitesting2():

		msg = "Enter your personal information"
		title = "Credit Card Application"
		fieldNames = ["Name","Street Address","City","State","ZipCode"]
		fieldValues = []  # we start with blanks for the values
		fieldValues = multenterbox(msg,title, fieldNames)

		# make sure that none of the fields was left blank
		while 1:
			if fieldValues == None: break
			errmsg = ""
			for i in range(len(fieldNames)):
				if fieldValues[i].strip() == "":
					errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
			if errmsg == "": break # no problems found
			fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

		print "Reply was:", fieldValues

def uitesting3():
		msg = "Enter logon information"
		title = "Demo of multpasswordbox"
		fieldNames = ["Server ID", "User ID", "Password"]
		fieldValues = []  # we start with blanks for the values
		fieldValues = multpasswordbox(msg,title, fieldNames)

		# make sure that none of the fields was left blank
		while 1:
			if fieldValues == None: break
			errmsg = ""
			for i in range(len(fieldNames)):
				if fieldValues[i].strip() == "":
					errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
			if errmsg == "": break # no problems found
			fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)

		print "Reply was:", fieldValues

def uitesting4():
	message = "Welcome!"

	# Handler for mouse click
	def click():
	    global message
	    message = "Good job!"

	# Handler to draw on canvas
	def draw(canvas):
	    canvas.draw_text(message, [50,112], 48, "Red")

	# Create a frame and assign callbacks to event handlers
	frame = simplegui.create_frame("Home", 300, 200)
	frame.add_button("Click me", click)
	frame.set_draw_handler(draw)

	# Start the frame animation
	frame.start()

def test3():
	import subprocess
	import sys

	HOST="dti@17.208.130.222"
	# Ports are handled in ~/.ssh/config since we use OpenSSH
	COMMAND="desktopqa"

	ssh = subprocess.Popen(["ssh", "%s" % HOST, ],
	                       shell=False,
	                       stdout=subprocess.PIPE,
	                       stderr=subprocess.PIPE)
	result = ssh.stdout.readlines()
	if result == []:
	    error = ssh.stderr.readlines()
	    print >>sys.stderr, "ERROR: %s" % error
	else:
	    print result

def test4():
	test = ssh()

def sshToHost(hostUserID, hostIPAddress, hostPassword):
	username = hostUserID + '@' + hostIPAddress
	password = hostPassword + '\r'
	try:
		print 'SSHing into target PC'
		proc=subprocess.Popen(['ssh -t -t ' + username], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, )
		#output=proc.communicate()[0]
		proc.communicate(password)[0]
		print output
		
		#if output == username + "'s password: ":
		#	proc.stdin.write(password)

	except:
		print 
		proc.communicate(password)[0]
		#pass


#captureCurrent()
sshToHost("DTMLLUAdminUser", "17.208.130.107", "desktopqa")

#!/usr/bin/env python      1
import Tkinter as tk       

class Application(tk.Frame):              
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)   
        self.grid()                       
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit',
            command=self.quit)            
        self.quitButton.grid()            

#app = Application()                       
#app.master.title('Sample application')    
#app.mainloop()

