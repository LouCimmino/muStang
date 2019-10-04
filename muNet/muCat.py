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

pedSr = 5
adcSr = 4

inpFile = open('/home/DatiTB/DTC/ENV.txt', 'r+')
s = inpFile.readlines()
RUNflag = s[0].split('\t')
RUNflag[1] = RUNflag[1].replace('\n', '')
inpFile.close()
while (int(RUNflag[1]) != 0):
	inpFile = open('/home/DatiTB/DTC/ENV.txt', 'r+')
	s = inpFile.readlines()
	RUNflag = s[0].split('\t')
	RUNflag[1] = RUNflag[1].replace('\n', '')
	inpFile.close()
	time.sleep(30)

RUNtemp = s[1].split('\t')
RUNtemp[1] = RUNtemp[1].replace('\n', '')
RUNhum = s[2].split('\t')
RUNhum[1] = RUNhum[1].replace('\n', '')
RUNwp = s[4].split('\t')
RUNwp[1] = RUNwp[1].replace('\n', '')

arg = ['./sendDTC', str(pedSr), str(adcSr)]	
subprocess.call(arg)

time.sleep(12)
subprocess.call('./wait2go')	
while True :
	now = datetime.datetime.now()
	TimeS = now.strftime("%Y-%m-%d %H:%M:%S")
	
	ID_start = ID + 5
	
	ID = ID + 1
	flag = 1
	i = 0
	j = 0
	outs = ''
	out_byte = ''
	
	print ('Wait...\n')
	
	inpFile = open('/home/DatiTB/DTC/ENV.txt', 'r+')
	s = inpFile.readlines()
	RUNflag = s[0].split('\t')
	RUNflag[1] = RUNflag[1].replace('\n', '')
	inpFile.close()
	while (int(RUNflag[1]) != 0):
		inpFile = open('/home/DatiTB/DTC/ENV.txt', 'r+')
		s = inpFile.readlines()
		RUNflag = s[0].split('\t')
		RUNflag[1] = RUNflag[1].replace('\n', '')
		inpFile.close()
		time.sleep(30)

	print ('\n\n' + TimeS + ' MURAVES_Rosso@Vesuvio')
	print ('__________________________________________________________\n')
	
	SCstring = ''
	fileSC = dir + 'LOG_run' + str(ID)
	outpFileSC = open(fileSC, 'w')
	
	outpFileSC.write('Current run : ' + str(ID) + '\n')
	outpFileSC.write('Timestamp : ' + str(int(round(time.time()*1000))) + '\n\n')
	outpFileSC.close()

	print ('Current run : ' + str(ID) + '\n')
	print ('__________________________________________________________\n')
	cont = cont + 1

	inpFile = open('/home/DatiTB/DTC/ENV.txt', 'r+')
	s = inpFile.readlines()
	RUNflag = s[0].split('\t')
	RUNflag[1] = RUNflag[1].replace('\n', '')
	inpFile.close()
	while (int(RUNflag[1]) != 0):
		inpFile = open('/home/DatiTB/DTC/ENV.txt', 'r+')
		s = inpFile.readlines()
		RUNflag = s[0].split('\t')
		RUNflag[1] = RUNflag[1].replace('\n', '')
		inpFile.close()
		time.sleep(30)

	arg = ['./sendRuNum', str(ID)]
	subprocess.call(arg)

	inputF = open('/home/DatiTB/DTC/POS_ROSSO', 'r')
	POS = inputF.readline()
	inputF.close()

	SCstring = str(ID-1) + '\t' + str(int(round(time.time()*1000))) + '\t' + POS.replace('\n','') + '\t' + RUNtemp[1] + '\t' + RUNhum[1] + '\t' + RUNwp[1] + '\t'

	inputF = open('/home/DatiTB/DTC/HVtemp_ROSSO', 'r')
	s = inputF.readline()
	SCstring = SCstring + s
	inputF.close()

	inputF = open('/home/DatiTB/DTC/MUXtemp_ROSSO', 'r')
	s = inputF.readline()
	SCstring = SCstring + s
	inputF.close()
	
	outpFileRun = open(runFile, 'w')
	outpFileRun.write('$RUN\t' + str(ID+1))
	outpFileRun.close()

	subprocess.call('./wait2go')

	outpFileSC = open(fileSC, 'a')
	OK = 0
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
		t = t + str(h) +'\t'
		t = t + r[68] + '\t' + r[69]
		outputFsub.write(t)
		outpFileSC.write('\t' + r[0] + '\t' + str(round(h/9060, 2)) + '\n')
		SCstring = SCstring + '\t' + str(round(h/9060, 2))
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

	print('\n--- COMPRESSION STARTED ---')

	arg = ['gzip', '-f', '/home/DatiTB/SLOWCONTROL_run' + str(ID-1), '/home/DatiTB/LOG_run' + str(ID-1), '/home/DatiTB/CONTEGGI_run' + str(ID-1)]
	subprocess.call(arg)

	for i in range (1, pedSr+1):
		arg = ['gzip', '-f', '/home/DatiTB/pedData_evts' + str(pedSr*10000) + '_run' + str(ID-1) + '_sr' + str(i)]
		subprocess.call(arg)

	for i in range (1, adcSr+1):
		arg = ['gzip', '-f', '/home/DatiTB/slaveData_evts' + str(adcSr*10000) + '_run' + str(ID-1) + '_sr' + str(i)]
		subprocess.call(arg)

	inpFile = open('/home/DatiTB/DTC/ENV.txt', 'r+')
	s = inpFile.readlines()
	inpFile.close()
	RUNflag = s[0].split('\t')
	RUNflag[1] = RUNflag[1].replace('\n', '')
	if (int(RUNflag[1]) == 0):
		print('*** Wait to go again ***\n')
		subprocess.call('./wait2go')
	else : print('*** STOP Condition found ***\n')
