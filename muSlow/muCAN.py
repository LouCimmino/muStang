import RPi.GPIO as GPIO
import can
import time
import os
import struct


TEClist = [0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11]
#CMDlistA = [0x06, 0x0a, 0x0c, 0x15, 0x16, 0x19]
#CMDlistB = [0x07, 0x0b, 0x0d, 0x17, 0x18, 0x1a]
CMDlist = [0x06, 0x0a, 0x0c, 0x15, 0x16, 0x07, 0x0b, 0x0d, 0x17, 0x18]

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
	for ID in TEClist :
		GPIO.output(led,True)
		msg = can.Message(arbitration_id=ID,data=[0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
		bus.send(msg)
		time.sleep(0.3)
		GPIO.output(led,False)
		time.sleep(0.3)
		message = bus.recv()	# Wait until a message is received.
		GPIO.output(led,True)
		msg = can.Message(arbitration_id=ID,data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
		bus.send(msg)
		time.sleep(0.3)
		GPIO.output(led,False)
		time.sleep(0.3)
		message = bus.recv()	# Wait until a message is received.
		GPIO.output(led,True)
		msg = can.Message(arbitration_id=ID,data=[0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
		bus.send(msg)
		time.sleep(0.3)
		GPIO.output(led,False)
		time.sleep(0.3)
		message = bus.recv()	# Wait until a message is received.

	while True:
		count +=1
		for ID in TEClist :
			for CMD in CMDlist :
				logStr = ''
				check = 0
				while (check == 0) : 
					bicheck = 0
					GPIO.output(led,True)
					msg = can.Message(arbitration_id=ID,data=[0x00, CMD, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
					bus.send(msg)
					time.sleep(0.3)
					while (bicheck == 0) : 
						GPIO.output(led,False)
						time.sleep(0.3)
						message = bus.recv()	# Wait until a message is received.
						c = '{0:x} {1:x} '.format(message.arbitration_id, message.dlc)
						s=''
						for i in range(message.dlc):
							s +=  '{0:x} '.format(message.data[i])
						a = s.split(' ')
						#print(a)
						if a[0] != '20' :
							print(a)
							sfh = a[7].replace('0x','') + a[6].replace('0x','') + a[5].replace('0x','') + a[4].replace('0x','')
							n = struct.unpack('f', struct.pack('i', int(sfh, 16)))
							logStr = logStr + str(round(n[0], 2)) + '\t'
							check = 1
							bicheck = 1
						else :
							bicheck = 0
				logStr = logStr + '\n'
				print(logStr)
except KeyboardInterrupt:
	#Catch keyboard interrupt
	GPIO.output(led,False)
	os.system("/sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')
