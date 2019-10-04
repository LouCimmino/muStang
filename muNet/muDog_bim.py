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

arg = ['./sendDTC', '1', '1']	
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
	
	print ('\n__________________________________________________________\n')
	
	print ('\n\n' + TimeS + ' @DeadpoolLab')
	print ('__________________________________________________________\n')
	

	time.sleep(1)
	cont_a = 1

	
	termrs_flag = 1
	
	msg_j = 'in_pv_00'

	msg_j = 'in_pv_01'
		
	SCstring = ''
	fileSC = dir + 'LOG_run' + str(ID)

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
	inpFileAcc = open(fileAcc, 'r')
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
	inputF = open(fileinp, 'r')

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
