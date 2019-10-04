import sys
import os
import subprocess
import time

skList = [sys.argv[1],sys.argv[2]]

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
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

	inputF = open('Core/ReadCount.txt', 'r')
	outputF = open('Conf/ReadCount_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(648 + y)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

	inputF = open('Core/ReadSlave.txt', 'r')
	outputF = open('Conf/ReadSlave_' + Sk + '.txt', 'w')
	s = inputF.readline()
	y = int(Sk)<<10
	w = "{:04x}".format(192+y)
	outputF.write(w + '\n')
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()
	
subprocess.call("./Reset")

for dac10 in range (750,749,-10):
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

		for Sk in skList :
			arg = ["./ResetSlave", Sk]
			subprocess.call(arg)

		subprocess.call("./Init")

			
		for Sk in skList :
			inputF = open('Core/EASI_Slow_Control.txt', 'r')
			outputF = open('Conf/EASI_Slow_Control_' + Sk + '.txt', 'w')
			s = inputF.readline()
			y = int(Sk)<<10
			w = "{:04x}".format(224 + y)
			outputF.write(w + '\n')
			while s:
				s = inputF.readline()
				outputF.write(s)
			inputF.close()
			outputF.close()


		for Sk in skList :
			time.sleep(1)
			arg = ["./SendFSlaves", "Conf/EASI_Probe_" + Sk + ".txt"]
			subprocess.call(arg)
			arg = ["./SendFSlaves", "Conf/EASI_Hold_Pot_46ns_" + Sk + ".txt"]
			subprocess.call(arg)
			arg = ["./SendFSlaves", "Conf/EASI_TimeOut_Pot_300ns_" + Sk + ".txt"]
			subprocess.call(arg)
			arg = ["./SendFSlaves", "Conf/EASI_Slow_Control_" + Sk + ".txt"]
			subprocess.call(arg)

			if (dac8 == 255):
				argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
				subprocess.call(argv)
				argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_ON_" + Sk + ".txt"]
				subprocess.call(argv)
				argv = ["./SendHV", "Conf_HV/EASI_HV-OUT_Vop_" + Sk + ".txt"]
				subprocess.call(argv)
			print('\n')

		
		print ('\nConfiguring Triggers...')

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

		#subprocess.call('./Reset')

		#print ('\nAquiring Trigger Rates and Counts...')

		#arg = ['./ReadMaster_cTrigger', '60', 'MasterCMD/START_TRG_CNT_60.txt', 'MasterCMD/RD_TRG_CNT.txt']
		#subprocess.call(arg)

		print ('\nAquiring Counts...')
		while (1):
		
			subprocess.call('./Reset')

			for Sk in skList :
				arg = ["./SendFSlaves", "Conf/ReadCount_" + Sk + ".txt"]
				subprocess.call(arg)
			time.sleep(12)
			for Sk in skList :
				arg = ["./SendFSlaves", "Conf/ReadSlave_" + Sk + ".txt"]
				subprocess.call(arg)
				subprocess.call("./ReadMaster_count")
				inp = open('/home/DatiTB/SlaveCounts', 'r')
				outp = open('Counts_LAB', 'a')

				r = inp.readline()
				r = r.replace('\n', '')
				while r :
					w = Sk + '\t' + r + str(dac10) + '\t' + str(int(time.time())) + '\n'
					outp.write(w)
					r = inp.readline()
				inp.close()
				outp.close()
				arg = ['rm', '/home/DatiTB/SlaveCounts']
				subprocess.call(arg)
				print ('END\n')
			#subprocess.call("./Reset")

		dac8 = dac8 - 64
		if (dac8 == -1):
			dac8 = 0
		
	print ('\n--- Shutting Down System\n')
	for Sk in skList :
		argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_Vop_" + Sk + ".txt"]
		subprocess.call(argv)
		argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
		subprocess.call(argv)
		argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_OFF_" + Sk + ".txt"]
		subprocess.call(argv)
