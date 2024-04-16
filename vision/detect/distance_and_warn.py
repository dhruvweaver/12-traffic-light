import cv2
import depthai as dai
import numpy as np
import time
from utility import *
from PIL import Image
import math
import torch

# demo variables for OBD data
camera_height = 4.5
speed = 35.0
dist_to_light = 0.0
light = 0


# warning functions
def miles_to_km(miles):
    return miles * 1.609344


def calc_dist_to_inter(dist):
    dist = math.sqrt(camera_height**2 - dist**2)
    print(f'Distance to intersection {dist}')
    return dist


def min_brake_dist_ft(speed):
    kmh = miles_to_km(speed)
    meters = kmh**2 / (250 * 0.8)
    # distance in feet
    return meters * 3.28084


def gentle_warning():
    print('warning 😀')


def strong_warning():
    print("WARNING 😬")


def brake_warning(speed):
    brake_dist = min_brake_dist_ft(speed)
    print(f'Calculated brake distance: {brake_dist}')
    if (light > 0):
        if (brake_dist < dist_to_light):
            gentle_warning()
        else:
            strong_warning()

# Configuration variables
extended_disparity = False
subpixel = False
lr_check = True
enable_4k = True

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
depth = pipeline.create(dai.node.StereoDepth)
xout = pipeline.create(dai.node.XLinkOut)

# Define a source - color camera
cam_rgb = pipeline.createColorCamera()
cam_rgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
cam_rgb.setInterleaved(False)

if enable_4k:
    cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
    cam_rgb.setIspScale(1, 2)
else:
    cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

# Create an UVC (USB Video Class) output node
uvc = pipeline.createUVC()
cam_rgb.video.link(uvc.input)

xout.setStreamName("depth")

# Properties
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setCamera("left")
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setCamera("right")

# Create a node that will produce the depth map
depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
depth.setLeftRightCheck(lr_check)
depth.setExtendedDisparity(extended_disparity)
depth.setSubpixel(subpixel)

# Linking
monoLeft.out.link(depth.left)
monoRight.out.link(depth.right)
depth.depth.link(xout.input)

# Create device with config
config = dai.Device.Config()
config.board.uvc = dai.BoardConfig.UVC(1920, 1080)
config.board.uvc.frameType = dai.ImgFrame.Type.NV12
pipeline.setBoardConfig(config.board)

device = dai.Device(config)

# Start the pipeline
device.startPipeline(pipeline)

# Output queue will be used to get the depth frames from the outputs defined above
q = device.getOutputQueue(name="depth", maxSize=4, blocking=False)

text_helper = TextHelper()

model = torch.hub.load('ultralytics/yolov3', 'custom', path='../vision-prototype/custom-train/weights/best.pt')

# Assuming 'model' is your trained YOLOv3 model
cap = cv2.VideoCapture(0)

while True:

#////////////////////////////////////////////////////////
    inDepth = q.get()
    depthframe = inDepth.getFrame()

    # Convert depth frame to meters by dividing by 1000
    depthframe = depthframe / 1000.0

    cv2.imshow("depth", depthframe)
#/////////////////////////////////////////////////////////

    ret, frame = cap.read()
    if not ret:
        break

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    results = model(img)

    for *box, conf, cls in results.xyxy[0]:
        if int(cls) in [0, 1, 2]:
            xmin, ymin, xmax, ymax = map(int, box)
            light_type = 'red' if int(cls) == 1 else 'yellow' if int(cls) == 2 else 'green'
            print(f"Coordinates of detected {light_type} light: (xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax})")
            print(f"Class Probability Score of detected {light_type} light: {conf}")

            if (light_type == 'red'):
                light = 2
            elif (light_type == 'yellow'):
                light = 1
            else:
                light = 0

            print(f'Light: {light}')

            top_left = (xmin, ymin)
            bottom_right = (xmax, ymax)
            text_helper.rectangle(frame, top_left, bottom_right)

            webcam_height, webcam_width = frame.shape[:2]
            depth_height, depth_width = depthframe.shape[:2]

            center_x = (xmin + xmax) // 2
            center_y = (ymin + ymax) // 2

            scale_x = depth_width / webcam_width
            scale_y = depth_height / webcam_height
            center_x = int(center_x * scale_x)
            center_y = int(center_y * scale_y)

            depth_value = depthframe[center_y, center_x]
            print(f"Depth at the center of the detected {light_type} light: {depth_value} meters")

            text = f"{light_type}: {conf:.2f}, Depth: {depth_value:.2f} meters"
            text_helper.putText(frame, text, (xmin, int(ymin - 0.05 * frame.shape[0])))

            # convert distance to feet.
            # this could be simplified through the whole process
            dist_to_light = depth_value * 3.28084
            brake_warning(speed)

    cv2.imshow('Webcam Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
