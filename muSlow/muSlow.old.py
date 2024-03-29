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

TEClist = [0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11]
#TEClist_2C = [0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11]
TEClist_2C = [0x0a, 0x0b]
#TEClist_2C = [0x0a, 0x0b]
#TEClist_2C = [0x10]

CMDlist = [0x06, 0x08, 0x0a, 0x0c, 0x11, 0x12, 0x15, 0x16, 0x1b, 0x1c, 0x07, 0x09, 0x0b, 0x0d, 0x13, 0x14, 0x17, 0x18, 0x1d, 0x1e]

WP_hex_34 = [0x00, 0x00, 0x08, 0x42]
WP_hex_32 = [0x00, 0x00, 0x00, 0x42]
WP_hex_30 = [0x00, 0x00, 0xf0, 0x41]
WP_hex_27 = [0x00, 0x00, 0xd8, 0x41]
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
#os.system("/sbin/ip link set can0 down")

# Bring up can0 interface at 500kbps
#os.system("/sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
print('Press CTL-C to exit')

h = None
t = None
RH = 1000
TMP = -273
print('\n --- READING ENVIRONMENTAL SENSORS --- \n ')
while (RH > 110):
	#while (h==None and t==None) :
	h,t = dht.read_retry(dht.DHT22, 14)
	if h!=None : RH = round(float(h), 2)
	else : RH = RH_MEM
	if t!=None : TMP = round(float(t), 2)
	else : TMP = TMP_MEM
