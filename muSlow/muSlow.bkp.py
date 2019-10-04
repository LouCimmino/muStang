import os
import sys
import serial
import time
import subprocess
import datetime
import math

outFile = open('/home/DatiTB/DTC/ENV.txt', 'w')
outFile.write('$FLG\t2\n')
outFile.write('$TMP\t0\n')
outFile.write('$RH\t100\n')
outFile.write('$DEW\t0\n')
outFile.write('$WP\t-1\n')
outFile.close()

serArd0 = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd1 = serial.Serial(
	port='/dev/ttyACM1',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd2 = serial.Serial(
	port='/dev/ttyACM2',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd3 = serial.Serial(
	port='/dev/ttyACM3',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd4 = serial.Serial(
	port='/dev/ttyACM4',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd5 = serial.Serial(
	port='/dev/ttyACM5',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd6 = serial.Serial(
	port='/dev/ttyACM6',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd7 = serial.Serial(
	port='/dev/ttyACM7',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)


serArd0.close()
serArd1.close()
serArd2.close()
serArd3.close()
serArd4.close()
serArd5.close()
serArd6.close()
serArd7.close()
serArd0.open()
serArd1.open()
serArd2.open()
serArd3.open()
serArd4.open()
serArd5.open()
serArd6.open()
serArd7.open()

for j in range(12) :
	out_byte = str(serArd0.readline())
for j in range(12) :
	out_byte = str(serArd1.readline())
for j in range(12) :
	out_byte = str(serArd2.readline())
for j in range(12) :
	out_byte = str(serArd3.readline())
for j in range(12) :
	out_byte = str(serArd4.readline())
for j in range(12) :
	out_byte = str(serArd5.readline())
for j in range(12) :
	out_byte = str(serArd6.readline())
for j in range(12) :
	out_byte = str(serArd7.readline())

QUEST = 'STAT?\r'

i = 0
while True:
	inFile = open('/home/DatiTB/DTC/RI.txt', 'r')
	s = inFile.readline()
	a = s.split('\t')
	run = str(a[1].replace('\n', ''))
	inFile.close()

	outFile = open('slowTemp','a')

	now = str(datetime.datetime.now())
	
	serArd0.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd0.readline())
		outs = out_byte.strip("'b")
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd1.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd1.readline())
		outs = out_byte.strip("'b")
		outss = outs.split(' ')
		RHA = float(outss[24])
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd2.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd2.readline())
		outs = out_byte.strip("'b")
		outss = outs.split(' ')
		RHA = RHA + float(outss[24])
		RHB = float(outss[60])
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd3.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd3.readline())
		outs = out_byte.strip("'b")
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd4.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd4.readline())
		outs = out_byte.strip("'b")
		outss = outs.split(' ')
		TB = float(outss[64])
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd5.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd5.readline())
		outs = out_byte.strip("'b")
		outss = outs.split(' ')
		TA = float(outss[28])
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd6.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd6.readline())
		outs = out_byte.strip("'b")
		outss = outs.split(' ')
		TA = TA + float(outss[28])
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd7.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd7.readline())
		outs = out_byte.strip("'b")
		outss = outs.split(' ')
		TA = TA + float(outss[28])
		RHB = RHB + float(outss[60])
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	outFile.close()
	RH = round((RHA+RHB)/4, 2)
	TMP = round((TA+TB)/4, 2)
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
	#WP_set = -1
	WP_set = 20
	FLG = 0 

	#if (TMP>=10 and TMP<=18 and (15-DEW)>2) : WP_set = 15
	#elif (TMP>=5 and TBH<=13 and (10-DEW)>2) : WP_set = 10
	#elif (TMP>=1 and TMP<=9 and (6-DEW)>2) : WP_set = 6
	
	#if (TMP>10 and TMP<18 and (15-DEW)>2 and WP == 15) :
	#	WP_set = 15
	#if (TMP>5 and TMP<13 and (10-DEW)>2 and WP == 10) : 
	#	WP_set = 15
	#if (TMP>1 and TMP<9 and (6-DEW)>2 and WP == 6) :
	#	WP_set = 15

	# END
	outFile = open('/home/DatiTB/DTC/ENV.txt','w')
	if (WP_set!=-1 and WP!=WP_set) :
		outFile.write('$FLG\t1\n')
		FLG = 1
	elif (WP_set == -1) :
		if (WP != WP_set) : 
			# SPEGNIMENTO TEC

			QUESTA = 'CHA 0\r'
			QUESTB = 'CHB 0\r'
			for ii in range(8) :
				print(' --- Accendo TEC : ' + str(ii) + '\n' )
				if (ii == 0) :
					serArd0.write(bytes(QUESTA,'UTF-8'))
					serArd0.write(bytes(QUESTB,'UTF-8'))
				elif (ii == 1) :
					serArd1.write(bytes(QUESTA,'UTF-8'))
					serArd1.write(bytes(QUESTB,'UTF-8'))
				elif (ii == 2) :
					serArd2.write(bytes(QUESTA,'UTF-8'))
					serArd2.write(bytes(QUESTB,'UTF-8'))
				elif (ii == 3) :
					serArd3.write(bytes(QUESTA,'UTF-8'))
					serArd3.write(bytes(QUESTB,'UTF-8'))
				elif (ii == 4) :
					serArd4.write(bytes(QUESTA,'UTF-8'))
					serArd4.write(bytes(QUESTB,'UTF-8'))
				elif (ii == 5) :
					serArd5.write(bytes(QUESTA,'UTF-8'))
					serArd5.write(bytes(QUESTB,'UTF-8'))
				elif (ii == 6) :
					serArd6.write(bytes(QUESTA,'UTF-8'))
					serArd6.write(bytes(QUESTB,'UTF-8'))
				elif (ii == 7) :
					serArd7.write(bytes(QUESTA,'UTF-8'))
					serArd7.write(bytes(QUESTB,'UTF-8'))

			# END
		outFile.write('$FLG\t1\n')
			
	else : outFile.write('$FLG\t0\n')
	outFile.write('$TMP\t' + str(TMP) + '\n')
	outFile.write('$RH\t' + str(RH) + '\n')
	outFile.write('$DEW\t' + str(DEW) + '\n')
	outFile.write('$WP\t' + str(WP_set) + '\n')
	outFile.close()
	
	print('WP2SET : ' + str(WP_set) + '\n') 

	if (WP_set == -1) : FLG = 0	
	if (FLG == 1) : 
		while (FLG == 1) :
			if (WP == -1) :
				# ACCENSIONE TEC

				QUESTA = 'CHA 1\r'
				QUESTB = 'CHB 1\r'
				for ii in range(8) :
					print(' --- Accendo TEC : ' + str(ii) + '\n' )
					if (ii == 0) :
						serArd0.write(bytes(QUESTA,'UTF-8'))
						serArd0.write(bytes(QUESTB,'UTF-8'))
					elif (ii == 1) :
						serArd1.write(bytes(QUESTA,'UTF-8'))
						serArd1.write(bytes(QUESTB,'UTF-8'))
					elif (ii == 2) :
						serArd2.write(bytes(QUESTA,'UTF-8'))
						serArd2.write(bytes(QUESTB,'UTF-8'))
					elif (ii == 3) :
						serArd3.write(bytes(QUESTA,'UTF-8'))
						serArd3.write(bytes(QUESTB,'UTF-8'))
					elif (ii == 4) :
						serArd4.write(bytes(QUESTA,'UTF-8'))
						serArd4.write(bytes(QUESTB,'UTF-8'))
					elif (ii == 5) :
						serArd5.write(bytes(QUESTA,'UTF-8'))
						serArd5.write(bytes(QUESTB,'UTF-8'))
					elif (ii == 6) :
						serArd6.write(bytes(QUESTA,'UTF-8'))
						serArd6.write(bytes(QUESTB,'UTF-8'))
					elif (ii == 7) :
						serArd7.write(bytes(QUESTA,'UTF-8'))
						serArd7.write(bytes(QUESTB,'UTF-8'))
					time.sleep(60)

				# END 
			inpFile = open('/home/DatiTB/DTC/ENV.txt','r')
			s = inpFile.readlines()
			inpFile.close()
			RUNflag = s[0].split('\t')
			RUNflag[1] = RUNflag[1].replace('\n','')
			if (int(RUNflag[1]) == 1) :
				# IMPOSTAZIONE TEMPERATURA

				QUESTC = 'TA ' + str(WP_set) + '\r'
				serArd0.write(bytes(QUESTC,'UTF-8'))
				serArd1.write(bytes(QUESTC,'UTF-8'))
				serArd2.write(bytes(QUESTC,'UTF-8'))
				serArd3.write(bytes(QUESTC,'UTF-8'))
				serArd4.write(bytes(QUESTC,'UTF-8'))
				serArd5.write(bytes(QUESTC,'UTF-8'))
				serArd6.write(bytes(QUESTC,'UTF-8'))
				serArd7.write(bytes(QUESTC,'UTF-8'))

				out_byte = str(serArd0.readline())
				out_byte = str(serArd1.readline())
				out_byte = str(serArd2.readline())
				out_byte = str(serArd3.readline())
				out_byte = str(serArd4.readline())
				out_byte = str(serArd5.readline())
				out_byte = str(serArd6.readline())
				out_byte = str(serArd7.readline())
				
				QUESTC = 'TB ' + str(WP_set) + '\r'
				serArd0.write(bytes(QUESTC,'UTF-8'))
				serArd1.write(bytes(QUESTC,'UTF-8'))
				serArd2.write(bytes(QUESTC,'UTF-8'))
				serArd3.write(bytes(QUESTC,'UTF-8'))
				serArd4.write(bytes(QUESTC,'UTF-8'))
				serArd5.write(bytes(QUESTC,'UTF-8'))
				serArd6.write(bytes(QUESTC,'UTF-8'))
				serArd7.write(bytes(QUESTC,'UTF-8'))

				out_byte = str(serArd0.readline())
				out_byte = str(serArd1.readline())
				out_byte = str(serArd2.readline())
				out_byte = str(serArd3.readline())
				out_byte = str(serArd4.readline())
				out_byte = str(serArd5.readline())
				out_byte = str(serArd6.readline())
				out_byte = str(serArd7.readline())

				# END
				FLG = 0
			else : time.sleep(30)
	else : 
		print('ATTENDO 5 MINUTI!!!\n')
		time.sleep(300)
	i = i+1

