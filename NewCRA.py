###########################################################
from __future__ import print_function
try:
    import __builtin__
except ImportError:
    # Python 3
    import builtins as __builtin__

def print(*args, **kwargs):
    """My custom print() function."""
    # Adding new arguments to the print function signature 
    # is probably a bad idea.
    # Instead consider testing if custom argument keywords
    # are present in kwargs
    #__builtin__.print('My overridden print() function!')
    return __builtin__.print(timeStamp(), *args, **kwargs)
###########################################################


# Add text notification - Kaushal
# add queue info

import sys
import traceback
import copy
from time import gmtime, strftime, sleep
from datetime import datetime, timedelta
import pexpect 
from pexpect import popen_spawn





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

class CurrentMeasurement:
	minimum = 0.0
	average = 0.0
	maximum = 0.0
	minResult = ''
	avgResult = ''
	maxResult = ''

class OSInfoClass:
	hostOS = "OPERATING SYSTEM"
	hostIPAddress = "IPADDRESS"
	hostUserID = "USER ID"
	hostPassword = "PASSWORD"
	osid = "OPERATING SYSTEM ID"

class DeviceInfo(OSInfoClass):
	hostUserID = "root"
	hostPassword = "alpine"
	battery = 0


# Setting Color, bold and underline to print statements
def setFancyFonts(string, color, bold=0, underline=0):

	colorDict ={'HEADER': bcolors.HEADER,
				'blue': bcolors.OKBLUE,
				'green': bcolors.OKGREEN,
				'yellow': bcolors.WARNING,
				'red': bcolors.FAIL}

	if bold:
		bold = bcolors.BOLD
	else:
		bold = ''

	if underline:
		underline = bcolors.UNDERLINE
	else:
		underline = ''

	return colorDict[color] + bold + underline + string + bcolors.ENDC

def timeStamp():
	hostPCDate = strftime("%m/%d/%Y", gmtime())
	hostPCTime = '{:%H:%M:%S}'.format(datetime.now())
	timeStamp = setFancyFonts("[" + str(hostPCDate) + " " + str(hostPCTime) + "] ", "blue")
	return timeStamp

def batteryRange(stateOfCharge):
	batteryRanges = [(0,4), (5,9), (10,14), (15,49), (50,79), (80,96), (97,99), (100,101)]
	for idx, batteryRange in enumerate(batteryRanges):
		if (stateOfCharge >= batteryRange[0]) and (stateOfCharge < batteryRange[1]):
			return CHARGE_LOOKUP_TABLE['Expected Current Value'][idx]

def batteryRangeIndex(stateOfCharge):
	batteryRanges = [(0,4), (5,9), (10,14), (15,49), (50,79), (80,96), (97,99), (100,101)]
	for idx, batteryRange in enumerate(batteryRanges):
		if (stateOfCharge >= batteryRange[0]) and (stateOfCharge < batteryRange[1]):
			return idx

def currentStringResults(current, currentRange):
	if current.average > currentRange[0] and current.average < currentRange[1]:
		current.avgResult = "PASS"
	else:
		current.avgResult = "FAIL"

	if current.minimum > currentRange[0] and current.minimum < currentRange[1]:
		current.minResult = "PASS"
	else:
		current.minResult = "FAIL"

	if current.maximum < currentRange[1]:
		current.maxResult = "PASS"
	else:
		current.maxResult = "FAIL"

def captureCurrent():
	try:
		#print "in Capture Current"
		proc=subprocess.Popen('python ' + initialPath + 'capture_usb480_power.py 512', shell=True, stdout=subprocess.PIPE, )
		output=proc.communicate()[0]
		if output == "Unable to open Beagle device on port 0\nError code = -8\n":
			print (setFancyFonts("[ERROR]", "red"), "Beagle device is not connected. Please make sure Beagle device is connected and restart the automation.\n")
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
		print ('-'*60 + '\n')
		e = sys.exc_info()[0]
		print (setFancyFonts("[ERROR]", "red"), "in captureCurrent(): ",  "%s" % e)
		print ("Exception in user code:")
		print (traceback.format_exc())
		print ('-'*60 + '\n')

