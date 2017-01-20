#!/bin/env python
#==========================================================================
# (c) 2012  Total Phase, Inc.
#--------------------------------------------------------------------------
# Project : Beagle Sample Code
# File    : capture_usb5000_stats.py
#--------------------------------------------------------------------------
# Hardware-based Statistics Example for Beagle USB 5000
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================
import platform
import os

from beagle_py import *


#==========================================================================
# OS-SPECIFIC IMPORTS
#==========================================================================
SYSTEM = platform.system()

if SYSTEM == "Windows":
    import msvcrt
else:
    import termios
    import tty
    import select


#==========================================================================
# CONSTANTS
#==========================================================================
# Automatically configure the connection-specific USB 3.0 stats based on the
# first observed USB 3.0 Set Address request.
AUTO_CONFIG     = 1

UPDATE_INTERVAL = 50 # Milliseconds


#==========================================================================
# GLOBALS
#==========================================================================
# Variables
beagle           = 0
samplerate_khz   = 0
running          = True
console_settings = None


#==========================================================================
# GLOBAL MAPS
#==========================================================================
TYPE_MAP = {
    BG_USB_MATCH_TYPE_EQUAL     : "==",
    BG_USB_MATCH_TYPE_NOT_EQUAL : "!=",
}

SOURCE_MAP = {
    BG_USB_SOURCE_USB3_RX : "RX",
    BG_USB_SOURCE_USB3_TX : "TX",
}


#==========================================================================
# UTILITY FUNCTIONS
#==========================================================================
def print_hardware_based_stats_config (config):
    if AUTO_CONFIG and config.auto_config:
        dev  = "?"
        ep   = "?"
        src  = "?"
    else:
        if config.dev_match_type == BG_USB_MATCH_TYPE_DISABLED:
            dev = "X"
        else:
            dev = "%s %d" % (TYPE_MAP[config.dev_match_type],
                             config.dev_match_val)

        if config.ep_match_type == BG_USB_MATCH_TYPE_DISABLED:
            ep = "X"
        else:
            ep = "%s %d" % (TYPE_MAP[config.ep_match_type],
                            config.ep_match_val)

        if config.source_match_type == BG_USB_MATCH_TYPE_DISABLED:
            src = "X"
        else:
            src = "%s %s" % (TYPE_MAP[config.source_match_type],
                             SOURCE_MAP[config.source_match_val])

    print "----------------------------------------------"
    print "| USB 3.0 Connection-Specific Configuration  |"
    print "----------------------------------------------"
    print "| DEV: %7s | EP: %8s | SRC: %7s |" % (dev, ep, src)
    print "----------------------------------------------"

def print_hardware_based_stats (stats):
    print "----------------------------------------------"
    print "|   USB 3.0 Connection-Specific Statistics   |"
    print "----------------------------------------------"

    row_fmt = "| %6s | TX: %11s | RX: %11s |"
    tx_conn = stats.usb3_tx_conn
    rx_conn = stats.usb3_rx_conn

    print row_fmt % ("TXN",  tx_conn.txn,  rx_conn.txn)
    print row_fmt % ("DP",   tx_conn.dp,   rx_conn.dp)
    print row_fmt % ("ACK",  tx_conn.ack,  rx_conn.ack)
    print row_fmt % ("NRDY", tx_conn.nrdy, rx_conn.nrdy)

    print "----------------------------------------------"

    print "---------------------------------------------- --------------------------"
    print "|         USB 3.0 General Statistics         | |   USB 2.0 Statistics   |"
    print "---------------------------------------------- --------------------------"

    row_fmt = "| %6s | TX: %11s | RX: %11s | | %8s | %11s |"
    tx_gen  = stats.usb3_tx_gen
    rx_gen  = stats.usb3_rx_gen
    usb2    = stats.usb2

    print row_fmt % ("Link",     tx_gen.link,   rx_gen.link,
                     "SOF",      usb2.sof)
    print row_fmt % ("TXN",      tx_gen.txn,    rx_gen.txn,
                     "DATA",     usb2.data)
    print row_fmt % ("LGO U1",   tx_gen.lgo_u1, rx_gen.lgo_u1,
                     "IN-NAK",   usb2.in_nak)
    print row_fmt % ("ITP",      tx_gen.itp,    rx_gen.itp,
                     "PING-NAK", usb2.ping_nak)

    print "---------------------------------------------- --------------------------"


#==========================================================================
# CONSOLE UTILITY FUNCTIONS
#==========================================================================
def init_console ():
    if SYSTEM != "Windows":
        global console_settings

        # Save the console settings so they can be restored after running.
        console_settings = termios.tcgetattr(sys.stdin)

        # Set the console to character mode.
        tty.setcbreak(sys.stdin.fileno())

def restore_console ():
    if SYSTEM != "Windows":
        # Restore the console settings.
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, console_settings)

def is_key_available ():
    if SYSTEM == "Windows":
        return msvcrt.kbhit()
    else:
        rlist, _, _ = select.select([sys.stdin], [], [], 0)
        return bool(rlist)

