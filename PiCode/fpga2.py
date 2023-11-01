import serial
import time
import RPi.GPIO as GPIO

c211 = serial.Serial("/dev/ttyUSB0", 115200, 8, 'N', 1, timeout = 1)
angle = 0
time.sleep(1)

pin0 = 27
pin1 = 22
pin2 = 10
pin3 = 2
pin4 = 3
pin5 = 4
pin6 = 17
pins = [pin0, pin1, pin2, pin3, pin4, pin5, pin6]

def serial_read():
    event = c211.readline()
    event = event.decode('utf-8')
    event = event.split(",")
    if len(event) > 2:
        #Eddystone ID, RSSI, Azimuth, Elevation, ...
        angle = event[3] #elevation angle
        return int(angle)

slope = (127 - 0)/(180 - 0)

GPIO.setmode(GPIO.BCM)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

while True:
    try:
        angle = serial_read()
        angle = int(angle)
        angle = angle + 90
        angle = int(0 + slope * (angle - 0))
        print("new range: " + str(angle))
        angle = str(bin(angle))[2:]
        while len(angle) < 7:
            angle = "0" + angle
        #print(angle)
        for i in range(7):
            if angle[i] == '1':
                GPIO.output(pins[i], GPIO.HIGH)
            else:
                GPIO.output(pins[i], GPIO.LOW)
    except TypeError:
        pass