def SSH(loginInfo):
	hostIPAddress = loginInfo.hostIPAddress
	hostUserID = loginInfo.hostUserID
	hostPassword = loginInfo.hostPassword

	try: 
		print ("Connecting to host PC via SSH")
		ssh_newkey = 'Are you sure you want to continue connecting'
		child = pexpect.spawn('ssh ' + hostUserID + '@'+ hostIPAddress)

		i=child.expect([ssh_newkey,'password:',pexpect.EOF])
		if i==0:
		    #print timeStamp() + "Continue connecting to host PC"
		    child.sendline('yes')
		    i=child.expect([ssh_newkey,'password:',pexpect.EOF])
		if i==1:
		    #print timeStamp() + "Sending password\n",
		    child.sendline(hostPassword)
		    #child.expect(pexpect.EOF)
		elif i==2:
		    print (setFancyFonts("Retrieved key or connection timeout", "yellow"))
		    pass

		# We expect any of these three patterns...
		i = child.expect (['Permission denied', 'Terminal type', '[#\$] '])
		if i==0:
		    print (setFancyFonts("Permission denied on host. Cant login", "red"))
		    child.kill(0)
		elif i==1:
		    print ('Login OK... need to send terminal type.')
		    child.sendline('vt100')
		    child.expect ('[#\$] ')
		elif i==2:
		    print (setFancyFonts("[CONNECTED]", "green"))
		    #print timeStamp() + 'Shell command prompt', child.after

		return child
	
	except pexpect.exceptions.TIMEOUT:
		print (setFancyFonts("[SSH TIMEOUT]", "yellow"))

		# if state == "Awake":
		# 	print timeStamp() + (bcolors.WARNING + bcolors.BOLD + "[WARNING]" + bcolors.ENDC),  'Host PC is SLEEPING or HIBERNATING -- SSH Attempted '
		# 	sleep(30)
		# elif state == "Sleep":
		# 	print timeStamp() + 'Host PC is SLEEPING'
		# elif state == "Hibernate":
		# 	print timeStamp() + 'Host PC is HIBERNATING'

	except pexpect.exceptions.EOF:
		print (setFancyFonts("[SSH EOF]", "yellow"))
		
		# if state == "Awake":
		# 	print timeStamp() + (bcolors.WARNING + bcolors.BOLD + "[WARNING]" + bcolors.ENDC), 'Host PC is SLEEPING or HIBERNATING -- SSH Attempted ' 
		# 	sleep(30)
		# elif state == "Sleep":
		# 	print timeStamp() + 'Host PC is SLEEPING'
		# elif state == "Hibernate":
		# 	print timeStamp() + 'Host PC is HIBERNATING'

	except:
		print ('-'*60 + '\n')
		e = sys.exc_info()[0]
		print (setFancyFonts("[ERROR]", "FAIL", 1), "in SSH(): \n",  "%s" % e)
		print ("Exception in user code:")
		print (traceback.format_exc())
		print ('-'*60 + '\n')

def closeSSH(child):
	child.close()
	child.terminate()

def setCommand(command):

	child = SSH(OSInfo)

	command = command.upper()

	if command == 'SUSPEND':
		print ("Sending SUSPEND command")
		child.sendline('cd /; ./cygdrive/c/pwrtest.exe /sleep /p:90 & exit')
		sleep(1)
	elif command == 'RESUME':
		print ("Sending RESUME command")
		#child.sendline('cd /; ./cygdrive/c/pwrtest.exe /sleep /s:hibernate /p:90 & exit')
		sleep(1)
	elif command == 'RESET':
		print ("Sending RESET command")
		#child.sendline('cd /; ./cygdrive/c/pwrtest.exe /sleep /s:hibernate /p:90 & exit')
		sleep(1)
	elif command == 'UNCONFIGURED':
		print ("Sending UNCONFIGURED command")
		#child.sendline('cd /; ./cygdrive/c/pwrtest.exe /sleep /s:hibernate /p:90 & exit')
		sleep(1)
	elif command == 'CONFIGURED':
		print ("Sending CONFIGURED command")
		#child.sendline('cd /; ./cygdrive/c/pwrtest.exe /sleep /s:hibernate /p:90 & exit')
		sleep(1)
	elif command == 'SLEEP':
		print ("Sending SLEEP command")
		child.sendline('cd /; ./cygdrive/c/pwrtest.exe /sleep /p:90 & exit')
		sleep(1)
	elif command == 'HIBERNATE':
		print ("Sending HIBERNATE command")
		child.sendline('cd /; ./cygdrive/c/pwrtest.exe /sleep /s:hibernate /p:90 & exit')
		sleep(1)
	else:
		print ("Invalid command. Please issue a valid command.")

	closeSSH(child)