def get_key ():
    if SYSTEM == "Windows":
        return msvcrt.getch()
    else:
        return sys.stdin.read(1)

def process_key (key):
    if key == 'q':
        global running
        running = False
    elif key == ' ':
        bg_usb_stats_reset(beagle)

def clear_console ():
    if SYSTEM == "Windows":
        os.system("cls")
    else:
        os.system("clear")


#==========================================================================
# HARDWARE-BASED STATISTICS CONFIGURATION
#==========================================================================
def usb_config_hardware_based_stats ():
    config = BeagleUsbStatsConfig()

    if AUTO_CONFIG:
        config.auto_config = 1
    else:
        config.source_match_type = BG_USB_MATCH_TYPE_EQUAL
        config.source_match_val  = BG_USB_SOURCE_TX
        config.ep_match_type     = BG_USB_MATCH_TYPE_EQUAL
        config.ep_match_val      = 1
        config.dev_match_type    = BG_USB_MATCH_TYPE_EQUAL
        config.dev_match_val     = 1

    if bg_usb_stats_config(beagle, config) != BG_OK:
        print "error: could not configure hardware-based statistics"
        sys.exit(1)


#==========================================================================
# USB DUMP
#==========================================================================
# The main packet dump routine
def usb_dump (cap_mask):
    # Initialize the console.
    init_console()

    # Configure Beagle 5000 for non-immediate trigger.
    if bg_usb_configure(beagle, cap_mask,
                        BG_USB_TRIGGER_MODE_EVENT) != BG_OK:
        print "error: could not configure Beagle 5000 with desired mode"
        sys.exit(1)

    # Start the capture.
    if (bg_enable(beagle, BG_PROTOCOL_USB) != BG_OK):
        print "error: could not enable USB capture; exiting..."
        sys.exit(1)

    # Start printing statistics.
    while running:
        # Check for user keyboard input.
        if is_key_available():
            process_key(get_key())

        status, config = bg_usb_stats_config_query(beagle)
        status, stats  = bg_usb_stats_read(beagle)

        clear_console()

        print_hardware_based_stats_config(config)
        print_hardware_based_stats(stats)

        print "\n: <Press SPACE to reset, q to quit>"

        sys.stdout.flush()

        bg_sleep_ms(UPDATE_INTERVAL)

    # Stop the capture.
    bg_disable(beagle)

    # Restore the console.
    restore_console()


#==========================================================================
# USAGE INFORMATION
#==========================================================================
def print_usage ():
    print """Usage: capture_usb5000_stats source
Example utility for observing USB statistics from a Beagle 5000 analyzer.

    capture_usb5000_stats runs a capture on a Beagle 5000 analyzer and
    displays several tables of hardware-based USB statistics.  To reset the
    counts, press SPACE.  To exit the program, press "q".

    The parameter source determines which USB source to capture on.
    The source can be set to either: both, usb2, or usb3.
    Note that only analyzers licensed for the simultaneous feature will
    be able to capture both sources at the same time.

For product documentation and specifications, see www.totalphase.com."""
    sys.stdout.flush()


#==========================================================================
# MAIN PROGRAM ENTRY POINT
#==========================================================================
port       = 0      # open port 0 by default
timeout    = 100    # in milliseconds
latency    = 200    # in milliseconds
num        = 0

if len(sys.argv) < 2:
    print_usage()
    sys.exit(1)

if not sys.argv[1] in ['usb2', 'usb3', 'both']:
    print_usage()
    sys.exit(1)

if sys.argv[1] == 'usb2':
    cap_mask = BG_USB_CAPTURE_USB2
elif sys.argv[1] == 'usb3':
    cap_mask = BG_USB_CAPTURE_USB3
else:
    cap_mask = BG_USB_CAPTURE_USB3 | BG_USB_CAPTURE_USB2

# Open the device.
beagle = bg_open(port)
if (beagle <= 0):
    print "Unable to open Beagle device on port %d" % port
    print "Error code = %d" % beagle
    sys.exit(1)

print "Opened Beagle device on port %d" % port

# Query the samplerate since Beagle USB has a fixed sampling rate.
samplerate_khz = bg_samplerate(beagle, samplerate_khz)
if (samplerate_khz < 0):
    print "error: %s" % bg_status_string(samplerate_khz)
    sys.exit(1)

print "Sampling rate set to %d KHz." % samplerate_khz

# Set the idle timeout.
# The Beagle read functions will return in the specified time
# if there is no data available on the bus.
bg_timeout(beagle, timeout)
print "Idle timeout set to %d ms." %  timeout

# Set the latency.
# The latency parameter allows the programmer to balance the
# tradeoff between host side buffering and the latency to
# receive a packet when calling one of the Beagle read
# functions.
bg_latency(beagle, latency)
print "Latency set to %d ms." % latency

print "Host interface is %s." % \
      (bg_host_ifce_speed(beagle) and "high speed" or "full speed")

print ""
sys.stdout.flush()

# Configure hardware-based statistics.
usb_config_hardware_based_stats()

# Output statistics table.
usb_dump(cap_mask)

# Close the device.
bg_close(beagle)

sys.exit(0)
