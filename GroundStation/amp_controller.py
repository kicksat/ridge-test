import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600)

def tx():
	arduino.write('0')
	print arduino.readline()

def rx():
	arduino.write('1')
	print arduino.readline()

