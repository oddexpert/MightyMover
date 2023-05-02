import serial
from time import sleep

#############################
##
## This code interprets the data coming from the gt-u7
## gps module. We need to know latitude and longitude.
## Signal strength and number of satelites is also good
## to have display. We also need a way to call this data
## into another program, and a clean way to display the
## data while debugging.
##
#############################

ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
flag = "off"

while True:
   lati = 0
   longi = 0
   received_data = str(ser.readline())              #read serial port
   if received_data.startswith( "b'$GPRMC" ):
      data = received_data.split(",")
      if data[2] == 'V':
         print ("no satellite signal")
         flag = True
      else:
         lat = data[3]
         long = data[5]
         lati = lat[0]+lat[1]+'.'+lat[2]+lat[3]+lat[5]+lat[6]+lat[7]
         if long[0] == "0":
            longi = "-"+long[1]+long[2]+'.'+long[3]+long[4]+long[6]+long[7]+long[8]
         else :
            longi = long[0]+long[1]+'.'+long[2]+long[3]+long[5]+long[6]+long[7]
         lati = round(float(lati) + 0.00173, 5)
         longi = round(float(longi) - 0.25717, 5)
         print (lati, longi) #print lat and long
         flag = "on"
   if received_data.startswith( "b'$GPGSV" ):
      data = received_data.split(",")
      if flag == True :
         flag = False
      elif data[2] == "1":
         print("Satellites: " + data[3])


