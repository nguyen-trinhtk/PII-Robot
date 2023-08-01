import serial
import time
ser = serial.Serial('COM13', 9600, timeout=.1)

while True:
    ser.write(b"stop\n")