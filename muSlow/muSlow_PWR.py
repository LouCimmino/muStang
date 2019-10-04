import os
import sys
import time
import subprocess
import datetime
import math
import RPi.GPIO as GPIO
import can
import struct

PWRlist = [0x20]

led = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,True)

print('\n\rCAN Rx test')
print('Bring up CAN0....')

GPIO.output(led,False)
os.system("/sbin/ip link set can0 down")

# Bring up can0 interface at 500kbps
os.system("/sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
print('Press CTL-C to exit')

try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print('Cannot find PiCAN board.')
	GPIO.output(led,False)
	exit()

for ID in PWRlist :
	GPIO.output(led,True)
	msg = can.Message(arbitration_id=ID,data=[0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3f],extended_id=False)
#	msg = can.Message(arbitration_id=ID,data=[0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
	bus.send(msg)
	time.sleep(0.3)
	GPIO.output(led,False)
	time.sleep(0.3)
	message = bus.recv(1.0)	# Wait until a message is received.

GPIO.output(led,False)
os.system("/sbin/ip link set can0 down")

