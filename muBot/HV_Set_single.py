import sys
import os
import subprocess
import time

Sk = sys.argv[1]
Volt = sys.argv[2]
Temp = sys.argv[3]

inputF = open('Core/EASI_HV-OUT_bas.txt', 'r')
outputF = open('Conf_HV/EASI_HV-OUT_Vop_' + Sk + '.txt', 'w')
s = inputF.readline()
y = int(Sk)<<10
w = "{:04x}".format(672+y)
outputF.write(w + '\n')
s = inputF.readline()
if (Sk == '0') :
	m = 0.1942
	q = 25.492
	DVop = 0
if (Sk == '1') :
	m = 0.1943
	q = 77.429
	DVop = 0.20
if (Sk == '2') :
	m = 0.1941
	q = 77.519
	DVop = 0.20
if (Sk == '3') :
	m = 0.1931
	q = 77.224
	DVop = 0.20
if (Sk == '4') :
	m = 0.1903
	q = 77.157
	DVop = 0.20
if (Sk == '5') :
	m = 0.1940
	q = 77.423
	DVop = 0.20
if (Sk == '6') :
	m = 0.1933
	q = 77.227
	DVop = 0.20
if (Sk == '7') :
	m = 0.1932
	q = 77.423
	DVop = 0
if (Sk == '8') :
	m = 0.1929
	q = 77.516
	DVop = 0.20
if (Sk == '9') :
	m = 0.1935
	q = 77.229
	DVop = 0
if (Sk == '10') :
	m = 0.0644
	q = 40.531
	DVop = 0
if (Sk == '11') :
	m = 0.0644
	q = 40.491
	DVop = 0
if (Sk == '12') :
	m = 0.0643
	q = 40.458
	DVop = 0
if (Sk == '13') :
	m = 0.0646
	q = 40.459
	DVop = 0
if (Sk == '14') :
	m = 0.0643
	q = 40.42
	DVop = 0
if (Sk == '15') :
	m = 0.0645
	q = 40.554
	DVop = 0

digiVolt = int(((q - (float(Volt) + DVop +(float(Temp)-25)*0.05))//m))	
w = "{:04x}".format(digiVolt)
outputF.write(w + '\n')
while s:
	s = inputF.readline()
	outputF.write(s)
inputF.close()
outputF.close()
