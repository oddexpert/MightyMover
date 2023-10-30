from gpiozero import Servo
from time import sleep
import serial
from sense_hat import  SenseHat
from math import radians, cos, sin, atan2, sqrt, abs

sense = SenseHat()
sense.set_imu_config(True, False, False)
motor_port = 13
servo_port = 12
ser = serial.Serial ("/dev/ttyS0", 9600)
flag="off"

def get_direction_and_distance(start_lat, start_lon, end_lat, end_lon):
    # convert decimal degrees to radians
    start_lat, start_lon, end_lat, end_lon = map(radians, [start_lat, start_lon, end_lat, end_lon])

    # haversine formula
    dlat = end_lat - start_lat 
    dlon = end_lon - start_lon 
    a = sin(dlat/2)**2 + cos(start_lat) * cos(end_lat) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a)) 
    distance = 6371 * c # radius of earth in km

    # bearing formula
    y = sin(end_lon - start_lon) * cos(end_lat)
    x = cos(start_lat) * sin(end_lat) - sin(start_lat) * cos(end_lat) * cos(end_lon - start_lon)
    bearin = atan2(y, x) * 180 / pi

    return (bearin, distance)


def motor(action):
	servo = Servo(motor_port)
	if (action == "Forward"):
		val = -0.13
	elif (action == "Back"):
		val = -0.4
	else :
		val = -0.35

	try:
		servo.value = val
		sleep(4)
		print ("Successful!", action)

	except KeyboardInterrupt:
		print ("Program Interrupted")

def servo_m(action):
	servo = Servo(servo_port)
	if (action == "Left"):
		val = 0.75
	elif (action == "Right"):
		val = -0.75
	else :
		val = 0
	try:
		servo.value = val
		sleep(1)
		print("Sucessful!", action)

	except KeyboardInterrupt:
		print("Program Interrupted")

def GPS():
	lati = 0
	longi = 0
	received_data = str(ser.readline())
	if received_data.startswith( "b'$GPRMC" ):
		data = received_data.split(",")
		if data[2] == 'V':
			out = "no satellite signal"
			flag = True
		else:
			lat = data[3]
			long = data[5]
			lati = lat[0]+lat[1]+'.'+lat[2]+lat[3]+lat[5]+lat[6]+lat[7]
         		if long[0] == "0":
            			longi = "-"+long[1]+long[2]+'.'+long[3]+long[4]+long[6]+long[7]+long[8]
         		else :
            			longi = long[0]+long[1]+'.'+long[2]+long[3]+long[5]+long[6]+long[7]
         		out1 = round(float(lati) + offset1, 5)
         		out2 = round(float(longi) - offset2, 5)
         		out = [out1, out2]
			print (lati, longi) #print lat and long
         		flag = False
   	if received_data.startswith( "b'$GPGSV" ):
      		data = received_data.split(",")
      		if flag == True :
         		flag = False
      		elif data[2] == "1":
         		print("Satellites: " + data[3])
	print (out)
	return (out)

def get_location():
	bear = sense.get_compass()
	if bear < 45 or bear > 315:
		sense.show_letter('N')
	elif bear < 135:
		sense.show_letter('E')
	elif bear < 225:
		sense.show_letter('S')
	else :
		sense.show_letter('W')
	print (bear)
	return (bear)

def calibrate(phone_lat, phone_long)
	while True:
		if (GPS() == "no satellite signal"):
			continue
		else :
			break
	offset1 = phone_lat - (GPS())[0]
	offset2 = phone_long - (GPS())[1]

first_lat = input ("Enter your phone's  GPS latitude")
first_long = input ("Enter your phone's GPS longitude")
calibrate(first_lat, first_long)

while True:
	if (GPS() == "no satellite signal"):
		continue
	else :
		new_location1 = input ("Enter your phone's GPS latitude")
		new_location2 = input ("Enter your phone's GPS longitude")
		destination = [new_location1, new_location2]
		start = GPS()
		bearing, dist = get_direction_and_distance(start[0], start[1], new_location1, new_location2)
		if (bearing != get_location()):
			while True:
				angle_d = int(bearing - get_location())
				angle2 = int(360 - angle_d)
				if (angle_d > angle2):
					servo_m("Left")
					motor("Forward")
				elif (angle_d < angle2):
					servo_m("Right")
					motor("Forward")
				else :
					break
		while True:
			new_cord = GPS()
			if (new_cord != destination)
				motor("Forward")
			else :
				break

