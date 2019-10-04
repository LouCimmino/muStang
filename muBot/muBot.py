import sys
import os
import subprocess

print ('\n\nMuDog (MuBot ver 5.0) - MURAVES Experiment')
print ('Copyright 2019(C) 19LC77 (email : luigi.cimmino@na.infn.it)')
print ('__________________________________________________________\n')

if sys.argv[1] == 'ROSSO' :
	muClient = 'tcp://192.168.77.32:5000'
	broadPort = 'tcp://0.0.0.0:5000'
elif sys.argv[1] == 'NERO' :
	muClient = 'tcp://192.168.77.82:6000'
	broadPort = 'tcp://0.0.0.0:6000'
elif sys.argv[1] == 'BLU' :
	muClient = 'tcp://192.168.77.136:7000'
	broadPort = 'tcp://0.0.0.0:7000'

arg = ['./DTCrcvr', broadPort, sys.argv[1]]
subprocess.call(arg)

DTCfile = '/home/DatiTB/DTC/DTC_' + sys.argv[1] + '.txt'
inputF = open(DTCfile, 'r')
s = inputF.readline()
s = s.replace('$PEDS\t', '')
peds = s.replace('\n', '')
s = inputF.readline()
s = s.replace('$EVTS\t', '')
evts = s.replace('\n', '')
inputF.close()
try :
	arg = ['python3', 'acqCPE.py', peds, evts, sys.argv[1]]
	subprocess.call(arg)
except :
	arg = ['python3', 'HV_Shutdown.py']
	subprocess.call(arg)
	print(' *** EXIT ***')
