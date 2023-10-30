
import serial
from time import sleep

ser = serial.Serial ("/dev/ttyS0", 9600)

while True:
   received_data = ser.readline()
   print (received_data)
   ser.write(received_data)
