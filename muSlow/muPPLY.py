import RPi.GPIO as GPIO
import can
import time
import os
import struct


SUPPLYlist = [0x20]
#CMDlist = [0x06, 0x0a, 0x0c, 0x15, 0x16, 0x07, 0x0b, 0x0d, 0x17, 0x18]

led = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,True)

count = 0

print('\n\rCAN Rx test')
print('Bring up CAN0....')

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

# Main loop
try:
	for ID in SUPPLYlist :
		GPIO.output(led,True)
		msg = can.Message(arbitration_id=ID,data=[0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
		bus.send(msg)
		time.sleep(0.1)
		GPIO.output(led,False)
		time.sleep(0.1)
		message = bus.recv()	# Wait until a message is received.
	GPIO.output(led,False)
	os.system("/sbin/ip link set can0 down")

except KeyboardInterrupt:
	#Catch keyboard interrupt
	GPIO.output(led,False)
	os.system("/sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')
