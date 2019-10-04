import os
import sys
import serial
import subprocess
import time

Start = time.time()

setT = int(sys.argv[1])
stopT = int(sys.argv[2])

serArd0 = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd1 = serial.Serial(
	port='/dev/ttyACM1',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd2 = serial.Serial(
	port='/dev/ttyACM2',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd3 = serial.Serial(
	port='/dev/ttyACM3',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd4 = serial.Serial(
	port='/dev/ttyACM4',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd5 = serial.Serial(
	port='/dev/ttyACM5',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd6 = serial.Serial(
	port='/dev/ttyACM6',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)
serArd7 = serial.Serial(
	port='/dev/ttyACM7',
	baudrate=38400,
	parity='N',
	stopbits=1,
	bytesize=8
)


serArd0.close()
serArd1.close()
serArd2.close()
serArd3.close()
serArd4.close()
serArd5.close()
serArd6.close()
serArd7.close()
serArd0.open()
serArd1.open()
serArd2.open()
serArd3.open()
serArd4.open()
serArd5.open()
serArd6.open()
serArd7.open()

for j in range(12) :
	out_byte = str(serArd0.readline())
	outs = out_byte.strip("'b")
for j in range(12) :
	out_byte = str(serArd1.readline())
	outs = out_byte.strip("'b")
for j in range(12) :
	out_byte = str(serArd2.readline())
	outs = out_byte.strip("'b")
for j in range(12) :
	out_byte = str(serArd3.readline())
	outs = out_byte.strip("'b")
for j in range(12) :
	out_byte = str(serArd4.readline())
	outs = out_byte.strip("'b")
for j in range(12) :
	out_byte = str(serArd5.readline())
	outs = out_byte.strip("'b")
for j in range(12) :
	out_byte = str(serArd6.readline())
	outs = out_byte.strip("'b")
for j in range(12) :
	out_byte = str(serArd7.readline())
	outs = out_byte.strip("'b")

QUEST = 'TA ' + str(setT) + '\r'
serArd0.write(bytes(QUEST,'UTF-8'))
serArd1.write(bytes(QUEST,'UTF-8'))
serArd2.write(bytes(QUEST,'UTF-8'))
serArd3.write(bytes(QUEST,'UTF-8'))
serArd4.write(bytes(QUEST,'UTF-8'))
serArd5.write(bytes(QUEST,'UTF-8'))
serArd6.write(bytes(QUEST,'UTF-8'))
serArd7.write(bytes(QUEST,'UTF-8'))

for j in range(1) :
	out_byte = str(serArd0.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd1.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd2.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd3.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd4.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd5.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd6.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd7.readline())
	outs = out_byte.strip("'b")


QUEST = 'TB ' + str(setT) + '\r'
serArd0.write(bytes(QUEST,'UTF-8'))
serArd1.write(bytes(QUEST,'UTF-8'))
serArd2.write(bytes(QUEST,'UTF-8'))
serArd3.write(bytes(QUEST,'UTF-8'))
serArd4.write(bytes(QUEST,'UTF-8'))
serArd5.write(bytes(QUEST,'UTF-8'))
serArd6.write(bytes(QUEST,'UTF-8'))
serArd7.write(bytes(QUEST,'UTF-8'))

for j in range(1) :
	out_byte = str(serArd0.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd1.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd2.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd3.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd4.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd5.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd6.readline())
	outs = out_byte.strip("'b")
for j in range(1) :
	out_byte = str(serArd7.readline())
	outs = out_byte.strip("'b")


outLog = []

while(time.time() < (Start + stopT)) :
	logStr = ''
	exitCode = 0
	QUEST = 'TA?\r'
	serArd0.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd0.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TA=', '').replace('\\r\\n', '')
		TA = float(outss)
		if (abs(TA - setT) < 2) : exitCode = exitCode + 1
	QUEST = 'TB?\r'
	serArd0.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd0.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TB=', '').replace('\\r\\n', '')
		TB = float(outss)
		if (abs(TB - setT) < 2) : exitCode = exitCode + 1
	logStr = logStr + str(TA) + '\t' + str(TB) + '\t'
		
	QUEST = 'TA?\r'
	serArd1.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd1.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TA=', '').replace('\\r\\n', '')
		TA = float(outss)
		if (abs(TA - setT) < 2) : exitCode = exitCode + 1
	QUEST = 'TB?\r'
	serArd1.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd1.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TB=', '').replace('\\r\\n', '')
		TB = float(outss)
		if (abs(TB - setT) < 2) : exitCode = exitCode + 1
	logStr = logStr + str(TA) + '\t' + str(TB) + '\t'
	 
	QUEST = 'TA?\r'
	serArd2.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd2.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TA=', '').replace('\\r\\n', '')
		TA = float(outss)
		if (abs(TA - setT) < 2) : exitCode = exitCode + 1
	QUEST = 'TB?\r'
	serArd2.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd2.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TB=', '').replace('\\r\\n', '')
		TB = float(outss)
		if (abs(TB - setT) < 2) : exitCode = exitCode + 1
	logStr = logStr + str(TA) + '\t' + str(TB) + '\t'

	QUEST = 'TA?\r'
	serArd3.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd3.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TA=', '').replace('\\r\\n', '')
		TA = float(outss)
		if (abs(TA - setT) < 2) : exitCode = exitCode + 1
	QUEST = 'TB?\r'
	serArd3.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd3.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TB=', '').replace('\\r\\n', '')
		TB = float(outss)
		if (abs(TB - setT) < 2) : exitCode = exitCode + 1
	logStr = logStr + str(TA) + '\t' + str(TB) + '\t'

	QUEST = 'TA?\r'
	serArd4.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd4.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TA=', '').replace('\\r\\n', '')
		TA = float(outss)
		if (abs(TA - setT) < 2) : exitCode = exitCode + 1
	QUEST = 'TB?\r'
	serArd4.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd4.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TB=', '').replace('\\r\\n', '')
		TB = float(outss)
		if (abs(TB - setT) < 2) : exitCode = exitCode + 1
	logStr = logStr + str(TA) + '\t' + str(TB) + '\t'

	QUEST = 'TA?\r'
	serArd5.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd5.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TA=', '').replace('\\r\\n', '')
		TA = float(outss)
		if (abs(TA - setT) < 2) : exitCode = exitCode + 1
	QUEST = 'TB?\r'
	serArd5.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd5.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TB=', '').replace('\\r\\n', '')
		TB = float(outss)
		if (abs(TB - setT) < 2) : exitCode = exitCode + 1
	logStr = logStr + str(TA) + '\t' + str(TB) + '\t'

	QUEST = 'TA?\r'
	serArd6.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd6.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TA=', '').replace('\\r\\n', '')
		TA = float(outss)
		if (abs(TA - setT) < 2) : exitCode = exitCode + 1
	QUEST = 'TB?\r'
	serArd6.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd6.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TB=', '').replace('\\r\\n', '')
		TB = float(outss)
		if (abs(TB - setT) < 2) : exitCode = exitCode + 1
	logStr = logStr + str(TA) + '\t' + str(TB) + '\t'

	QUEST = 'TA?\r'
	serArd7.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd7.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TA=', '').replace('\\r\\n', '')
		TA = float(outss)
		if (abs(TA - setT) < 2) : exitCode = exitCode + 1
	QUEST = 'TB?\r'
	serArd7.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd7.readline())
		outs = out_byte.strip("'b")
		outss = outs.replace('TB=', '').replace('\\r\\n', '')
		TB = float(outss)
		if (abs(TB - setT) < 2) : exitCode = exitCode + 1
	logStr = logStr + str(TA) + '\t' + str(TB) + '\t'

	logStr = logStr + str(exitCode) + '\n'
	outLog.append(logStr)
	print('EXITCODE : ' + str(exitCode) + '\n')
	if (exitCode == 16) :
		outLog = [] 
		break

if (exitCode != 16):
	logFile = open('/home/DatiTB/DTC/WPlogfile', 'w')
	for i in range(len(outLog)) :
		logFile.write(outLog[i])
	logFile.close()
	envFile = open('/home/DatiTB/DTC/ENV.txt', 'r')
	s = envFile.readlines()
	envFile.close()
	envFile = open('/home/DatiTB/DTC/ENV.txt', 'w')
	envFile.write('$FLG\t2\n')
	envFile.write(s[1])
	envFile.write(s[2])
	envFile.write(s[3])
	envFile.write('$WP\t-1\n')
	envFile.close()

serArd0.close()
serArd1.close()
serArd2.close()
serArd3.close()
serArd4.close()
serArd5.close()
serArd6.close()
serArd7.close()