# Checks if the current OS is the correct OS
def checkOS():
	# SSH into the host
	child = SSH(OSInfo)

	# Send the BCDedit command to get the list of OSes on Windows boot manager
	child.sendline('bcdedit')
	sleep(1)
	child.expect('~') 

	# Set a varaible for the list
	bcdeditInfo = child.before

	# Check to see if the current OSID is in the list
	# If it is not, then it is the correct OS
	# When running 'bcdedit' command, 
	# the current OS will have the identifier: '{current}'
	if OSInfo.osid not in bcdeditInfo:
		print ("Correct OS verified")
		return True
	else:
		print (setFancyFonts("Not in correct OS", "yellow"))
		return False

	# Close the SSH connection
	closeSSH(child)
	#return child
	
def stateOfCharge():
	try:
		child = SSH(deviceLoginInfo)
		print ("Checking battery percentage")
		child.sendline("gestalt_query BatteryCurrentCapacity")
		sleep(1)
		child.expect('#')
		i = child.before
		
		batteryPercent = re.search(r'BatteryCurrentCapacity: (\d+)',i)
		#print timeStamp(), "Battery for ", entries[threadID]["IPAddress"], ": ", battery
		batteryPercent = batteryPercent.group(1)
		return batteryPercent
	except:
		print ("STILL UNDER CONSTRUCTION")
		return 10

def removeKnownHosts(sshPath):
	try:
		with open(sshPath + '/known_hosts', 'r'):
			proc=subprocess.Popen('rm ' + sshPath + 'known_hosts', shell=True, stdout=subprocess.PIPE,)
			output=proc.communicate()[0]
			print ("Removing known_hosts from SSH path")
	except IOError:			
		pass

		# proc=subprocess.Popen('rm ' + sshPath + 'known_hosts', shell=True, stdout=subprocess.PIPE,)
		# output=proc.communicate()[0]
		# print timeStamp() + "Removing known_hosts from SSH path"
		#output = check_output(['rm ' + sshPath + 'known_hosts'])
	except OSError:
		pass
	except:
		print ('-'*60 + '\n')
		e = sys.exc_info()[0]
		print (setFancyFonts("[ERROR]", "FAIL", 1), "in removeKnownHosts(): \n",  "%s" % e)
		print ("Exception in user code:")
		print (traceback.format_exc())
		print ('-'*60 + '\n')

def checkHostState(hostLoginInfo):
	for i in range(3):
		try:
			child = SSH(hostLoginInfo)
			if state == 'Awake':
				print ("Login OK")
				closeSSH(child)
				break
			elif (state == 'Sleep') or (state == 'Hibernate'):
				print (setFancyFonts("[WARNING]", 'yellow'), 
						"Host PC is", setFancyFonts("NOT", 'red', 1), "in correct state.")
				print ("\t\tExpected: AWAKE | Actual:", state.upper())
				sleep(30)

		except pexpect.exceptions.TIMEOUT:
			if state == 'Awake':
				print (setFancyFonts("[WARNING]", 'yellow'), 
						"Host PC is", setFancyFonts("NOT", 'red', 1), "in correct state.")
				print ("\t\tExpected: ", state.upper(), " | Actual: AWAKE")
				sleep(30)
			elif (state == 'Sleep') or (state == 'Hibernate'):
				print ("Host is in correct state.")
				break
		except pexpect.exceptions.EOF:
			if state == 'Awake':
				print (setFancyFonts("[WARNING]", 'yellow'), 
						"Host PC is", setFancyFonts("NOT", 'red', 1), "in correct state.")
				print ("\t\tExpected: ", state.upper(), " | Actual: AWAKE")
				sleep(30)
			elif (state == 'Sleep') or (state == 'Hibernate'):
				print ("Host is in correct state.")
				break
	
	# 	if i == 2:
	# 		print (setFancyFonts("[ERROR]", 'red'), 'Host PC is not in correct state')
	# 		global Errorlogs
	# 		Errorlogs += '\nHost PC is not in correct state. Please check host PC and restart the automation.'
	# 		sys.exit()

