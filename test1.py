import serial
from time import sleep
print ("Hello World")
ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
while True:
   received_data = str(ser.readline())              #read serial port
   if received_data.startswith( "b'$GPGLL" ):
      data = received_data.split(",")
      if data[-2] == 'V':
         print ("no satellite signal")
      else:
         print (received_data)                   #print received data
