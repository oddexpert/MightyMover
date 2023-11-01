import time
import serial

ser = serial.Serial("/dev/ttyUSB0", 115200, 8, 'N', 1, timeout=1)

while True:
    rec = ser.readline()
    rec = rec.decode('utf-8')
    rec = rec.split(",")
    if len(rec) > 2: #some messages dont contain an angle
        angle = rec[3] #rec[4] = azimuth (left/right) angle
        print(angle)