def wakeComputer(macAddress):
	# Waking Host PC from sleep
	print ("Waking Host PC from SLEEP")
	WakeOnLan.wake_on_lan(macAddress)
	sleep(30)

def captureCurrent():
	try:
		proc=subprocess.Popen('python ' + initialPath + 'capture_usb480_power.py 512', shell=True, stdout=subprocess.PIPE, )
		output=proc.communicate()[0]
		if output == "Unable to open Beagle device on port 0\nError code = -8\n":
			print (setFancyFonts("[ERROR]", 'red', 1), "Beagle device is not connected. Please make sure Beagle device is connected and restart the automation.\n")
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
		print ('-'*60 + '\n')
		e = sys.exc_info()[0]
		print (setFancyFonts("[ERROR]", 'red', 1), "in SSH(): \n",  "%s" % e)
		print ("Exception in user code:")
		print (traceback.format_exc())
		print ('-'*60 + '\n')

def amdsToggle(hostLoginInfo, amds):
	child =SSH(hostLoginInfo)

	if amds:
		print ("Turning on Apple Mobile Device Service")
		child.sendline("sc config \"Apple Mobile Device Service\" start= auto")
		sleep(10)
		child.sendline("sc start \"Apple Mobile Device Service\"")
		sleep(1)
	else:
		print ("Turning off Apple Mobile Device Service")
		child.sendline("sc config \"Apple Mobile Device Service\" start= disabled")
		sleep(10)
		child.sendline("sc stop \"Apple Mobile Device Service\"")
		sleep(1)

	closeSSH(child)

def changeOS(hostLoginInfo, OSID):
	child = SSH(hostLoginInfo)

	print ("Sending command to boot to next operating system")
	sleep(2)
	# child.sendline('cd /; ./cygdrive/c/users/desktop/')
	# sleep(2)
	child.sendline('bcdedit /timeout 5')
	sleep(2)
	child.sendline('bcdedit /default {' + OSID + '}')
	sleep(2)
	child.sendline('Shutdown.exe -r -t 05; exit')
	sleep(2)
	closeSSH(child)
	sleep(120)

def setCurrentLimits():
	lowerLimit = 100.0
	upperLimit = portLimits[portType]

	if device in watchFamily and not docked:
		lowerLimit = 10.0
		upperLimit = 15.0

	if chargingPort:
		upperLimit = chargingPortLimits[state]
	elif AMDSisOn:
		upperLimit = portLimits[portType]
	elif (state is "SLEEP") or (state is "HIBERNATE"):
		lowerLimit = 0.0
		upperLimit = 2.5

	print (lowerLimit, upperLimit)
	return (lowerLimit, upperLimit)

def extractCurrent():
	iLowerBound, iUpperBound = setCurrentLimits()
	
	print ("Extracting current...")
	avgC, maxC, minC = captureCurrent()
	if not avgC:
	 	sys.exit()
	avgCurrentValue = str(avgC)
	maxCurrentValue = str(maxC)
	minCurrentValue = str(minC)
	print ("Extraction complete")

	for os in OperatingSystems:
		for hostStates in OperatingSystems[OS]:
			for amds in OperatingSystems[OS][hostStates]:
				if (os == OS) and (hostStates == state) and (amds == AMDSisOn):

					OperatingSystems[os][hostStates][amds]["Current"].average = avgC 
					OperatingSystems[os][hostStates][amds]["Current"].minimum = minC
					OperatingSystems[os][hostStates][amds]["Current"].maximum = maxC

					if (avgC > 2.5 and avgC < 100.00):
						OperatingSystems[os][hostStates][amds]["Current"].avgResult = "ISSUE"
						OperatingSystems[os][hostStates][amds]["Comments"] = "Possible Un-configured state"
					elif (avgC > iLowerBound and avgC < iUpperBound):
						OperatingSystems[os][hostStates][amds]["Current"].avgResult = "PASS"
					else:
						OperatingSystems[os][hostStates][amds]["Current"].avgResult = "FAIL"

					if (minC > 2.5 and minC < 100.00):
						OperatingSystems[os][hostStates][amds]["Current"].minResult = "ISSUE"
					elif (minC > iLowerBound and minC < iUpperBound):
						OperatingSystems[os][hostStates][amds]["Current"].minResult = "PASS"
					else:
						OperatingSystems[os][hostStates][amds]["Current"].minResult = "FAIL"

					if (maxC > 2.5 and maxC < 100.00):
						OperatingSystems[os][hostStates][amds]["Current"].maxResult = "ISSUE"
					elif (maxC < iUpperBound and maxC > iLowerBound):
						OperatingSystems[os][hostStates][amds]["Current"].maxResult = "PASS"
					else:
						OperatingSystems[os][hostStates][amds]["Current"].maxResult = "FAIL"
				else:
					pass



