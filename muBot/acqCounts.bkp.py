import sys
import os
import subprocess
import time

skList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
#skList = ['5']

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

for dac10 in range (700,299,-5):
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

		inputF = open('Conf/EASI_Slow_Control_5.txt', 'r')
		s = inputF.readlines()
		inputF.close()
		s[11] = '7b05\n'
		s[12] = 'a0c8\n'
		s[13] = 'ed31\n'
		#s[14] = '98cc\n'
		#s[15] = '8e5b\n'
		s[14] = '98c8\n'
		s[15] = '065b\n'
		s[16] = '2391\n'
		s[17] = 'c8e4\n'
		s[18] = '7699\n'
		s[19] = '1cb6\n'
		s[20] = '4723\n'
		s[21] = '8cc8\n'
		s[22] = 'e332\n'
		s[23] = '391c\n'
		s[24] = '8e47\n'
		s[25] = '2391\n'
		s[26] = 'c8e8\n'
		#s[27] = '3239\n'
		s[27] = '2019\n'
		s[28] = '1c8e\n'
		s[29] = '4700\n'
		outputF = open('Conf/EASI_Slow_Control_5.txt', 'w')
		for line in s:
			outputF.write(line)
		outputF.close()

		inputF = open('Conf/EASI_Slow_Control_6.txt', 'r')
		s = inputF.readlines()
		inputF.close()
		s[11] = '7aab\n'
		s[12] = '5fad\n'
		s[13] = '56aa\n'
		s[14] = 'b5aa\n'
		s[15] = 'd56a\n'
		s[16] = 'b55a\n'
		s[17] = 'ad56\n'
		s[18] = 'aab5\n'
		s[19] = '5ad5\n'
		s[20] = '6ab5\n'
		s[21] = '64ad\n'
		s[22] = '56ab\n'
		s[23] = '55aa\n'
		s[24] = 'd56a\n'
		s[25] = 'b55a\n'
		s[26] = 'ad56\n'
		s[27] = 'ab55\n'
		s[28] = 'aad5\n'
		s[29] = 'bb00\n'
		outputF = open('Conf/EASI_Slow_Control_6.txt', 'w')
		for line in s:
			outputF.write(line)
		outputF.close()
		
		inputF = open('Conf/EASI_Slow_Control_7.txt', 'r')
		s = inputF.readlines()
		inputF.close()
		s[11] = '7b0f\n'
		s[12] = '9bd0\n'
		s[13] = '6833\n'
		s[14] = '7a0c\n'
		s[15] = '8e6f\n'
		s[16] = '2d9b\n'
		s[17] = 'cb66\n'
		s[18] = 'f2d9\n'
		s[19] = '6c8e\n'
		s[20] = '5b23\n'
		s[21] = '91c6\n'
		s[22] = '66f2\n'
		s[23] = '391c\n'
		s[24] = '8e47\n'
		s[25] = '198c\n'
		s[26] = 'c67f\n'
		s[27] = 'f9b8\n'
		s[28] = 'cc8e\n'
		s[29] = '4700\n'
		outputF = open('Conf/EASI_Slow_Control_7.txt', 'w')
		for line in s:
			outputF.write(line)
		outputF.close()

		inputF = open('Conf/EASI_Slow_Control_12.txt', 'r')
		s = inputF.readlines()
		inputF.close()
		s[11] = '7b23\n'
		s[12] = '8cc3\n'
		s[13] = 'e472\n'
		s[14] = 'd91c\n'
		s[15] = '6633\n'
		s[16] = '1991\n'
		s[17] = 'c8e1\n'
		s[18] = 'f0f9\n'
		s[19] = '1c66\n'
		s[20] = '1f0f\n'
		s[21] = '87d2\n'
		s[22] = 'e0b0\n'
		s[23] = 'f87c\n'
		s[24] = '661f\n'
		s[25] = '1987\n'
		s[26] = 'cb63\n'
		s[27] = '3198\n'
		s[28] = '7c8e\n'
		s[29] = '5b00\n'
		outputF = open('Conf/EASI_Slow_Control_12.txt', 'w')
		for line in s:
			outputF.write(line)
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
				argv = ["./SendHV", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
				subprocess.call(argv)
			print('\n')

		
		print ('\nConfiguring Triggers...')

		arg = ["./SendFMaster", "MasterCMD/EN_MUX0.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX1.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX2.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX3.txt"]
		subprocess.call(arg)
		arg = ["./SendFMaster", "MasterCMD/EN_MUX4.txt"]
		subprocess.call(arg)

		#subprocess.call('./Reset')

		#print ('\nAquiring Trigger Rates and Counts...')

		#arg = ['./ReadMaster_cTrigger', '60', 'MasterCMD/START_TRG_CNT_60.txt', 'MasterCMD/RD_TRG_CNT.txt']
		#subprocess.call(arg)

		print ('\nAquiring Counts...')
		
		subprocess.call('./Reset')

		for Sk in skList :
			arg = ["./SendFSlaves", "Conf/ReadCount_" + Sk + ".txt"]
			subprocess.call(arg)
		time.sleep(11)
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
		#argv = ["./SendHV_rDown", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
		#subprocess.call(argv)
		argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
		subprocess.call(argv)
		argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_OFF_" + Sk + ".txt"]
		subprocess.call(argv)
