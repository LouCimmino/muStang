import sys
import os
import time
import serial
import subprocess
import datetime
import binascii
from math import log
from time import strptime, strftime
import threading
#import psutil


print ('\n\nMuDog (MuBot ver 4.0) - MuRay Experiment')
print ('Copyright 2013(C) 19LC77 (email : luigi.cimmino@na.infn.it)')
print ('__________________________________________________________\n')

print ("* LOADING SYSTEM")

out_a = [b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00']
cont_a = 0

flag = 1

V_ref = 13.90 #Volt
R_ch_mean = 6.80 #kOhm

T_ext = '0.00' 
H_ext = '0.00'
Hp = '0.00'

T_mean_st = 20
T_mean_new = 20
V35 = 38.500
V18 = 14.500

cont = 0
inp=''
out=''

serc = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=9600,
	parity='N',
	stopbits=1,
	bytesize=8
	)
serJ = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=38400,
	parity='E',
	stopbits=1,
	bytesize=7,
    	xonxoff=1
)	
serArdDx = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=9600,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArdSx = serial.Serial(
	port='/dev/ttyACM1',
	baudrate=9600,
	parity='N',
	stopbits=1,
	bytesize=8
)

serJ.close()
serArdSx.close()
serArdDx.close()
serc.close()

serArdSx.open()
serArdDx.open()
#serJ.open()
time.sleep(2)

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

murayPID = 0

dir = '/home/DatiTB/'
runFile = dir + 'DTC/RI.txt'

try:
	inpFileRun = open(runFile, 'r')
	s = inpFileRun.readline()
	s = s.replace('$RUN\t', '')
	run = s.replace('\n', '')
	ID = int(run) - 1

except:
	ID = 0

#def WatchDog():
#	SleepNowInTheFire = 1800
#	count = 0
#	print ('---> WatchDog activated!\n')
#	while 1:
#		now_WD = datetime.datetime.now()
#		lastfile = max(os.listdir('/home/DatiTB/'), key=os.path.getmtime)
#		lastfile_ts = modification_date('/home/DatiTB/' + lastfile)
#		if (count != 0) and ((now_WD - lastfile_ts).total_seconds() > SleepNowInTheFire) :
#			murayProc = filter(lambda p: p.name == "MURAY", psutil.process_iter())
#			for muDog in murayProc:
#				print ('----- PID to kill : ' + str(muDog.pid) + ' -----')
#				args_WD = ['kill', '-9', str(muDog.pid)]
#				subprocess.call(args_WD)
#			print ('__________________________________________________________')
#			print ("---> WatchDog kills...\n* Rebooting Master...\n")
#			args_WD = ['python3', '/home/muNet/ResetMaster.py']
#			subprocess.call(args_WD)
#			print ("---> MasterPi Rebooted!")
#			print ('__________________________________________________________\n')
#		time.sleep(SleepNowInTheFire/3)
#		count = count + 1
		
#try:
#	threading.Thread(target = WatchDog).start()
#except:
#	print ("*** Error: unable to start WatchDog!")