iPhoneFamily = ['N41', 'N48', 'N51', 'N56', 'N61', 'N66', 'N69', 'N71']
iPadFamily = ['J1', 'J71', 'J81', 'J127']
iPadProFamily =['J99', 'J207']
iPadMiniFamily = ['J85m']
iPodFamily = ['N78', 'N102']
watchFamily = ['N27a', 'N28a', 'N27b', 'N28b', 'N27d', 'N28d', 'N74', 'N75']
hidFamily = []

iPhoneFamily_ExpectedCurrentValues = [(1480,1490), (1430,1440), (1380,1390), (1200,1390), (1200,1390), (1000,1100), (900,1000), (0,500)]

CHARGE_LOOKUP_TABLE = []
CHARGE_LOOKUP_TABLE.append({'Device': 'N71',
							'Device Family': iPhoneFamily,
							'Expected Current Value': iPhoneFamily_ExpectedCurrentValues,
							'docked': 0 })
CHARGE_LOOKUP_TABLE.append({'Device': 'N74',
							'Device Family': watchFamily,
							'Expected Current Value': iPhoneFamily_ExpectedCurrentValues,
							'docked': 0 })
CHARGE_LOOKUP_TABLE.append({'Device': 'J99',
							'Device Family': iPadProFamily,
							'Expected Current Value': iPhoneFamily_ExpectedCurrentValues,
							'docked': 0 })
CHARGE_LOOKUP_TABLE.append({'Device': 'N102',
							'Device Family': iPodFamily,
							'Expected Current Value': iPhoneFamily_ExpectedCurrentValues,
							'docked': 0 })
CHARGE_LOOKUP_TABLE.append({'Device': 'J71',
							'Device Family': iPadFamily,
							'Expected Current Value': iPhoneFamily_ExpectedCurrentValues,
							'docked': 0 })
CHARGE_LOOKUP_TABLE.append({'Device': 'J85m',
							'Device Family': iPadMiniFamily,
							'Expected Current Value': iPhoneFamily_ExpectedCurrentValues,
							'docked': 0 })


OS = "Win7"
device = 'N74'
docked = False
chargingPort = True
state = "AWAKE"
AMDSisOn = False

avgC = 487.00
minC = 400.00
maxC = 490.00

portType = "500 mA"
if ' ' in portType:
	portType = portType.replace(' ', '')


chargingPortLimits = {'AWAKE': 		1500.0,
					  'SLEEP': 		2100.0,
					  'HIBERNATE': 	2100.0}

portLimits = {'500mA': 		500.0,
			  '1000mA': 	1000.0,
			  '1500mA': 	1500.0,
			  '2100mA': 	2100.0,
			  '2500mA': 	2500.0,
			  '3000mA': 	3000.0}

unconfigured = {'Yes': True,
				'No': False}


# Cubic Dictionary instead of an array of dictionaries
currentEntries 		= {"Current": 	CurrentMeasurement()}

amdsState 			= {False: 		copy.deepcopy(currentEntries),
				   	   True: 		copy.deepcopy(currentEntries)}

hostStates 			= {"AWAKE": 	copy.deepcopy(amdsState),
			  		   "SLEEP": 	copy.deepcopy(amdsState),
			  		   "HIBERNATE": copy.deepcopy(amdsState)}

