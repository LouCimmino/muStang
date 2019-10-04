import os
import sys
import time
import subprocess
import datetime
import math
import RPi.GPIO as GPIO
import can
import struct
import Adafruit_DHT as dht

outFile = open('/home/DatiTB/DTC/ENV.txt', 'w')
outFile.write('$FLG\t2\n')
outFile.write('$TMP\t0\n')
outFile.write('$RH\t100\n')
outFile.write('$DEW\t0\n')
outFile.write('$WP\t-1\n')
outFile.close()

TMP_MEM = 0.0
RH_MEM = 100.0

if sys.argv[1] == 'ALL' :
	TEClist = [0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11]
	TEClist_2C = [0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11]
if sys.argv[1] == 'NERO' :
	TEClist = [0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09]
	TEClist_2C = [0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09]
if sys.argv[1] == 'ROSSO' :
	TEClist = [0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11]
	TEClist_2C = [0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11]

CMDlist = [0x06, 0x08, 0x0a, 0x0c, 0x11, 0x12, 0x15, 0x16, 0x1b, 0x1c, 0x07, 0x09, 0x0b, 0x0d, 0x13, 0x14, 0x17, 0x18, 0x1d, 0x1e]

WP_hex_34 = [0x00, 0x00, 0x18, 0x42]
WP_hex_30 = [0x00, 0x00, 0xf0, 0x41]
WP_hex_24 = [0x00, 0x00, 0xd0, 0x41]
WP_hex_25 = [0x00, 0x00, 0xc8, 0x41]
WP_hex_20 = [0x00, 0x00, 0xa0, 0x41]
WP_hex_15 = [0x00, 0x00, 0x70, 0x41]
WP_hex_10 = [0x00, 0x00, 0x20, 0x41]
WP_hex_6 = [0x00, 0x00, 0xc0, 0x40]

counter = 0

led = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,True)

print('\n\rCAN Rx test')
print('Bring up CAN0....')

GPIO.output(led,False)
#os.system("/sbin/ip link set can0 down")

# Bring up can0 interface at 500kbps
#os.system("/sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)	
print('Press CTL-C to exit')

WP_set = -1
FLG = 0
# --- COMMENTA QUI
TMP = -273.15
RH = 100.0
#---- FINE ----



try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print('Cannot find PiCAN board.')
	GPIO.output(led,False)
	exit()

