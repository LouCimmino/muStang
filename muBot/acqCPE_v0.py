import sys 
import os 
import subprocess 
import time 
import zmq 
import curses

skList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']

numPeds = sys.argv[1]
numEvts = sys.argv[2]

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
	y = 6
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
	while s:
		s = inputF.readline()
		outputF.write(s)
	inputF.close()
	outputF.close()

subprocess.call("./Reset")

while True : 
	dac10 = 2610
	dac8 = 1977
		
	while True:
		print ('----------------------------')
		print ('DAC8 value  : ' + str(dac8))
		print ('DAC10 value : ' + str(dac10))
		print ('----------------------------')

		tFile = open('/home/DatiTB/DTC/ENV.txt', 'r')
		s = tFile.readlines()
		tFile.close()
		RUNflag = s[0].split('\t')
		RUNflag[1] = RUNflag[1].replace('\n', '')
		while (int(RUNflag[1]) == 1) : 
			time.sleep(60)
			tFile = open('/home/DatiTB/DTC/ENV.txt', 'r')
			s = tFile.readlines()
			tFile.close()
			RUNflag = s[0].split('\t')
			RUNflag[1] = RUNflag[1].replace('\n', '')

		s[4] = s[4].replace('$WP\t', '')
		workpoint = s[4].replace('\n', '')
		ATC = int(workpoint)

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
		if not(ATC==-1):
			DAC10 = []
			DAC10file = open('/home/DatiTB/DTC/WP_' + str(ATC) + 'deg', 'r')
			s = DAC10file.readlines()
			DAC10file.close()
			for ii in range(16) :
				DAC10.append(s[ii].split('\t'))
			dac10List = [DAC10[0][1].replace('\n', ''), DAC10[1][1].replace('\n', ''), DAC10[2][1].replace('\n', ''), DAC10[3][1].replace('\n', ''), DAC10[4][1].replace('\n', ''), DAC10[5][1].replace('\n', ''), DAC10[6][1].replace('\n', ''), DAC10[7][1].replace('\n', ''), DAC10[8][1].replace('\n', ''), DAC10[9][1].replace('\n', ''), DAC10[10][1].replace('\n', ''), DAC10[11][1].replace('\n', ''), DAC10[12][1].replace('\n', ''), DAC10[13][1].replace('\n', ''), DAC10[14][1].replace('\n', ''), DAC10[15][1].replace('\n', '')]

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

		#inputF = open('Conf/EASI_Slow_Control_15.txt', 'r')
		#s = inputF.readlines()
		#inputF.close()
		#s[3] = 'fffb\n'
		#outputF = open('Conf/EASI_Slow_Control_15.txt', 'w')
		#for line in s:
		#	outputF.write(line)
		#outputF.close()
		#inputF = open('Conf/EASI_Slow_Control_13.txt', 'r')
		#s = inputF.readlines()
		#inputF.close()
		#s[3] = 'fbfe\n'
		#outputF = open('Conf/EASI_Slow_Control_13.txt', 'w')
		#for line in s:
		#	outputF.write(line)
		#outputF.close()

		inputF = open('Conf/EASI_Slow_Control_5.txt', 'r')
		s = inputF.readlines()
		inputF.close()
		s[11] = '7b05\n'
		s[12] = 'a0c8\n'
		s[13] = 'de31\n'
		s[14] = '98cc\n'
		s[15] = '8e5b\n'
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
		s[27] = '3239\n'
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
			argv = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
			subprocess.call(argv)
			argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_OFF_" + Sk + ".txt"]
			subprocess.call(argv)


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

		if (ATC!=-1):
			arg = ['python3', 'HV_Set.py', '31.1', str(ATC)]
			#arg = ['python3', 'HV_Set.py', '20.1', str(ATC)]
			subprocess.call(arg)

		for Sk in skList :
			argv = ["./SendFSlaves", "Conf_HV/EASI_SwHV_ON_" + Sk + ".txt"]
			subprocess.call(argv)
			argv = ["./SendHV", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
			subprocess.call(argv)
		print('\n')



		#	if (ATC!=-1):
				#vopFile = open('Conf_HV/EASI_HV-OUT_Vop_' + Sk + '.txt', 'r')
				#vbiasFile = open('Conf_HV/EASI_HV-OUT_Vbias_' + Sk + '.txt', 'w')
				#s = vopFile.readline()
				#vbiasFile.write(s)
				#s = vopFile.readline()
				#vopFile.close()
				#s = s.replace('\n', '')
				#Vnew = hex(int(s,16) + round((23.5 - ATC)*0.06/0.18))
				#Vnew = Vnew.replace('x', '0')
				#vbiasFile.write(Vnew)
				#vbiasFile.close()

		
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
		
		subprocess.call('./Reset')

		MUXapp = ''
		for mux in range(5):
			inputF = open('MasterCMD/EN_MUX' + str(mux) + '.txt', 'r')
			s = inputF.readlines()
			MUXapp = MUXapp + s[1].replace('\n', '') + '\t'
			inputF.close()
		outputF = open('/home/DatiTB/DTC/MUXtemp_ROSSO', 'w')
		outputF.write(MUXapp)
		outputF.close()

		runCounter = 0
		evts = 10000
		pedEvts = 10000

		inpFile = open('/home/DatiTB/DTC/ENV.txt', 'r')
		s = inpFile.readlines()
		inpFile.close()
		RUNflag = s[0].split('\t')
		RUNflag[1] = RUNflag[1].replace('\n', '')

		if (int(RUNflag[1]) == 1) : break

		print('\nContacting muNet... ')
		subprocess.call('./sendStart')
		print("Ready to go!\n")
		#while (runCounter<int(numRuns)):
		while True:
			context = zmq.Context()
			socket = context.socket(zmq.REP)
			socket.bind("tcp://*:5000")

			buffer = socket.recv().decode('utf-8')
			runNum = buffer.replace('@', '')
			print(runNum)
			runCounter = int(runNum.strip('\0'))
			socket.send(b"Ok")
			#runCounter = runCounter + 1
			print ('\nAquiring Trigger Rates and Counts...')
		
			arg = ['./ReadMaster_cTrigger', '60', 'MasterCMD/START_TRG_CNT_60.txt', 'MasterCMD/RD_TRG_CNT.txt']
			subprocess.call(arg)
	
			subprocess.call("./Reset")
			print('\n')
			arg = ["./SendFMaster", "MasterCMD/EN_DEL0.txt"]
			subprocess.call(arg)
			arg = ["./SendFMaster", "MasterCMD/EN_DEL1.txt"]
			subprocess.call(arg)
			arg = ["./SendFMaster", "MasterCMD/EN_DEL2.txt"]
			subprocess.call(arg)
			arg = ["./SendFMaster", "MasterCMD/EN_DEL3.txt"]
			subprocess.call(arg)
	
			arg = ['./ReadMaster_cTrigger_DLY', '60', 'MasterCMD/START_TRG_CNT_60.txt', 'MasterCMD/RD_TRG_CNT.txt']
			subprocess.call(arg)
			print('\n')

			arg = ['cp', 'cTrigger_Counts', '/home/DatiTB/cTrigger_Counts']
			subprocess.call(arg)
			arg = ['rm', 'cTrigger_Counts']
			subprocess.call(arg)
			
			subprocess.call("./Reset")
			time.sleep(1)
			for Sk in skList :
				argv = ["./SendFSlaves", "Conf/ReadCount_" + Sk + ".txt"]
				subprocess.call(argv)
			time.sleep(11)
			for Sk in skList :
				argv = ["./SendFSlaves", "Conf/ReadSlave_" + Sk + ".txt"]
				subprocess.call(argv)
			
				subprocess.call("./ReadMaster_count")
				inp = open('/home/DatiTB/SlaveCounts', 'r')
				outp = open('/home/DatiTB/Counts_LAB', 'a')

				r = inp.readline()
				r = r.replace('\n', '')
				while r :
					w = Sk + '\t' + r + str(dac10) + '\t' + str(int(time.time())) + '\n'
					outp.write(w)
					r = inp.readline()
				inp.close()
				outp.close()
				
				argv = ["rm", "/home/DatiTB/SlaveCounts"]
				subprocess.call(argv)
					
			argv = ["mv", "/home/DatiTB/Counts_LAB", "/home/DatiTB/SlavesCount_run" + str(runCounter)]
			subprocess.call(argv)
			print ('I END Count\n\n')
			
			inpFile = open('/home/DatiTB/DTC/ENV.txt', 'r')
			s = inpFile.readlines()
			inpFile.close()
			RUNflag = s[0].split('\t')
			RUNflag[1] = RUNflag[1].replace('\n', '')
			if (int(RUNflag[1]) == 1) : 
				break
			subprocess.call('./sendStart')
			
			pedCounter = 0
			adcCounter = 0
			
			print ('Doing Pedestal...\n')

			while(pedCounter < int(numPeds)):
				inpFile = open('/home/DatiTB/DTC/ENV.txt', 'r')
				s = inpFile.readlines()
				inpFile.close()
				RUNflag = s[0].split('\t')
				RUNflag[1] = RUNflag[1].replace('\n', '')
				if (int(RUNflag[1]) == 1) : 
					break
				outputF = open('/home/DatiTB/pedData', 'w')
				outputF.write(str(int(round(time.time()*1000))) + '\n')
				outputF.close()		
			
				pedCounter = pedCounter + 1
				arg = ['./ReadPed', str(pedEvts) , skList[0], skList[1], skList[2], skList[3], skList[4], skList[5], skList[6], skList[7], skList[8], skList[9], skList[10], skList[11], skList[12], skList[13], skList[14], skList[15]]
				subprocess.call(arg)

				outputF = open('/home/DatiTB/pedData', 'a')
				outputF.write(str(int(round(time.time()*1000))))
				outputF.close()
			
				arg = ['mv', '/home/DatiTB/pedData', '/home/DatiTB/pedData_evts' + str(pedEvts*int(numPeds)) + '_run' + str(runCounter) + '_sr' + str(pedCounter)]
				subprocess.call(arg)
			
			print("Run " + str(runCounter) + " :: Now reading")

			while(adcCounter < int(numEvts)):
				inpFile = open('/home/DatiTB/DTC/ENV.txt', 'r')
				s = inpFile.readlines()
				inpFile.close()
				RUNflag = s[0].split('\t')
				RUNflag[1] = RUNflag[1].replace('\n', '')
				if (int(RUNflag[1]) == 1) : 
					inpFile = open('/home/DatiTB/DTC/ENV.txt', 'w')
					inpFile.write('$FLG\t2\n')
					inpFile.write(s[1])
					inpFile.write(s[2])
					inpFile.write(s[3])
					inpFile.write(s[4])
					inpFile.close()
					break

				outputF = open('/home/DatiTB/slaveData', 'w')
				outputF.write(str(int(round(time.time()*1000))) + '\n')
				outputF.close()

				adcCounter = adcCounter + 1
				arg = ['./ReadSlave', str(evts) , skList[0], skList[1], skList[2], skList[3], skList[4], skList[5], skList[6], skList[7], skList[8], skList[9], skList[10], skList[11], skList[12], skList[13], skList[14], skList[15]]
				subprocess.call(arg)

				outputF = open('/home/DatiTB/slaveData', 'a')
				outputF.write(str(int(round(time.time()*1000))))
				outputF.close()
			
				arg = ['mv', '/home/DatiTB/slaveData', '/home/DatiTB/slaveData_evts' + str(evts*int(numEvts)) + '_run' + str(runCounter) + '_sr' + str(adcCounter)]
				subprocess.call(arg)

			if (int(RUNflag[1]) == 1) : break
			print('\nContacting muNet... ')
			subprocess.call('./sendStart')
			print("Ready to go!\n")

	print ('\n--- Shutting Down System\n')
	for Sk in skList :
		#argv = ["./SendHV_rDown", "Conf_HV/EASI_HV-OUT_Vbias_" + Sk + ".txt"]
		#subprocess.call(argv)
		arg = ["./SendHV_NORUMP", "Conf_HV/EASI_HV-OUT_ShutDown_" + Sk + ".txt"]
		subprocess.call(arg)
		arg = ["./SendFSlaves", "Conf_HV/EASI_SwHV_OFF_" + Sk + ".txt"]
		subprocess.call(arg)
