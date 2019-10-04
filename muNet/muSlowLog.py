import os
import sys
import serial
import time
import subprocess
import datetime
import math

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


#QUEST = 'TB?\r'
QUEST = 'STAT?\r'

i = 0
while True:
	inFile = open('/home/DatiTB/DTC/RI.txt', 'r')
	s = inFile.readline()
	a = s.split('\t')
	run = str(a[1].replace('\n', ''))
	inFile.close()

	outFile = open('slowTemp','a')

	now = str(datetime.datetime.now())
	
	serArd0.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd0.readline())
		outs = out_byte.strip("'b")
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd1.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd1.readline())
		outs = out_byte.strip("'b")
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd2.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd2.readline())
		outs = out_byte.strip("'b")
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd3.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd3.readline())
		outs = out_byte.strip("'b")
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd4.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd4.readline())
		outs = out_byte.strip("'b")
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd5.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd5.readline())
		outs = out_byte.strip("'b")
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd6.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd6.readline())
		outs = out_byte.strip("'b")
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	serArd7.write(bytes(QUEST,'UTF-8'))
	for j in range(1) :
		out_byte = str(serArd7.readline())
		outs = out_byte.strip("'b")
		outFile.write(str(i) + '\t' + run + '\t' + outs + '\t' + now + '\n')
		print(outs)

	outFile.close()
	
	time.sleep(500)
	i = i+1

serArd0.close()
serArd1.close()
serArd2.close()
serArd3.close()
serArd4.close()
serArd5.close()
serArd6.close()
serArd7.close()

