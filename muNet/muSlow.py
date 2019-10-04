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

light = 'RED'
while light == 'RED' :
	try :
		outFile = open('/home/DatiTB/DTC/ENV_' + sys.argv[1] + '.txt','r')
		s = outFile.readlines()
		outFile.close()
		light = 'GREEN'
	except :
		print ('\n +++ RESOURCE ENV_' + sys.argv[1] + '.txt BUSY! NEW TRY IN FEW SECONDS +++\n')
		time.sleep(5)

light = 'RED'
while light == 'RED' :
	try :
		outFile = open('/home/DatiTB/DTC/ENV_' + sys.argv[1] + '.txt', 'w')
		outFile.write('$FLG\t2\n')
		outFile.write(s[1])
		outFile.write(s[2])
		outFile.write(s[3])
		outFile.write('$WP\t-1\n')
		outFile.close()
		light = 'GREEN'
	except :
		print ('\n +++ RESOURCE ENV_' + sys.argv[1] + '.txt BUSY! NEW TRY IN FEW SECONDS +++\n')
		time.sleep(5)

if (sys.argv[1] == 'ALL') :
	TEClist = [0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11]
	TEClist_2C = [0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11]
if (sys.argv[1] == 'NERO') :
	TEClist = [0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09]
	TEClist_2C = [0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09]
elif (sys.argv[1] == 'ROSSO') :
	TEClist = [0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11]
	TEClist_2C = [0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11]

CMDlist = [0x06, 0x08, 0x0a, 0x0c, 0x11, 0x12, 0x15, 0x16, 0x1b, 0x1c, 0x07, 0x09, 0x0b, 0x0d, 0x13, 0x14, 0x17, 0x18, 0x1d, 0x1e]

WP_hex_35 = [0x00, 0x00, 0x0c, 0x42]
WP_hex_30 = [0x00, 0x00, 0xf0, 0x41]
WP_hex_25 = [0x00, 0x00, 0xc8, 0x41]
WP_hex_20 = [0x00, 0x00, 0xa0, 0x41]
WP_hex_15 = [0x00, 0x00, 0x70, 0x41]
WP_hex_10 = [0x00, 0x00, 0x20, 0x41]
WP_hex_6 = [0x00, 0x00, 0xc0, 0x40]

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

env = [0,0,0]
print('\n --- READING ENVIRONMENTAL SENSORS --- \n ')
light = 'RED'
while light == 'RED' :
	try :
		outFile = open('/home/DatiTB/DTC/ENV_' + sys.argv[1] + '.txt','r')
		s = outFile.readlines()
		outFile.close()
		light = 'GREEN'
	except :
		print ('\n +++ RESOURCE ENV_' + sys.argv[1] + '.txt BUSY! NEW TRY IN FEW SECONDS +++\n')
		time.sleep(5)
for iii in range (1,4) : 
	support = s[iii].split('\t')
	support[1] = support[1].replace('\n', '')
	env[iii-1] = int(support[1])
TMP = env[0]
RH = env[1]
DEW = env[2]	
print ('Temperature : ' + str(TMP))
print ('R. Humidity : ' + str(RH))
WP_set = -1

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

input('Premi Ctrl-C')

