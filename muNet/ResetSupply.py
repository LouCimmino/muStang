import time
import serial
import subprocess
import os

print ('MuBot ver 2.0beta - MuRay Experiment')
print ('Copyright 2012(C) 19LC77 (email : luigi.cimmino@na.infn.it)')
print ('__________________________________________________________\n')

wami = os.popen('whoami').read().rstrip()

ser2 = serial.Serial(
	port='/dev/ttyUSB0', 
	baudrate=9600, 
	parity='N', 
	stopbits=2, 
	bytesize=8
	)
#ser1 = serial.Serial(
#	port='/dev/ttyUSB3', 
#	baudrate=9600, 
#	parity='N', 
#	stopbits=2, 
#	bytesize=8
#	)
	
print ('__________________________________________________________')

print ('\n*******************\n')
print ('**  RESETTING... **\n')
print ('*******************\n')

print ('--- Shutting Down Supplies\n')
#inp1 = 'OUTP OFF'
inp2 = 'OUTP OFF'

#for i in range (len(inp1)) :
#	ser1.write(str.encode(inp1[i]))
#ser1.write(str.encode('\n'))
for i in range (len(inp2)) :
	ser2.write(str.encode(inp2[i]))
ser2.write(str.encode('\n'))

print ('Done!\n\n')

time.sleep(1)

print ('--- Appling Settings\n')
#inp1 = 'APPL P25V,8.5'
#for i in range (len(inp1)) :
#	ser1.write(str.encode(inp1[i]))
#ser1.write(str.encode('\n'))
inp1 = 'APPL P6V,6.15'
for i in range (len(inp1)) :
	ser2.write(str.encode(inp1[i]))
ser2.write(str.encode('\n'))
inp2 = 'APPL N25V,-9.0'
for i in range (len(inp2)) :
	ser2.write(str.encode(inp2[i]))
ser2.write(str.encode('\n'))
#inp3 = 'APPL P25V,0'
#for i in range (len(inp3)) :
#	ser2.write(str.encode(inp3[i]))
#ser2.write(str.encode('\n'))
#inp4 = 'VOLT 35.00'
#for i in range (len(inp4)) :
#	ser4.write(str.encode(inp4[i]))
#ser4.write(str.encode('\n'))
print ('Done!\n\n')


time.sleep(1)

print ('--- Power ON Mu-RAY\n')
#inp1 = 'OUTP ON'
inp2 = 'OUTP ON'
#for i in range (len(inp1)) :
#	ser1.write(str.encode(inp1[i]))
#ser1.write(str.encode('\n'))
for i in range (len(inp2)) :
	ser2.write(str.encode(inp2[i]))
ser2.write(str.encode('\n'))

print ('Done!\n\n')
print ('__________________________________________________________')
