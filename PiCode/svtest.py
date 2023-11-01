import threading
#import board
import serial
import random
import time
import asyncio

c211 = serial.Serial("/dev/ttyUSB0", 115200, 8, 'N', 1, timeout = 1)
arduino = serial.Serial("/dev/ttyACM0", 9600, 8, 'N', 1, timeout = 1)

angle = 0
time.sleep(1)

def fake_serial_read(device):
    return random.randint(30,150)

async def serial_read():
    global angle
    while True:
        event = c211.readline()
        event = event.decode('utf-8')
        event = event.split(",")
        if len(event) > 2:
            #Eddystone ID, RSSI, Azimuth, Elevation, ...
            angle = event[3] #azimuth angle
            return int(angle)

#def serial_send(device, msg):
    #device.write(msg.encode())
    #msg = [ord(str(ch)) for ch in str(msg)]
    #msg.append('\n')
    #try:
    #    for ch in msg:
    #        device.write(ch.encode())
    #except:
    #    print(msg)

async def serial_send():
    asyncio.create_task(serial_read())
    try:
        while True:
            try:
                angle = await serial_read()
                angle = int(angle)
                angle = angle + 90
                print(angle)
            except:
                pass
            try:
                if 0 <= angle <= 180:
                    arduino.write((str(angle)+'\n').encode())
                    print("SENT: " + str(angle))
                else:
                    print("INVALID ANGLE")
            except ValueError:
                print("Input Invalid. Ignoring.")
            time.sleep(.1)
    except KeyboardInterrupt:
        print("Exiting...")
        arduino.close()
        c211.close()

if __name__ == "__main__":
    asyncio.run(serial_send())
