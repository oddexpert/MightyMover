from time import sleep
from sense_hat import SenseHat
import math

sense = SenseHat()

while True:
   # Get the raw accelerometer, gyroscope, and magnetometer readings
   accel = sense.get_accelerometer_raw()
   gyro = sense.get_gyroscope_raw()
   mag = sense.get_compass_raw()

   # Compute the pitch, roll, and yaw angles from the sensor readings
   pitch = math.atan2(accel['y'], math.sqrt(accel['x']**2 + accel['z']**2))
   roll = math.atan2(accel['x'], math.sqrt(accel['y']**2 + accel['z']**2))
   yaw = math.atan2(mag['y'], mag['x']) + math.pi

   # Convert the angles from radians to degrees
   pitch = pitch * 180 / math.pi
   roll = roll * 180 / math.pi
   yaw = yaw * 180 / math.pi

   # Print the pitch, roll, and yaw angles
   int(yaw)
   print(yaw)
   sleep(1)