arg = ['./sendDTC', '10', '10']	
subprocess.call(arg)
time.sleep(12)
subprocess.call('./wait2go')	
while True :
	now = datetime.datetime.now()
	TimeS = now.strftime("%Y-%m-%d %H:%M:%S")
	
	ID_start = ID + 5
	
	flag = 1
	i = 0
	j = 0
	outs = ''
	out_byte = ''
	
	print ('Wait...\n')
	while (flag == 1) :
		OK = 0
		if i >= 25 : 
			flag = 0
			ID = ID + 1
			break
			
		if (i < 5): 
			out_dx = [0,0,0,0,0,0,0,0,0,0,0,0]
			out_sx = [0,0,0,0,0,0,0,0,0,0,0,0]
		if (i == 24):
			T_ch00 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[0]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch01 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[1]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch02 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[2]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch03 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[3]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch04 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[4]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch05 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[5]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch06 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[6]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch07 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[7]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch08 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[8]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch09 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[9]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch10 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[10]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch11 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_dx[11]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch12 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[0]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch13 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[1]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch14 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[2]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch15 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[3]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch16 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[4]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch17 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[5]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch18 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[6]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch19 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[7]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch20 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[8]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch21 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[9]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch22 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[10]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
			T_ch23 = round(3383.81-865.8*(15.274+0.00231*(1000-(R_ch_mean/(V_ref/(round(out_sx[11]/(i-4),0)*3.3/4095)-1))*1000))**0.5, 1)
		
		try :

			serArdDx.write(bytes('S', 'UTF-8'))
			for j in range(12) :
				out_byte = str(serArdDx.readline())
				outs = out_byte.strip("'b")
				outs = outs[0:-4]
				out_dx[j] = out_dx[j] + int(outs)
						
			j = 0
			serArdSx.write(bytes('S', 'UTF-8'))
			for j in range(12):
				out_byte = str(serArdSx.readline())
				outs = out_byte.strip("'b")
				outs = outs[0:-4]
				out_sx[j] = out_sx[j] + int(outs)
		except :
			print('Skipping one row...')
			OK = 1
		if (OK == 0) : 
			i = i + 1
		j = 0
		outs=''
				
	print ('\n__________________________________________________________\n')
	
	print ('Measure ',ID,':')
	print ('\t T_ch00 :\t' + str(T_ch00) + "'C")
	print ('\t T_ch01 :\t' + str(T_ch01) + "'C")
	print ('\t T_ch02 :\t' + str(T_ch02) + "'C")
	print ('\t T_ch03 :\t' + str(T_ch03) + "'C")
	print ('\t T_ch04 :\t' + str(T_ch04) + "'C")
	print ('\t T_ch05 :\t' + str(T_ch05) + "'C")
	print ('\t T_ch06 :\t' + str(T_ch06) + "'C")
	print ('\t T_ch07 :\t' + str(T_ch07) + "'C")
	print ('\t T_ch08 :\t' + str(T_ch08) + "'C")
	print ('\t T_ch09 :\t' + str(T_ch09) + "'C")
	print ('\t T_ch10 :\t' + str(T_ch10) + "'C")
	print ('\t T_ch11 :\t' + str(T_ch11) + "'C")
	print ('\t T_ch12 :\t' + str(T_ch12) + "'C")
	print ('\t T_ch13 :\t' + str(T_ch13) + "'C")
	print ('\t T_ch14 :\t' + str(T_ch14) + "'C")
	print ('\t T_ch15 :\t' + str(T_ch15) + "'C")
	print ('\t T_ch16 :\t' + str(T_ch16) + "'C")
	print ('\t T_ch17 :\t' + str(T_ch17) + "'C")
	print ('\t T_ch18 :\t' + str(T_ch18) + "'C")
	print ('\t T_ch19 :\t' + str(T_ch19) + "'C")
	print ('\t T_ch20 :\t' + str(T_ch20) + "'C")
	print ('\t T_ch21 :\t' + str(T_ch21) + "'C")
	print ('\t T_ch22 :\t' + str(T_ch22) + "'C")
	print ('\t T_ch23 :\t' + str(T_ch23) + "'C")	
	

	print ('\n\n' + TimeS + ' @TunnelBorbonico')
	print ('__________________________________________________________\n')
	
	serc.close()
	serc.open()
	serc.isOpen()
	#serJ.open()


	time.sleep(1)
	cont_a = 1

	
	termrs_flag = 1
	while (serc.inWaiting() > 0):
		out_a[0] = serc.read() 
		if out_a[0] == b'\x02':
			while (serc.inWaiting() > 0 and cont_a < 7):
				out_a[cont_a] = serc.read()
				cont_a = cont_a + 1
		T_ext = str(round((int(bytes.decode(binascii.hexlify(out_a[4])), 16)*256 + int(bytes.decode(binascii.hexlify(out_a[5])), 16))/100 - 50, 2))
		H_ext = str(round((int(bytes.decode(binascii.hexlify(out_a[2])), 16)*256 + int(bytes.decode(binascii.hexlify(out_a[3])), 16))/100 + 0.2, 2))
		a = 17.271
		b = 237.7
		Hp = str(round(b * ((a * float(T_ext))/(b + float(T_ext)) + log(float(H_ext)/100))/(a - ((a * float(T_ext))/(b + float(T_ext)) + log(float(H_ext)/100))), 2))
		if out_a[0] == b'\x02' and out_a[6] == b'\x03' :
			break
	
	print ('Room temperature : \t\t' + T_ext + "'C")
	
	#msg_j = 'in_pv_00'

	#for i in range (len(msg_j)) :
	#	serJ.write(str.encode(msg_j[i]))
	#serJ.write(str.encode(chr(0x0D)))

	#time.sleep(1)	
	#while serJ.inWaiting() > 0 :
	#	out_byte = serJ.read()
	#	if (bytes.decode(out_byte) != '\n' and bytes.decode(out_byte) != '\r') : out += bytes.decode(out_byte)
	#if (out  != '') :
	#	T_bath = out
	#	print ('Bath temperature : \t\t' + T_bath + "'C")
	#	out=''
	#else : 
	#	T_bath = '0.00'
	
	#msg_j = 'in_pv_01'

	#for i in range (len(msg_j)) :
	#	serJ.write(str.encode(msg_j[i]))
	#serJ.write(str.encode(chr(0x0D)))

	#time.sleep(1)
	#while serJ.inWaiting() > 0 :
	#	out_byte = serJ.read()
	#	if (bytes.decode(out_byte) != '\n' and bytes.decode(out_byte) != '\r') : out += bytes.decode(out_byte)
	#if (out  != '') :
	#	P_bath = out
	#	print ('[ ' + P_bath + '% of total power used by chiller ]')
	#	out=''
	#else :
	#	P_bath = '0'
	#	print ("*** WARNING : Julabo is not responding!\n")
	
	print ('Relative humidity : \t\t' + H_ext + '%')
	print ('Dew Point : \t\t\t' + Hp + "'C\n")
	serc.close()
	#serJ.close()
		
	#sql = "INSERT INTO Temperature (id, T_bath, P_bath, T_ext, H_ext, Hp, T_Ch01, T_Ch02, T_Ch03, T_Ch04, T_Ch05, T_Ch06, T_Ch07, T_Ch08, T_Ch09, T_Ch10, T_Ch11, T_Ch12, T_Ch13, T_Ch14, T_Ch15, T_Ch16, T_Ch17, T_Ch18, T_Ch19, T_Ch20, T_Ch21, T_Ch22, T_Ch23, T_Ch24, TimeS) VALUES (" + str(ID) + " , " + T_bath + ", " + P_bath + ", " + T_ext + ", " + H_ext + ", " + Hp + ", " + str(T_ch00) + ", " + str(T_ch01) + ", " + str(T_ch02) + ", " + str(T_ch03) + ", " + str(T_ch04) + ", " + str(T_ch05) + ", " + str(T_ch06) + ", " + str(T_ch07) + ", " + str(T_ch08) + ", " + str(T_ch09) + ", " + str(T_ch10) + ", " + str(T_ch11) + ", " + str(T_ch12) + ", " + str(T_ch13) + ", " + str(T_ch14) + ", " + str(T_ch15) + ", " + str(T_ch16) + ", " + str(T_ch17) + ", " + str(T_ch18) + ", " + str(T_ch19) + ", " + str(T_ch20) + ", " + str(T_ch21) + ", " + str(T_ch22) + ", " + str(T_ch23) + ", '" + TimeS + "')" 
	SCstring = ''
	fileSC = dir + 'LOG_run' + str(ID)
	outpFileSC = open(fileSC, 'w')
	
	outpFileSC.write('Current run : ' + str(ID) + '\n')
	outpFileSC.write('Timestamp : ' + str(int(round(time.time()*1000))) + '\n\n')
	outpFileSC.write('Hybrid Temp :\n')
	outpFileSC.write('\t T_ch00 :\t' + str(T_ch00) + "'C" + "\n")
	outpFileSC.write('\t T_ch01 :\t' + str(T_ch01) + "'C" + "\n")
	outpFileSC.write('\t T_ch02 :\t' + str(T_ch02) + "'C" + "\n")
	outpFileSC.write('\t T_ch03 :\t' + str(T_ch03) + "'C" + "\n")
	outpFileSC.write('\t T_ch04 :\t' + str(T_ch04) + "'C" + "\n")
	outpFileSC.write('\t T_ch05 :\t' + str(T_ch05) + "'C" + "\n")
	outpFileSC.write('\t T_ch06 :\t' + str(T_ch06) + "'C" + "\n")
	outpFileSC.write('\t T_ch07 :\t' + str(T_ch07) + "'C" + "\n")
	outpFileSC.write('\t T_ch08 :\t' + str(T_ch08) + "'C" + "\n")
	outpFileSC.write('\t T_ch09 :\t' + str(T_ch09) + "'C" + "\n")
	outpFileSC.write('\t T_ch10 :\t' + str(T_ch10) + "'C" + "\n")
	outpFileSC.write('\t T_ch11 :\t' + str(T_ch11) + "'C" + "\n")
	outpFileSC.write('\t T_ch12 :\t' + str(T_ch12) + "'C" + "\n")
	outpFileSC.write('\t T_ch13 :\t' + str(T_ch13) + "'C" + "\n")
	outpFileSC.write('\t T_ch14 :\t' + str(T_ch14) + "'C" + "\n")
	outpFileSC.write('\t T_ch15 :\t' + str(T_ch15) + "'C" + "\n")
	outpFileSC.write('\t T_ch16 :\t' + str(T_ch16) + "'C" + "\n")
	outpFileSC.write('\t T_ch17 :\t' + str(T_ch17) + "'C" + "\n")
	outpFileSC.write('\t T_ch18 :\t' + str(T_ch18) + "'C" + "\n")
	outpFileSC.write('\t T_ch19 :\t' + str(T_ch19) + "'C" + "\n")
	outpFileSC.write('\t T_ch20 :\t' + str(T_ch20) + "'C" + "\n")
	outpFileSC.write('\t T_ch21 :\t' + str(T_ch21) + "'C" + "\n")
	outpFileSC.write('\t T_ch22 :\t' + str(T_ch22) + "'C" + "\n")
	outpFileSC.write('\t T_ch23 :\t' + str(T_ch23) + "'C" + "\n\n")	

	outpFileSC.write('Room temperature : \t\t' + T_ext + "'C\n")
	#outpFileSC.write('Bath temperature : \t\t' + T_bath + "'C\n")
	#outpFileSC.write('[ ' + P_bath + '% of total power used by chiller ]\n')
	outpFileSC.write('Relative humidity : \t\t' + H_ext + '%\n')
	outpFileSC.write('Dew Point : \t\t\t' + Hp + "'C\n\n")
	
	#SCstring = str(ID-1) + '\t' + str(int(round(time.time()*1000))) + '\t' + str(T_ch00) + '\t' + str(T_ch01) + '\t' + str(T_ch02) + '\t' + str(T_ch03) + '\t' + str(T_ch04) + '\t' + str(T_ch05) + '\t' + str(T_ch06) + '\t' + str(T_ch07) + '\t' + str(T_ch08) + '\t' + str(T_ch09) + '\t' + str(T_ch10) + '\t' + str(T_ch11) + '\t' + str(T_ch12) + '\t' + str(T_ch13) + '\t' + str(T_ch14) + '\t' + str(T_ch15) + '\t' + str(T_ch16) + '\t' + str(T_ch17) + '\t' + str(T_ch18) + '\t' + str(T_ch19) + '\t' + str(T_ch20) + '\t' + str(T_ch21) + '\t' + str(T_ch22) + '\t' + str(T_ch23) + '\t' + T_ext + '\t' + T_bath + '\t' + P_bath + '\t' + H_ext + '\t' +  Hp + '\t'
	SCstring = str(ID) + '\t' + str(int(round(time.time()*1000))) + '\t' + str(T_ch00) + '\t' + str(T_ch01) + '\t' + str(T_ch02) + '\t' + str(T_ch03) + '\t' + str(T_ch04) + '\t' + str(T_ch05) + '\t' + str(T_ch06) + '\t' + str(T_ch07) + '\t' + str(T_ch08) + '\t' + str(T_ch09) + '\t' + str(T_ch10) + '\t' + str(T_ch11) + '\t' + str(T_ch12) + '\t' + str(T_ch13) + '\t' + str(T_ch14) + '\t' + str(T_ch15) + '\t' + str(T_ch16) + '\t' + str(T_ch17) + '\t' + str(T_ch18) + '\t' + str(T_ch19) + '\t' + str(T_ch20) + '\t' + str(T_ch21) + '\t' + str(T_ch22) + '\t' + str(T_ch23) + '\t' + T_ext + '\t' + H_ext + '\t' +  Hp + '\t'
	outpFileSC.close()

	print ('Current run : ' + str(ID) + '\n')
	print ('__________________________________________________________\n')
	cont = cont + 1
	arg = ['./sendRunNum', str(ID)]
	subprocess.call(arg)

	outpFileRun = open(runFile, 'w')
	outpFileRun.write('$RUN\t' + str(ID+1))
	outpFileRun.close()

	subprocess.call('./wait2go')

	outpFileSC = open(fileSC, 'a')

	fileAcc = (dir + 'cTrigger_Counts')
	arg = ['touch', fileAcc]
	subprocess.call(arg)
	while (OK == 0):
		try:
			inpFileAcc = open(fileAcc, 'r')
			OK = 1
		except:
			print('!!! Trigger File not Found !!!')

	acc = inpFileAcc.readlines()
	acc[0].replace('\n', '')
	acc[1].replace('\n', '')
	tr = round(int('0x'+acc[0], 16)/60, 3)
	ar = round(int('0x'+acc[1], 16)/60, 3)
	inpFileAcc.close()

	outpFileSC.write('Trigger rate : ' + str(tr) + '\n')
	outpFileSC.write('Accidental rate : ' + str(ar) + '\n\n')
	
	SCstring = SCstring + str(tr) + '\t' + str(ar)
	mod = "CONTEGGI"
	outputFsub = open(dir + mod + '_run' + str(ID), 'a')
	fileinp = dir + "SlavesCount_run" + str(ID)
	arg = ['touch', fileinp]
	subprocess.call(arg)
	OK = 0
	while (OK == 0):
		try:
			inputF = open(fileinp, 'r')
			OK = 1
		except:
			print('!!! Counts File not Found !!!')

	outpFileSC.write('OR32 Counts :\n')

	s = inputF.readline()
	while s:
		s = s.replace('\t2', '\t')
		r = s.split('\t')
		t = r[0] + '\t'
		for i in range(4,68,2):
			h = int('0x'+r[i]+r[i+1], 16)
			t = t + str(h) +'\t'
		h = int('0x'+r[1]+r[2]+r[3], 16)
		t = t + str(h) +'\t66.4\t'
		t = t + r[68] + '\t10\t' + r[69]
		outputFsub.write(t)
		outpFileSC.write('\t' + r[0] + '\t' + str(round(h/10000, 2)) + '\n')
		SCstring = SCstring + '\t' + str(round(h/10000, 2))
		s = inputF.readline()
	outputFsub.close()
	inputF.close()
	outpFileSC.close()
	
	fileSC = dir + 'SLOWCONTROL_run' + str(ID)
	outpFileSC = open(fileSC, 'w')
	outpFileSC.write(SCstring)
	outpFileSC.close()

	arg = ['rm', dir + "SlavesCount_run" + str(ID)]
	subprocess.call(arg)

	arg = ['rm', dir + "cTrigger_Counts"]
	subprocess.call(arg)
	
	subprocess.call('./wait2go')
