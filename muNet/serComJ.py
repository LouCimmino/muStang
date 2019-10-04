import time
import serial
import subprocess
import os

print ('MuBot ver 2.0beta - MuRay Experiment')
print ('Copyright 2012(C) 19LC77 (email : luigi.cimmino@na.infn.it)')
print ('__________________________________________________________\n')

wami = os.popen('whoami').read().rstrip()
deg = '\u00b0'

ser = serial.Serial(
	port='/dev/ttyUSB1',
	baudrate=38400,
	parity='E',
	stopbits=1,
	bytesize=7,
	xonxoff=1
	)

ser.close()
ser.open()
ser.isOpen()

msg = 'in_pv_00'

inp=''
out=''

for i in range (len(msg)) :
	ser.write(str.encode(msg[i]))
ser.write(str.encode(chr(0x0D)))

time.sleep(1)
while ser.inWaiting() > 0 :
	out_byte = ser.read()
	if (bytes.decode(out_byte) != '\n' and bytes.decode(out_byte) != '\r') : out += bytes.decode(out_byte)
if (out  != '') :
	print ('Actual bath temperature : ' + out + deg + 'C')
	out=''
else :
	print ("No resp!")

msg = 'in_pv_01'

for i in range (len(msg)) :
	ser.write(str.encode(msg[i]))
ser.write(str.encode(chr(0x0D)))

time.sleep(1)
while ser.inWaiting() > 0 :
	out_byte = ser.read()
	if (bytes.decode(out_byte) != '\n' and bytes.decode(out_byte) != '\r') : out += bytes.decode(out_byte)
if (out  != '') :
	print ('[ ' + out + '% of total power used ]')
	out=''
else :
	print ("No resp!")

	
print ('__________________________________________________________')

inp=''
out=''
while 1 :
	print ('\nEnter your commands below.\r\n"help" for command list.')
	inp = input("[" + wami + "@pcmurayxx JComm]# ")
	inm = inp
	if (inp == 'q') or (inp == 'quit'):
		ser.close()
		exit()
	if (inp == 'h') or (inp == 'help'):
		print("* Jcomm HELP\n")
		print("General ----------------------------------------------")
		print(": h or help 	Show this help")
		print(": q or quit	Exit JComm")
		print("------------------------------------------------------\n")
		print("Control ----------------------------------------------")
		print(": status	Actual unit status")
		print(": start		Start the unit")
		print(": stop		Stop the unit")
		print("------------------------------------------------------\n")
		print("Settings ---------------------------------------------")
		print(": spused	Show set point in use")
		print(": listsp<n>	Show stored setpoint")
		print(": listpps	Show pump pressure stage in use")
		print(": setsp<n>	Set working temperature number <n>")
		print(": usesp<n>	use working temperature number <n>")
		print("		(<n> = 1, 2, 3)")
		print("------------------------------------------------------\n")
		print("Acnowledgement ---------------------------------------")
		print("- Every mistyped command will be ignored...")
		print("- You can also run command from the native list!")
		print("- Copyright 2012(C) 19LC77 (luigi.cimmino@na.infn.it)")
		print("------------------------------------------------------\n")
		print("*** End HELP\n")
	if (inm == 'status'):
		inp = 'in_mode_05'
	if (inm == 'start'):
		inp = 'out_mode_05 1'
	if (inm == 'stop'):
		inp = 'out_mode_05 0'
	if (inm == 'listsp1'):
		inp = 'in_sp_00'
	if (inm == 'listsp2'):
		inp = 'in_sp_01'
	if (inm == 'listsp3'):
		inp = 'in_sp_02'
	if (inm == 'spused'):
		inp = 'in_mode_01'
	if (inm == 'listpps'):
		inp = 'in_sp_07'
	if (inm == 'setsp1'):
		inp = ''
	if (inm == 'setsp2'):
		inp = ''
	if (inm == 'setsp3'):
		inp = ''
	if (inm == 'usesp1'):
		inp = 'out_mode_01 0'
	if (inm == 'usesp2'):
		inp = 'out_mode_01 1'
	if (inm == 'usesp3'):
		inp = 'out_mode_01 2'
	if (inm != 'h') and (inm != 'help') :
		for i in range (len(inp)) :
			ser.write(str.encode(inp[i]))
		ser.write(str.encode(chr(0x0D)))
	
	time.sleep(1)
	while ser.inWaiting() > 0 :
		out_byte = ser.read()
		out += bytes.decode(out_byte)
	if (out  != '') :
		print ('>>' + out)
		out=''
	else :
		if (inm != 'h') and (inm != 'help') :
			print ("Julabo is not responding!\nIf an error occurred please run diagnostic")
	
	print ('__________________________________________________________')
