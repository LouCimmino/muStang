import sys
import os
import subprocess
import time

skList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
Volt = sys.argv[1]
Temp = sys.argv[2]

Vapp = ''

for Sk in skList :
	inputF = open('Core/EASI_HV-OUT_bas.txt', 'r')
	outputF = open('Conf_HV/EASI_HV-OUT_Vbias_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(672+y)
	outputF.write(w + '\n')
	s = inputF.readline()
	if (Sk == '0') :
		m = 0.0644
		q = 40.533
		DVop = -0.2
	if (Sk == '1') :
		m = 0.0644
		q = 40.541
		DVop = -0.25
	if (Sk == '2') :
		m = 0.0644
		q = 40.445
		DVop = -0.35
	if (Sk == '3') :
		m = 0.0644
		q = 40.529
		DVop = -0.15
	if (Sk == '4') :
		m = 0.0641
		q = 40.411
		DVop = -0.35
	if (Sk == '5') :
		m = 0.0644
		q = 40.545
		DVop = 0.0
	if (Sk == '6') :
		m = 0.0645
		q = 40.515
		DVop = 1.7
	if (Sk == '7') :
		m = 0.0644
		q = 40.515
		DVop = 0.35
	if (Sk == '8') :
		m = 0.0645
		q = 40.616
		DVop = -0.1
	if (Sk == '9') :
		m = 0.0644
		q = 40.495
		DVop = -0.25
	if (Sk == '10') :		
		m = 0.0644
		q = 40.531
		DVop = -0.1
	if (Sk == '11') :
		m = 0.0644
		q = 40.491
		DVop = -0.2
	if (Sk == '12') :
		m = 0.0643
		q = 40.458
		DVop = 0.8
	if (Sk == '13') :
		m = 0.0646
		q = 40.594
		DVop = 0.05
	if (Sk == '14') :
		m = 0.0643
		q = 40.42
		DVop = 0.05
	if (Sk == '15') :
		m = 0.0645
		q = 40.554
		DVop = 0.15
	
	#digiVolt = int(((q - float(Volt))//m)+(float(Temp)-25)*0.05)
	#digiVolt = int(((q - (float(Volt) + DVop +(float(Temp)-21)*0.05))//m))	
	digiVolt = int(((q - (float(Volt) + DVop +(float(Temp)-21)*0.04))//m))	
	Vapp = Vapp + str(round(float(Volt) + DVop +(float(Temp)-21)*0.04, 2)) + '\t'

	w = "{:04x}".format(digiVolt)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()
	print('--- HV SK ' + Sk + ' SET! ---')

inputF = open('/home/DatiTB/DTC/HVtemp_ROSSO', 'w')
inputF.write(Vapp)
inputF.close()
print('\n')
