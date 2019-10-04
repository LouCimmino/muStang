import os
import sys
import serial
import time

onoff = sys.argv[1]

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

'''for j in range(12) :
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
	outs = out_byte.strip("'b")'''

QUEST = 'CHA ' + onoff + '\r'
print(QUEST)
serArd0.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd1.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd2.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd3.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd4.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd5.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd6.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd7.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)

QUEST = 'CHB ' + onoff + '\r'
print(QUEST)
serArd0.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd1.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd2.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd3.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd4.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd5.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd6.write(bytes(QUEST,'UTF-8'))
#time.sleep(30)
serArd7.write(bytes(QUEST,'UTF-8'))

serArd0.close()
serArd1.close()
serArd2.close()
serArd3.close()
serArd4.close()
serArd5.close()
serArd6.close()
serArd7.close()
print('TEC ACCESE!!!\n')
