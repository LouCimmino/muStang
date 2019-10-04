import sys
import os
import subprocess
import time

skList = ['6', '7']
dac10List = ['730','774']


for Sk in skList :
	inputF = open('Core/EASI_Probe.txt', 'r')
	outputF = open('Conf/EASI_Probe_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(256+y)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

	inputF = open('Core/EASI_Hold_Pot_46ns.txt', 'r')
	outputF = open('Conf/EASI_Hold_Pot_46ns_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(736+y)
	outputF.write(w + '\n')
	s = inputF.readline()
	y = 25 #25
	ht = "{:04x}".format(255-y)
	outputF.write(ht + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

	inputF = open('Core/EASI_TimeOut_Pot_300ns.txt', 'r')
	outputF = open('Conf/EASI_TimeOut_Pot_300ns_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(704+y)
	outputF.write(w + '\n')
	s = inputF.readline()
	y = 16 #16
	to = "{:04x}".format(255-y)
	outputF.write(to + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

subprocess.call("./Reset")

for dac10 in range (0,1,1):
	dac8 = 255
		
	while (dac8 >= 255):
		print ('----------------------------')
		print ('DAC8 value  : ' + str(dac8))
		print ('DAC10 value : ' + str(dac10))
		print ('----------------------------')
		inputF = open('EASIprog.c', 'r')
		outputF = open('EASIprog.out', 'w')
		s = inputF.readline()
		while s:
			outputF.write(s)
			#if ('//DAC8' in s):
			#	outputF.write('for (i=0; i<32; i++) error = DACbiasSC_EASI(SC_EASI, i, ' + str(dac8) + ');')
			#	outputF.write('\n')	
			#	s = inputF.readline()
			if ('//DAC10' in s) :
				outputF.write('\tDAC10thrsSC_EASI(SC_EASI,' + str(dac10) +');\n')
				s = inputF.readline()
			s = inputF.readline()
		inputF.close()
		outputF.close()
		arg = ["mv", "EASIprog.out", "EASIprog.c"]
		subprocess.call(arg)
		arg = ["gcc", "-O2", "EASIprog.c", "libreriaSC_EASI.c", "-o", "EASIprog"]
		subprocess.call(arg)
		subprocess.call("./EASIprog")

		subprocess.call('./Init')

		for Sk in skList :
			arg = ["./ResetSlave", Sk]
			subprocess.call(arg)
	
		skCounter = 0
		for Sk in skList :
			inputF = open('Core/EASI_Slow_Control.txt', 'r')
			outputF = open('Conf/EASI_Slow_Control_' + Sk + '.txt', 'w')
			s = inputF.readline()
			y = int(Sk)<<10
			w = "{:04x}".format(224 + y)
			outputF.write(w + '\n')
			s = inputF.readline()
			outputF.write(s)
			s = inputF.readline()
			y = int(dac10List[skCounter])<<2
			w = "{:04x}".format(61443 + y)
			outputF.write(w + '\n')
			
			while s:
				s = inputF.readline()
				outputF.write(s)
			inputF.close()
			outputF.close()
			skCounter = skCounter + 1
		
		for Sk in skList :
			subprocess.call('./Init')
			arg = ["./SendFSlaves", "Conf/EASI_Probe_" + Sk + ".txt"]
			subprocess.call(arg)
			arg = ["./SendFSlaves", "Conf/EASI_Hold_Pot_46ns_" + Sk + ".txt"]
			subprocess.call(arg)
			arg = ["./SendFSlaves", "Conf/EASI_TimeOut_Pot_300ns_" + Sk + ".txt"]
			subprocess.call(arg)
			arg = ["./SendFSlaves", "Conf/EASI_Slow_Control_" + Sk + ".txt"]
			subprocess.call(arg)

			#if (dac8 == 255):
			#	argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
			#	subprocess.call(argv)
			#	argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_ON_" + Sk + ".txt"]
			#	subprocess.call(argv)
			#	argv = ["./SendHV", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
			#	subprocess.call(argv)
			print('\n')

		print ('\nAquiring Triggers...')
		
		arg = ["./SendFMaster", "MasterCMD/EN_MUX0_S.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX1_S.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX2_S.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX3_S.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX4_S.txt"]
		subprocess.call(arg)
		
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL0.txt"]
		#subprocess.call(arg)
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL1.txt"]
		#subprocess.call(arg)
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL2.txt"]
		#subprocess.call(arg)
		#arg = ["./SendFMaster", "MasterCMD/EN_DEL3.txt"]
		#subprocess.call(arg)


		subprocess.call('./Reset')

		runCounter = 0
		evts = 1000
		
		#arg = ["./SendFSlaves", "/home/muBot/Sk17Ch00"]
		#subprocess.call(arg)

		#input("Press to Go...")
		while(runCounter<1):
			runCounter = runCounter + 1
			print("Run " + str(runCounter) + " :: Now reading")
			outputF = open('/home/DatiTB/slaveData', 'w')
			outputF.write(str(int(round(time.time()*1000))) + '\n')
			outputF.close()
			arg = ['./ReadSlave', str(evts) , skList[0], skList[1]] #, skList[2], skList[3], skList[4], skList[5], skList[6], skList[7], skList[8], skList[9], skList[10], skList[11]]
			subprocess.call(arg)
			outputF = open('/home/DatiTB/slaveData', 'a')
			outputF.write(str(int(round(time.time()*1000))))
			outputF.close()
			#arg = ['mv', '/home/DatiTB/slaveData', '/home/muray/CosmicRun/slaveData_evts' + str(evts) + '_run' + str(runCounter)]
			#arg = ['mv', '/home/muBot/slaveData', '/home/muray/CosmicRun/pedData_evts' + str(evts) + '_run' + str(runCounter) + '_Sk05']
			#subprocess.call(arg)

		dac8 = dac8 - 64
		if (dac8 == -1):
			dac8 = 0

	print ('\n--- Shutting Down System\n')
	#for Sk in skList :
		#argv = ["./SendHV_rDown", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
		#subprocess.call(argv)
		#argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
		#subprocess.call(argv)
		#argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_OFF_" + Sk + ".txt"]
		#subprocess.call(argv)
