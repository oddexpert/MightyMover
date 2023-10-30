from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.awb_mode = 'off'
camera.awb_gains = (1.2, 1.5)  # Adjust the values as needed
camera.resolution = (640, 480)

# Create a stream to capture images
rawCapture = PiRGBArray(camera)

# Allow the camera to warm up
camera.start_preview()

try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Image", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)

        if key == ord("q"):
            break  # Exit the loop if 'q' key is pressed

except KeyboardInterrupt:
    pass  # Handle Ctrl+C gracefully

finally:
    cv2.destroyAllWindows()
    rawCapture.truncate(0)
    camera.close()