OperatingSystems 	= {"Win7": 		copy.deepcopy(hostStates),
	  				   "Win8.1": 	copy.deepcopy(hostStates),
	  				   "Win10": 	copy.deepcopy(hostStates)}


eHCI = {"Suspend Current": 		CurrentMeasurement(),
		"Resume Current": 		CurrentMeasurement(),
		"Reset Current": 		CurrentMeasurement(),
		"Configured Current": 	CurrentMeasurement(),
		"Unconfigured Current": CurrentMeasurement()}




extractCurrent()

for OS in OperatingSystems.keys():
	for hostStates in OperatingSystems[OS].keys():
		for amds in OperatingSystems[OS][hostStates].keys():
			print (OS, hostStates, amds)
			print (OperatingSystems[OS][hostStates][amds]["Current"].average)
			print (OperatingSystems[OS][hostStates][amds]["Current"].avgResult)
			print (OperatingSystems[OS][hostStates][amds]["Current"].minimum)
			print (OperatingSystems[OS][hostStates][amds]["Current"].minResult)
			print (OperatingSystems[OS][hostStates][amds]["Current"].maximum)
			print (OperatingSystems[OS][hostStates][amds]["Current"].maxResult)

print (OperatingSystems["Win7"]['AWAKE'][False]["Current"].maximum)

if device in iPhoneFamily:
	print ("Yay")


#deviceInfo = (item for item in CHARGE_LOOKUP_TABLE if item["Device"] == device).next()

# if deviceInfo["Device"] in iPhoneFamily:
# 	print ("Yay again!")
#print (deviceInfo)
#print(deviceInfo["Expected Current Value"][batteryRangeIndex(50)])

# deviceInfo2 = (item for item in CHARGE_LOOKUP_TABLE if device in item['Device Family']).next()
# print (deviceInfo2['Expected Current Value'][batteryRangeIndex(stateOfCharge())])


# for idx in range(len(CHARGE_LOOKUP_TABLE)):
# 	if CHARGE_LOOKUP_TABLE[idx]['Device'] == 'N61':
# 		print ("N61")


# Win7HostInfo 				= OSInfoClass()
# Win7HostInfo.hostOS			= "Windows 7"
# Win7HostInfo.hostIPAddress 	= '17.208.128.47'
# Win7HostInfo.hostPassword  	= 'Testpassword,1'
# Win7HostInfo.hostUserID    	= 'DTMLLUAdminUser'
# Win7HostInfo.osid          	= "455f93d1-3a59-11e6-aacb-f8728d038731" 

# Win8HostInfo 				= OSInfoClass()
# Win8HostInfo.hostOS			= "Windows 8"
# Win8HostInfo.hostIPAddress 	= '17.208.128.47'
# Win8HostInfo.hostPassword  	= 'Testpassword,1'
# Win8HostInfo.hostUserID    	= 'DTMLLUAdminUser'
# Win8HostInfo.osid          	= "b6beb1f9-3dae-11e6-b81d-f72f01deb373" 

# Win10HostInfo 				= OSInfoClass()
# Win10HostInfo.hostOS		= "Windows 10"
# Win10HostInfo.hostIPAddress = '17.208.128.47'
# Win10HostInfo.hostPassword  = 'Testpassword,1'
# Win10HostInfo.hostUserID    = 'DTMLLUAdminUser'
# Win10HostInfo.osid          = "79ee6af5-aa33-11e5-87bd-b9e74922afd6"

# Win10Host = ["Windows 10",'17.208.128.47', 'Testpassword,1', 'DTMLLUAdminUser', "79ee6af5-aa33-11e5-87bd-b9e74922afd6"]

# allOSInfo = [Win7HostInfo, Win8HostInfo, Win10HostInfo]






# entries = [[[0 for amds in xrange(2)] for hostState in xrange(3)] for OS in xrange(3)]

# print (entries)



class Entries():
	current = CurrentMeasurement()

class AmdsState():
	current = Entries()

class Current():
	def __init__(self):
		self.current = CurrentMeasurement()

	def current(self):
		return self.current

class AMDS():
	def __init__(self):
		self.amdsON = Current()
		self.amdsOFF = Current()
		self.toggle = ["AMDS ON", "AMDS OFF"]

	def amds(self):
		return self.amdsON, self.amdsOFF, self.toggle

