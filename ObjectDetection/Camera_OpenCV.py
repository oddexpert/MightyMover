from picamera2 import Picamera2, Preview
import time
import cv2

cv2.startWindowThread()

picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)})
picam2.configure(preview_config)

picam2.start()

# allow the camera to warmup
time.sleep(2)

# capture frames from the camera
try:
   while True:
      image = picam2.capture_array()

      cv2.imshow("Camera", image)
      cv2.waitKey(1)



except KeyboardInterrupt:
   print("\nKeyboardInterrupt detected. Exiting the program.")

finally:
   # Additional cleanup code, if needed
   print("Program closing.")
   cv2.destroyAllWindows
   picam2.close()