i = 0
for ID in TEClist :
	GPIO.output(led,True)
	msg = can.Message(arbitration_id=ID,data=[0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
	bus.send(msg)
	time.sleep(0.3)
	GPIO.output(led,False)
	time.sleep(0.3)
	message = bus.recv(1.0)	# Wait until a message is received.
	GPIO.output(led,True)
	msg = can.Message(arbitration_id=ID,data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
	bus.send(msg)
	time.sleep(0.3)
	GPIO.output(led,False)
	time.sleep(0.3)
	message = bus.recv(1.0)	# Wait until a message is received.
	GPIO.output(led,True)
	msg = can.Message(arbitration_id=ID,data=[0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
	bus.send(msg)
	time.sleep(0.3)
	GPIO.output(led,False)
	time.sleep(0.3)
	message = bus.recv(1.0)
	GPIO.output(led,True)
	msg = can.Message(arbitration_id=ID,data=[0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
	bus.send(msg)
	time.sleep(0.3)
	GPIO.output(led,False)
	time.sleep(0.3)
	message = bus.recv(1.0)
	GPIO.output(led,True)
	msg = can.Message(arbitration_id=ID,data=[0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
	bus.send(msg)
	time.sleep(0.3)
	GPIO.output(led,False)
	time.sleep(0.3)
	message = bus.recv(1.0)

	GPIO.output(led,True)
	msg = can.Message(arbitration_id=ID,data=[0x00, 0x0e, 0x00, 0x00, 0x00, 0x00, 0x7a, 0x45],extended_id=False)
	bus.send(msg)
	time.sleep(0.3)
	GPIO.output(led,False)
	time.sleep(0.3)
	message = bus.recv(1.0)
	GPIO.output(led,True)
	msg = can.Message(arbitration_id=ID,data=[0x00, 0x0f, 0x00, 0x00, 0x00, 0x00, 0x7a, 0x45],extended_id=False)
	bus.send(msg)
	time.sleep(0.3)
	GPIO.output(led,False)
	time.sleep(0.3)
	message = bus.recv(1.0)


#input('Premi Ctrl-C')

try:
	while True:
		inFile = open('/home/DatiTB/DTC/RI_' + sys.argv[1] + '.txt', 'r')
		s = inFile.readline()
		a = s.split('\t')
		run = str(a[1].replace('\n', ''))
		inFile.close()

		outFile = open('/home/DatiTB/DTC/slowTemp_' + sys.argv[1] + '_dump_00','a')

		now = str(datetime.datetime.now())

		print('\n --- READING DETECTOR SENSORS --- \n ')
		logStr = ''
		
		for ID in TEClist :
			logStr_part = ''
			for CMD in CMDlist :
				check = 0
				try : 
					while (check == 0) : 
						bicheck = 0
						GPIO.output(led,True)
						msg = can.Message(arbitration_id=ID,data=[0x00, CMD, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
						bus.send(msg)
						time.sleep(0.3)
						while (bicheck == 0) : 
							GPIO.output(led,False)
							time.sleep(0.3)
							message = bus.recv(1.0)	# Wait until a message is received.
							c = '{0:x} {1:x} '.format(message.arbitration_id, message.dlc)
							s=''
							for ii in range(message.dlc):
								s +=  '{0:#x} '.format(message.data[ii])
							a = s.split(' ')
							#print(a)
							if (a[0] != '0x22') and (a[0] != '0x20') :
								b = ['', '', '', '']
								#print(a)
								for jj in range(4,8):
									b[jj - 4] = a[jj].replace('0x','')
									if (int(b[jj-4], 16) >= 0) and (int(b[jj-4], 16) <= 15) : a[jj] =  '0' + b[jj-4]
								sfh = a[7].replace('0x','') + a[6].replace('0x','') + a[5].replace('0x','') + a[4].replace('0x','')
								#print(sfh)
								n = struct.unpack('f', struct.pack('i', int(sfh, 16)))
								logStr = logStr + str(round(n[0], 2)) + '\t'
								logStr_part = logStr_part + str(round(n[0], 2)) + '\t'
								check = 1
								bicheck = 1
							else :
								bicheck = 0
				except :
					print('--- SKIP ---')
					logStr = logStr + '0.00\t'
					logStr_part = logStr_part + '0.00\t'

			print(logStr_part)
		outFile.write(str(i) + '\t' + run + '\t' + str(TMP)  + '\t' + str(RH)  + '\t' + str(WP_set)  + '\t' +  logStr + now + '\n')
		outFile.close()
		
		# CODICE GESTIONE TEC
		if (WP_set == -1) :			
			go = 0
			for ID in TEClist_2C :
				if (go == 1) : time.sleep(1)
				GPIO.output(led,True)
#				msg = can.Message(arbitration_id=ID,data=[0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
				msg = can.Message(arbitration_id=ID,data=[0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3f],extended_id=False)
				bus.send(msg)
				time.sleep(0.3)
				GPIO.output(led,False)
				time.sleep(0.3)
				message = bus.recv(1.0)
				go = 1
			go = 0
			time.sleep(60)
			for ID in TEClist_2C :
				if (go == 1) : time.sleep(1)
				time.sleep(3)
				GPIO.output(led,True)
#				msg = can.Message(arbitration_id=ID,data=[0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
				msg = can.Message(arbitration_id=ID,data=[0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3f],extended_id=False)
				bus.send(msg)
				time.sleep(0.3)
				GPIO.output(led,False)
				time.sleep(0.3)
				message = bus.recv(1.0)
				go = 1



		WP = 40
		# ---- COMMENTA QUI ----
		TMP = 12
		DEW = 0
		RH = 50
		#---- FINE ----


		if (counter % 2 == 0) : WP_set = 30
		else : WP_set = 25
		
		if (WP_set == 30) : WP_hex = WP_hex_30
		elif (WP_set == 25) : WP_hex = WP_hex_25
		# END

		TMP_MEM = TMP
		RH_MEM = RH
		
		print('\nWP2SET : ' + str(WP_set) + '\n') 
		
		if (FLG == 0) :
			# END
			# IMPOSTAZIONE TEMPERATURA 
		
			print('\n --- POWER ON TECs ---\n')
			go = 0
			for ID in TEClist_2C :
				if (go == 1) : time.sleep(1)
				GPIO.output(led,True)
				msg = can.Message(arbitration_id=ID,data=[0x00, 0x04, 0x00, 0x00, WP_hex[0], WP_hex[1], WP_hex[2], WP_hex[3]],extended_id=False)
				bus.send(msg)
				time.sleep(0.3)
				GPIO.output(led,False)
				time.sleep(0.3)
				message = bus.recv(1.0)	# Wait until a message is received.
				go = 1
			time.sleep(60)
			go = 0
			for ID in TEClist_2C :
				if (go == 1) : time.sleep(1)
				GPIO.output(led,True)
				msg = can.Message(arbitration_id=ID,data=[0x00, 0x05, 0x00, 0x00, WP_hex[0], WP_hex[1], WP_hex[2], WP_hex[3]],extended_id=False)
				bus.send(msg)
				time.sleep(0.3)
				GPIO.output(led,False)
				time.sleep(0.3)
				message = bus.recv(1.0)	# Wait until a message is received.
				go = 1
			# END
			FLG = 1
		else : 
			counter = counter + 1
			print('ATTENDO 5 MINUTI!!!\n')
			time.sleep(300)
			FLG = 0
	i = i+1
except KeyboardInterrupt:
	#Catch keyboard interrupt
	GPIO.output(led,False)
	#os.system("/sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')