class HostStates():
	def __init__(self):
		self.awake = AMDS()
		self.sleep = AMDS()
		self.hibernate = AMDS()

	def hostState(self):
		return self.awake, self.sleep, self.hibernate


# Win7 = HostStates()
# Win8 = HostStates()
# Win10 = HostStates()

# os = 3
# OS = []

# for i in range(os):
# 	OS.append(HostStates())

# print (OS[0])




# print (OS[0].awake)
# OS[0].awake.amdsON.current.average = 4.0
# OS[0].awake.amdsOFF.current.maximum = 7.0

# test = "Awake"

# awakeState = Win7.awake

# print (OS[0].awake.amdsON.current.average)
# print (OS[0].awake.amdsOFF.current.maximum)
# print (OS[0].awake)

# if awakeState == Win7.awake:
# 	print ("PASS")





# for OS in OperatingSystems:
# 	for hostStates in OperatingSystems[OS]:
# 		for amds in OperatingSystems[OS][hostStates]:

# 			if (OS == "Win8.1") and (hostStates == "Sleep") and (amds == "AMDS OFF"):
# 				OperatingSystems[OS][hostStates][amds]["Current"].average = 2.0
# 			print (OperatingSystems[OS][hostStates][amds]["Current"].average)





iLowerBound = 100
iUpperBound = 500
avgC = 487.00
minC = 400.00
maxC = 490.00

os = "Win7"
state = 'Awake'
amdsToggle = "AMDS OFF"


# for OS in OperatingSystems:
# 	for hostStates in OperatingSystems[OS]:
# 		for amds in OperatingSystems[OS][hostStates]:
# 			if (os == OS) and (state == hostStates) and (amds == amdsToggle):

# 				OperatingSystems[os][state][amdsToggle]["Current"].average = avgC 
# 				OperatingSystems[os][state][amdsToggle]["Current"].minimum = minC
# 				OperatingSystems[os][state][amdsToggle]["Current"].maximum = maxC

# 				if (avgC > 2.5 and avgC < 100.00):
# 					OperatingSystems[os][state][amdsToggle]["Current"].avgResult = "ISSUE"
# 					OperatingSystems[os][state][amdsToggle]["Comments"] = "Possible Un-configured state"
# 				elif (avgC > iLowerBound and avgC < iUpperBound):
# 					OperatingSystems[os][state][amdsToggle]["Current"].avgResult = "PASS"
# 				else:
# 					OperatingSystems[os][state][amdsToggle]["Current"].avgResult = "FAIL"

				
# 				if (minC > 2.5 and minC < 100.00):
# 					OperatingSystems[os][state][amdsToggle]["Current"].minResult = "ISSUE"
# 				elif (minC > iLowerBound and minC < iUpperBound):
# 					OperatingSystems[os][state][amdsToggle]["Current"].minResult = "PASS"
# 				else:
# 					OperatingSystems[os][state][amdsToggle]["Current"].minResult = "FAIL"

# 				if (maxC > 2.5 and maxC < 100.00):
# 					OperatingSystems[os][state][amdsToggle]["Current"].maxResult = "ISSUE"
# 				elif (maxC < iUpperBound and maxC > iLowerBound):
# 					OperatingSystems[os][state][amdsToggle]["Current"].maxResult = "PASS"
# 				else:
# 					OperatingSystems[os][state][amdsToggle]["Current"].maxResult = "FAIL"

# 			else:
# 				pass


# for OS in OperatingSystems.keys():
# 	for hostStates in OperatingSystems[OS].keys():
# 		for amds in OperatingSystems[OS][hostStates].keys():
# 			# print (OperatingSystems[OS][hostStates][amds]["Current"].average)
# 			# print (OperatingSystems[OS][hostStates][amds]["Current"].avgResult)
# 			# print (OperatingSystems[OS][hostStates][amds]["Current"].minimum)
# 			# print (OperatingSystems[OS][hostStates][amds]["Current"].minResult)
# 			# print (OperatingSystems[OS][hostStates][amds]["Current"].maximum)
# 			# print (OperatingSystems[OS][hostStates][amds]["Current"].maxResult)
# 			print (OS, hostStates, amds)


