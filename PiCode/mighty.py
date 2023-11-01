import serial
import bluetooth
import time

class MightyMover():

    #mcu = serial.Serial("/dev/ttyACM0", 9600, 8, 'N', 1, timeout = 1)

    def __init__(self):
        self.c211 = serial.Serial("/dev/ttyUSB0", 115200, 8, 'N', 1, timeout = 1)
        self.characteristic_uuid = "00002a19-0000-1000-8000-00805f9b34fb"
        self.service_uuid = "0000180f-0000-1000-8000-00805f9b34fb"
        self.azi_angle = 4
        self.ele_angle = 8
        self.rssi = -50
        self.stop = False
        self.battery = []
        self.detect = []
        self.stop = True
        self.speed = 0

    #bluetooth - phone comms
    #cooper
    def handle_client(self, client_sock):
        #print("Accepted connection from", client_sock.getpeername())
        while True:
            for message_to_send in [str(self.rssi), "AZ" + str(self.azi_angle), "EL" + str(self.ele_angle)]:
                # Send each predefined message to the connected device
                client_sock.send(message_to_send.encode())
                print("Sent data:", message_to_send)
                time.sleep(1)  # Introduce a 1-second delay

            #exit_command = client_sock.recv(1024).decode().strip()
            #if exit_command.lower() == "exit":
                #break  # Exit the loop if "exit" is received

        print("Disconnected.")
        #client_sock.close()

    #serial from bluetooth module
    def setAngle(self):
        event = self.c211.readline()
        #print(event)
        if event:
            event = event.decode('utf-8')
            event = event.split(",")
            if len(event) > 2:
                #Eddystone ID, RSSI, Azimuth, Elevation, ...
                self.azi_angle = int(event[3]) + 90
                self.ele_angle = int(event[4]) + 90
                self.rssi = int(event[1])
              

    #serial to microcontroller
    def pwmSend(self, msg):
        self.mcu(msg.encode())

    #object detection
    #hanson

    #code to manipulate data?
    #idk what this even is

    #voltage level?
    #need to add circuitry for this

    #stop handling?
    def stopMover(self):
        self.stop = True
        #print("Stopped")

    def unstopMover(self):
        self.stop = False
        #print("Not stopped")

