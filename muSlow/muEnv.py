import os
import sys
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import math
import time
import subprocess

while (True) :
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

# PARAMETRI AMBIENTALI DETECTOR ROSSO
	light = 'RED'
	while light == 'RED' :
		outFile = open('/home/DatiTB/DTC/ENV.tmp','w')
		outFile.write('$TMP\t' + str(TMP) + '\n')
		outFile.write('$RH\t' + str(RH) + '\n')
		outFile.write('$DEW\t' + str(DEW) + '\n')
		outFile.close()
		try :
#			arg = ['rm', '/home/DatiTB/DTC/ENV_ROSSO.txt']
#			subprocess.call(arg)
			arg = ['mv', '/home/DatiTB/DTC/ENV.tmp', '/home/DatiTB/DTC/ENV.txt']
			subprocess.call(arg)
			light = 'GREEN'
		except :
			print ('\n +++ RESOURCE ENV BUSY! NEW TRY IN FEW SECONDS +++\n')

	print ('\n *** 2 MIN TO THE NEXT MEASURE ***\n')
	time.sleep(120)