#print (OperatingSystems["Win7"]["Awake"]["AMDS OFF"]["Current"].average)
# if "Win7" in OS.keys():
# 	print (OS.keys())

# print (entries4)
# print (entries4["Win7"]["Awake"]["AMDS OFF"]["Current"].maximum)
# print ()

#entries = ['Win7', 'Win8.1', 'Win10']['Awake', 'Sleep','Hibernate']['AMDS OFF', 'AMDS ON']

# for OS in range(len(entires)):
# 	for hostState in range(len(entires[0])):
# 		for amds in range(len(entires[0][0])):
# 			#entires.append({'Current:', current})
# 			print (OS, hostState, amds)

# for i in range(len(allOSInfo)):
# 	entries.append({'OS': 			allOSInfo[i].hostOS, 
# 					'HostState':	'Awake',
# 					'AMDS': 		0,
# 					'Current': 		current,
# 					'Battery': 		stateOfCharge(),
# 					'Comments':		''})


# entries[0]["Current"].average = 485.00
# entries[0]["Current"].minimum = 200.00
# entries[0]["Current"].maximum = 500.00

# if __name__ == '__main__':
	

# 	#initialize()

# 	for i in range(len(Win10Host)):
# 		if Win10Host[i].count('-') == 4:
# 			print ("OSID:", Win10Host[i])
# 		elif Win10Host[i].count('.') == 3:
# 			print ("IP Address:", Win10Host[i])
# 		elif "Windows" in Win10Host[i]:
# 			print ("Operating System:", Win10Host[i])

# 	print (Win10HostInfo.osid.count('-'))
# 	print (Win10HostInfo.hostIPAddress.count('.'))
# 	print ("Test") if "10" in Win10HostInfo.hostOS else print ("FAIL")

# 	currentStringResults(entries[0]["Current"], batteryRange(stateOfCharge()))
# 	print (entries[0]["Current"].avgResult)
# 	print (entries[0]["Current"].minResult)
# 	print (entries[0]["Current"].maxResult)

# 	checkHostState(Win10HostInfo)

# 	device = 'iPhone'

# 	for i in range(3):
# 		print(i)

# 	if device is 'iPhone':
# 		print ("PASSSSSSSS")

# 	# for i in range(len(allOSInfo)):
# 	# 	OSInfo = allOSInfo[i]
# 	# 	if checkOS():
# 	# 		setCommand("sleep")




# entries.append({'OS': 				OperatingSystems[i], 
# 				'HostState': 		'Awake',
# 				'AMDS': 			0,
# 				'Current': 			0, 
# 				'CurrentResult': 	'',
# 				'MaxCurrent': 		0,
# 				'MaxCurrentResult': '',
# 				'MinCurrent': 		0,
# 				'MinCurrentResult': '',
# 				'Comments': 		''})



# current = CurrentMeasurement()

# entries = []

# for i in range(len(allOSInfo)):
# 	entries.append({'OS': 			allOSInfo[i].hostOS, 
# 					'HostState':	'Awake',
# 					'AMDS': 		0,
# 					'Current': 		current,
# 					'Battery': 		stateOfCharge(),
# 					'Comments':		''})


# N71 = entries[0]['Current']

# print N71.minimum




	# Win7Data = Data[0][0]
	# Win8Data = Data[0][1]
	# Win10Data = Data[0][2]

	# selectDevice = Data[1]
	# deviceConfig = Data[2]
	# accessories = Data[3]
	# build = Data[4]

	# ipAddress = Data[5]
	# macAddress = Data[6]
	# emailAddress = Data[7]

	# docked = Data[8]
	# chargingPort = Data[9]
	# amds = Data[10]
	# #amds = chargingPort

	# entries = []
	# OSName = ['Windows 7', 'Windows 8.1', 'Windows 10']
	# OperatingSystems = []

	# for i in range(len(selectedOS)):
	# 	if Data[0][i][0] != 0:
	# 		selectedOS[i] = 1

	# if selectedOS[0]:
	# 	OperatingSystems.append('Windows 7')
	# if selectedOS[1]:
	# 	OperatingSystems.append('Windows 8.1')
	# if selectedOS[2]:
	# 	OperatingSystems.append('Windows 10')

	# if chargingPort:
	# 	amds = 0

	