import serial
import time

arduino = serial.Serial('/dev/ttyUSB0', 9600)
print arduino.readline()

def tx():
	arduino.write('0')
	print arduino.readline()

def rx():
	arduino.write('1')
	print arduino.readline()

