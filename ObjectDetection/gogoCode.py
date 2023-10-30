# Import packages
import os
import argparse
import numpy as np
import importlib.util
import time
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

# Define PictureTaker class to capture pictures from the PiCamera
class PictureTaker:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = (1.2, 1.5)
        self.camera.resolution = (640, 480)
        self.rawCapture = PiRGBArray(self.camera)
        self.camera.start_preview()

    def capture_picture(self):
        self.camera.capture(self.rawCapture, format="bgr")
        frame = self.rawCapture.array
        return frame

    def close(self):
        self.rawCapture.truncate(0)
        self.camera.close()

# Define and parse input arguments
MODEL_NAME = 'Sample_TFLite-model'
GRAPH_NAME = 'detect.tflite'
LABELMAP_NAME = 'labelmap.txt'

min_conf_threshold = 0.50
resW, resH = 640, 480
imW, imH = resW, resH

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
else:
    from tensorflow.lite.python.interpreter import Interpreter       

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del labels[0]

# Load the TensorFlow Lite model.
interpreter = Interpreter(model_path=PATH_TO_CKPT)
interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

print(input_details[0]['shape'])

# Check output layer name to determine if this model was created with TF2 or TF1,
# because outputs are ordered differently for TF2 and TF1 models
outname = output_details[0]['name']

if ('StatefulPartitionedCall' in outname): # This is a TF2 model
    boxes_idx, classes_idx, scores_idx = 1, 3, 0
else: # This is a TF1 model
    boxes_idx, classes_idx, scores_idx = 0, 1, 2

# Wanted labels
labels_tokeep = ["person", "dog", "handbag", "suitcase", "dining table", "backpack", 
                "sports ball", "bottle", "chair", "potted plant", "cell phone"]
legs=0

# Initialize the picture taker
picture_taker = PictureTaker()

try:

    while True:
        # Capture a picture
        frame = picture_taker.capture_picture()

        # Acquire frame and resize to expected shape [1xHxWx3]
        frame_resized = cv2.resize(frame, (300, 300))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Normalize pixel values if using a floating model (i.e., if the model is non-quantized)
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0]  # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0]  # Class index of detected objects
        scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0]  # Confidence of detected objects

        # Initiate frame labels to nothing, dictionary faster lookup than arrays
        frame_labels = {'label': [], 'ymax': [], 'width': []}

        # Loop over all detections and draw a detection box if confidence is above the minimum threshold
        for i in range(len(scores)):
            # Only process labels that we want from array labels_tokeep
            label_i = labels[int(classes[i])]
            if (label_i not in labels_tokeep):
                # print(label_i) #debugging purposes
                continue

            # run model on labels_tokeep
            if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                # Get bounding box coordinates and draw a box
                ymin = int(max(1, (boxes[i][0] * 480)))
                xmin = int(max(1, (boxes[i][1] * 640)))
                ymax = int(min(480, (boxes[i][2] * 480)))
                xmax = int(min(640, (boxes[i][3] * 640)))

                # Calculate the four corners of the bounding box
                # top_left = (xmin, ymin)
                # top_right = (xmax, ymin)
                # bottom_left = (xmin, ymax)
                # bottom_right = (xmax, ymax)

                # Calculate Width, to figure out if person's leg or legs is detected
                width = xmax - xmin

                # Collect labels in frame
                frame_labels["label"].append(label_i)
                frame_labels["ymax"].append(ymax)
                frame_labels["width"].append(width)

        key = cv2.waitKey(1) & 0xFF
        picture_taker.rawCapture.truncate(0)

        # Make Decisions
        if "person" in frame_labels['label']:
            if len(frame_labels['label']) > 2:
                print("Object Detected")
            else:
                # Get index of person
                person_indices = [i for i, label in enumerate(frame_labels['label']) if label == "person"]
                person_data = [{"ymax": frame_labels['ymax'][i], "width": frame_labels['width'][i]} for i in person_indices]
                if all(data['ymax'] > 300 for data in person_data):
                    if len(person_data) == 1:
                        print("one person and under threshold")
                    else:
                        if all(data['width'] < 125 for data in person_data):
                            print("legs, but go anyways")
                        else:
                            print("multiple people")
                else:
                    print("ymax not under 300")
        else :
            print("person not in frame")
        
except KeyboardInterrupt:
    picture_taker.close()
    pass 

# This was taken out for debugging purposes
# except Exception as e: 
#     picture_taker.close()
    
finally:
    picture_taker.close()
