import os
import sys
import RPi.GPIO as GPIO
import Adafruit_DHT as dht

while (True) 
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
	
	WP_sup = s[4].split('\t')
	WP_sup[1] = WP_sup[1].replace('\n', '')
	WP = int(WP_sup[1])
	WP_set = -1

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
	
	outFile = open('/home/DatiTB/DTC/ENV.txt','w')
	if (WP_set!=-1) :
		outFile.write('$FLG\t1\n')
	
	else : outFile.write('$FLG\t0\n')
	outFile.write('$TMP\t' + str(TMP) + '\n')
	outFile.write('$RH\t' + str(RH) + '\n')
	outFile.write('$DEW\t' + str(DEW) + '\n')
	outFile.write('$WP\t' + str(WP_set) + '\n')
	outFile.close()
		
	TMP_MEM = TMP
	RH_MEM = RH
	
	print ('\n--- 5 MIN TO THE NEXT MEASURE ---\n')
	time.sleep(300)