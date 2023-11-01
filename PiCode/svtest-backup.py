import threading
#import board
import serial
import random
import time

c211 = serial.Serial("/dev/ttyUSB0", 115200, 8, 'N', 1, timeout = 1)
#c211 = "dummy"
arduino = serial.Serial("/dev/ttyACM0", 9600, 8, 'N', 1, timeout = 1)
angle = 0

def fake_serial_read(device):
    return random.randint(30,150)

def serial_read(device):
    while device.in_waiting > 0:
        event = device.readline()
    #event = device.readline()
    event = event.decode('utf-8')
    event = event.split(",")
    if len(event) > 2:
        #Eddystone ID, RSSI, Azimuth, Elevation, ...
        angle = event[3] #azimuth angle
        return angle

def serial_send(device, msg):
    device.write(msg.encode())
    #msg = [ord(str(ch)) for ch in str(msg)]
    #msg.append('\n')
    #try:
    #    for ch in msg:
    #        device.write(ch.encode())
    #except:
    #    print(msg)

if __name__ == "__main__":
    try:
        while True:
            try:
                angle = int(serial_read(c211))
                angle = angle + 90
            except:
                pass
            try:
                if 0 <= angle <= 180:
                    serial_send(arduino, str(angle)+'\n')
                    print("SENT: " + str(angle))
                else:
                    print("INVALID ANGLE")
            except ValueError:
                print("Input Invalid. Ignoring.")
            time.sleep(.1)
            #c211.reset_input_buffer()
    except KeyboardInterrupt:
        print("Exiting...")
        arduino.close()
        c211.close()