try:
	while True:
		inFile = open('/home/DatiTB/DTC/RI_' + sys.argv[1] + '.txt', 'r')
		s = inFile.readline()
		a = s.split('\t')
		run = str(a[1].replace('\n', ''))
		inFile.close()

		outFile = open('/home/DatiTB/DTC/slowTemp_' + sys.argv[1],'a')

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
							if (a[0] != '0x20') and (a[0] != '0x22'):
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
		
		env = [0,0,0]
		print('\n --- READING ENVIRONMENTAL SENSORS --- \n ')
		
		while light == 'RED' :
			try :
				outFile = open('/home/DatiTB/DTC/ENV_' + sys.argv[1] + '.txt','r')
				s = outFile.readlines()
				outFile.close()
				light = 'GREEN'
			except :
				print ('\n +++ RESOURCE ENV_' + sys.argv[1] + '.txt BUSY! NEW TRY IN FEW SECONDS +++\n')
				time.sleep(5)
		
		for iii in range (1,4) : 
			support = s[iii].split('\t')
			support[1] = support[1].replace('\n', '')
			env[iii-1] = int(support[1])
		TMP = env[0]
		RH = env[1]
		DEW = env[2]	
		print ('Temperature : ' + str(TMP))
		print ('R. Humidity : ' + str(RH))
		
		# CODICE GESTIONE TEC

		WP_sup = s[4].split('\t')
		WP_sup[1] = WP_sup[1].replace('\n', '')
		WP = int(WP_sup[1])
		WP_set = -1
		FLG = 0 

		if (TMP>=21 and TMP<=32 and (25-DEW)>2) : WP_set = 25
		elif (TMP>=15 and TMP<=22 and (20-DEW)>2) : WP_set = 20
		elif (TMP>=10 and TMP<=18 and (15-DEW)>2) : WP_set = 15
		elif (TMP>=5 and TMP<=13 and (10-DEW)>2) : WP_set = 10
		elif (TMP>=1 and TMP<=9 and (6-DEW)>2) : WP_set = 6

		if (TMP>21 and TMP<32 and (25-DEW)>2 and WP == 25) :
			WP_set = 25
		if (TMP>15 and TMP<22 and (20-DEW)>2 and WP == 20) :
			WP_set = 20
		if (TMP>10 and TMP<18 and (15-DEW)>2 and WP == 15) :
			WP_set = 15
		if (TMP>5 and TMP<13 and (10-DEW)>2 and WP == 10) :
			WP_set = 10
		if (TMP>1 and TMP<9 and (6-DEW)>2 and WP == 6) :
			WP_set = 6
		
		if (WP_set == 25) : WP_hex = WP_hex_25
		elif (WP_set == 20) : WP_hex = WP_hex_20
		elif (WP_set == 15) : WP_hex = WP_hex_15
		elif (WP_set == 10) : WP_hex = WP_hex_10
		elif (WP_set == 6) : WP_hex = WP_hex_6
		
		light = 'RED'
		while light == 'RED' :
			try :
				outFile = open('/home/DatiTB/DTC/ENV_' + sys.argv[1] + '.txt','w')
				light = 'GREEN'
			except :
				print ('\n +++ RESOURCE ENV_' + sys.argv[1] + '.txt BUSY! NEW TRY IN FEW SECONDS +++\n')
				time.sleep(5)
		
		if (WP_set!=-1 and WP!=WP_set) :
			outFile.write('$FLG\t1\n')
			FLG = 1
		elif (WP_set == -1) :
			if (WP != WP_set) : 
				# SPEGNIMENTO TEC
				for ID in TEClist :
					GPIO.output(led,True)
					msg = can.Message(arbitration_id=ID,data=[0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
					bus.send(msg)
					time.sleep(0.3)
					GPIO.output(led,False)
					time.sleep(0.3)
					message = bus.recv()	# Wait until a message is received.
				# END

			outFile.write('$FLG\t1\n')
			
		else : outFile.write('$FLG\t0\n')
		outFile.write('$TMP\t' + str(TMP) + '\n')
		outFile.write('$RH\t' + str(RH) + '\n')
		outFile.write('$DEW\t' + str(DEW) + '\n')
		outFile.write('$WP\t' + str(WP_set) + '\n')
		outFile.close()
		
		TMP_MEM = TMP
		RH_MEM = RH
		
		print('WP2SET : ' + str(WP_set) + '\n') 

		if (WP_set == -1) : FLG = 0	
		if (FLG == 1) : 
			while (FLG == 1) :
				if (WP == -1) :
					print('\n --- POWERING UP TECs ---\n')

					# ACCENSIONE TEC
					for ID in TEClist :
						GPIO.output(led,True)
						msg = can.Message(arbitration_id=ID,data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
						bus.send(msg)
						time.sleep(0.3)
						GPIO.output(led,False)
						time.sleep(0.3)
						message = bus.recv(1.0)	# Wait until a message is received.
					for ID in TEClist_2C :
						GPIO.output(led,True)
						msg = can.Message(arbitration_id=ID,data=[0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3f],extended_id=False)
						bus.send(msg)
						time.sleep(0.3)
						GPIO.output(led,False)
						time.sleep(0.3)
						message = bus.recv(1.0)	# Wait until a message is received.
					time.sleep(60)
					for ID in TEClist_2C :
						GPIO.output(led,True)
						msg = can.Message(arbitration_id=ID,data=[0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3f],extended_id=False)
						bus.send(msg)
						time.sleep(0.3)
						GPIO.output(led,False)
						time.sleep(0.3)
						message = bus.recv(1.0)	# Wait until a message is received.
					# END

				light = 'RED'
				while light == 'RED' :
					try :
						outFile = open('/home/DatiTB/DTC/ENV_' + sys.argv[1] + '.txt','r')
						s = outFile.readlines()
						outFile.close()
						light = 'GREEN'
					except :
						print ('\n +++ RESOURCE ENV_' + sys.argv[1] + '.txt BUSY! NEW TRY IN FEW SECONDS +++\n')
						time.sleep(5)
				RUNflag = s[0].split('\t')
				RUNflag[1] = RUNflag[1].replace('\n','')
				if (int(RUNflag[1]) == 1) :
					# IMPOSTAZIONE TEMPERATURA 
					#go = 0
					print('\n --- APPLYING TEMPERATURE SETTINGS ---\n')

					go = 0
					for ID in TEClist_2C :
						GPIO.output(led,True)
						msg = can.Message(arbitration_id=ID,data=[0x00, 0x04, 0x00, 0x00, WP_hex[0], WP_hex[1], WP_hex[2], WP_hex[3]],extended_id=False)
						bus.send(msg)
						time.sleep(0.3)
						GPIO.output(led,False)
						time.sleep(0.3)
						message = bus.recv(1.0)
					time.sleep(60)
					for ID in TEClist_2C :
						GPIO.output(led,True)
						msg = can.Message(arbitration_id=ID,data=[0x00, 0x05, 0x00, 0x00, WP_hex[0], WP_hex[1], WP_hex[2], WP_hex[3]],extended_id=False)
						bus.send(msg)
						time.sleep(0.3)
						GPIO.output(led,False)
						time.sleep(0.3)
						message = bus.recv(1.0)
					# END
					FLG = 0
				else : time.sleep(30)
		else : 
			print('ATTENDO 5 MINUTI!!!\n')
			time.sleep(300)
		i = i+1
except KeyboardInterrupt:
	#Catch keyboard interrupt
	GPIO.output(led,False)
	os.system("/sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')