print ('Temperature : ' + str(TMP))
print ('R. Humidity : ' + str(RH))
Es = 6.11*math.pow(10,(7.5*TMP/(237.7+TMP)))
E = RH*Es/100
DEW = round((-430.22 + (237.7*math.log(E)))/(-math.log(E)+19.08))
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
	msg = can.Message(arbitration_id=ID,data=[0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
	bus.send(msg)
	time.sleep(0.3)
	GPIO.output(led,False)
	time.sleep(0.3)
	message = bus.recv(1.0)
	GPIO.output(led,True)
	msg = can.Message(arbitration_id=ID,data=[0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
	bus.send(msg)
	time.sleep(0.3)
	GPIO.output(led,False)
	time.sleep(0.3)
	message = bus.recv(1.0)
	GPIO.output(led,True)
	msg = can.Message(arbitration_id=ID,data=[0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00],extended_id=False)
	bus.send(msg)
	time.sleep(0.3)
	GPIO.output(led,False)
	time.sleep(0.3)
	message = bus.recv(1.0)

input('Premi control-C')

try:
	while True:
		inFile = open('/home/DatiTB/DTC/RI.txt', 'r')
		s = inFile.readline()
		a = s.split('\t')
		run = str(a[1].replace('\n', ''))
		inFile.close()

		outFile = open('/home/DatiTB/DTC/slowTemp_ROSSO','a')

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
							if a[0] != '0x20' :
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

		h = None
		t = None
		RH = 1000
		TMP = -273
		print('\n --- READING ENVIRONMENTAL SENSORS --- \n ')
		while (RH > 110):
			#while (h==None and t==None) :
			h,t = dht.read_retry(dht.DHT22, 14)
			if h!=None : RH = round(float(h), 2)
			else : RH = RH_MEM
			if t!=None : TMP = round(float(t), 2)
			else : TMP = TMP_MEM
		print ('Temperature : ' + str(TMP))
		print ('R. Humidity : ' + str(RH))
		Es = 6.11*math.pow(10,(7.5*TMP/(237.7+TMP)))
		E = RH*Es/100
		DEW = round((-430.22 + (237.7*math.log(E)))/(-math.log(E)+19.08))

		outFile = open('/home/DatiTB/DTC/ENV.txt','r')
		s = outFile.readlines()
		outFile.close()
		# CODICE GESTIONE TEC

		WP_sup = s[4].split('\t')
		WP_sup[1] = WP_sup[1].replace('\n', '')
		WP = int(WP_sup[1])
		WP_set = -1
		# ---- COMMENTA QUI ----
		#WP_set = 27
		#TMP = 10
		#DEW = 0
		#RH = 50
		#---- FINE ----
		FLG = 0


		if (TMP>=28 and TMP<=35 and (30-DEW)>2) : WP_set = 30
		elif (TMP>=20 and TMP<=28 and (25-DEW)>2) : WP_set = 25
		elif (TMP>=15 and TMP<=23 and (20-DEW)>2) : WP_set = 20
		elif (TMP>=10 and TMP<=18 and (15-DEW)>2) : WP_set = 15
		elif (TMP>=5 and TMP<=13 and (10-DEW)>2) : WP_set = 10
		elif (TMP>=1 and TMP<=9 and (6-DEW)>2) : WP_set = 6

		if (TMP>=28 and TMP<35 and (30-DEW)>2 and WP == 30) :
			WP_set = 30
		if (TMP>20 and TMP<28 and (25-DEW)>2 and WP == 25) :
			WP_set = 25
		if (TMP>15 and TMP<23 and (20-DEW)>2 and WP == 20) :
			WP_set = 20
		if (TMP>10 and TMP<18 and (15-DEW)>2 and WP == 15) :
			WP_set = 15
		if (TMP>5 and TMP<13 and (10-DEW)>2 and WP == 10) :
			WP_set = 10
		if (TMP>1 and TMP<9 and (6-DEW)>2 and WP == 6) :
			WP_set = 6

		if (WP_set == 30) : 
			WP_hex = WP_hex_30
			WP_hex_fs = WP_hex_34
			WP_hex_sn = WP_hex_32
		elif (WP_set == 25) : WP_hex = WP_hex_25
		elif (WP_set == 27) : WP_hex = WP_hex_27
		elif (WP_set == 20) : WP_hex = WP_hex_20
		elif (WP_set == 15) : WP_hex = WP_hex_15
		elif (WP_set == 10) : WP_hex = WP_hex_10
		elif (WP_set == 6) : WP_hex = WP_hex_6
		# END

		outFile = open('/home/DatiTB/DTC/ENV.txt','w')
		if (WP_set!=-1 and WP!=WP_set) :
			outFile.write('$FLG\t1\n')
			FLG = 1
		elif (WP_set == -1) :
			if (WP != WP_set) :
				# Disab. POWER TEC
				for ID in TEClist :
					GPIO.output(led,True)
					msg = can.Message(arbitration_id=ID,data=[0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
					bus.send(msg)
					time.sleep(0.3)
					GPIO.output(led,False)
					time.sleep(0.3)
					message = bus.recv(1.0)
					GPIO.output(led,True)
					msg = can.Message(arbitration_id=ID,data=[0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00],extended_id=False)
					bus.send(msg)
					time.sleep(0.3)
					GPIO.output(led,False)
					time.sleep(0.3)
					message = bus.recv(1.0)

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
				#if (WP == -1) :
					# ACCENSIONE TEC
				#	for ID in TEClist :
				#		GPIO.output(led,True)
				#		msg = can.Message(arbitration_id=ID,data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
				#		bus.send(msg)
				#		time.sleep(0.3)
				#		GPIO.output(led,False)
				#		time.sleep(0.3)
				#		message = bus.recv(1.0)	# Wait until a message is received.
					# END
				inpFile = open('/home/DatiTB/DTC/ENV.txt','r')
				s = inpFile.readlines()
				inpFile.close()
				RUNflag = s[0].split('\t')
				RUNflag[1] = RUNflag[1].replace('\n','')
				if (int(RUNflag[1]) == 1) :
					# IMPOSTAZIONE TEMPERATURA
					#go = 0
					for ID in TEClist_2C :
						#if (go == 1) : time.sleep(120)
						GPIO.output(led,True)
						msg = can.Message(arbitration_id=ID,data=[0x00, 0x04, 0x00, 0x00, WP_hex[0], WP_hex[1], WP_hex[2], WP_hex[3]],extended_id=False)
						bus.send(msg)
						time.sleep(0.3)
						GPIO.output(led,False)
						time.sleep(0.3)
						message = bus.recv(1.0)	# Wait until a message is received.
						#go= 1
					for ID in TEClist_2C :
						#time.sleep(120)
						GPIO.output(led,True)
						msg = can.Message(arbitration_id=ID,data=[0x00, 0x05, 0x00, 0x00, WP_hex[0], WP_hex[1], WP_hex[2], WP_hex[3]],extended_id=False)
						bus.send(msg)
						time.sleep(0.3)
						GPIO.output(led,False)
						time.sleep(0.3)
						message = bus.recv(1.0)	# Wait until a message is received.
					go = 0
					for ID in TEClist_2C :
						if (go == 1) : time.sleep(120)
						GPIO.output(led,True)
						msg = can.Message(arbitration_id=ID,data=[0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3f],extended_id=False)
						bus.send(msg)
						time.sleep(0.3)
						GPIO.output(led,False)
						time.sleep(0.3)
						message = bus.recv(1.0)
						time.sleep(120)
						go = 1
						GPIO.output(led,True)
						msg = can.Message(arbitration_id=ID,data=[0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3f],extended_id=False)
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
	#os.system("/sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')


