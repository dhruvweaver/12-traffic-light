#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np
import time
from utility import *
from PIL import Image
import torch



# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = False
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = True
enable_4k = True  # Will downscale 4K -> 1080p

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

xout.setStreamName("disparity")

# Properties
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setCamera("left")
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setCamera("right")

# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
depth.setLeftRightCheck(lr_check)
depth.setExtendedDisparity(extended_disparity)
depth.setSubpixel(subpixel)

# Linking
monoLeft.out.link(depth.left)
monoRight.out.link(depth.right)
depth.disparity.link(xout.input)

# Create device with config
config = dai.Device.Config()
config.board.uvc = dai.BoardConfig.UVC(1920, 1080)
config.board.uvc.frameType = dai.ImgFrame.Type.NV12
pipeline.setBoardConfig(config.board)

device = dai.Device(config)

# Start the pipeline
device.startPipeline(pipeline)

# Output queue will be used to get the disparity frames from the outputs defined above
q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)

text_helper = TextHelper()

model = torch.hub.load('ultralytics/yolov3', 'custom', path='../vision-prototype/custom-train/weights/best.pt')

# Assuming 'model' is your trained YOLOv3 model
cap = cv2.VideoCapture(0)  # 0 is usually the default webcam

while True:
#from while loop which opens color map
#////////////////////////////////////////////////////////////////////////////
    inDisparity = q.get()  # blocking call, will wait until a new data has arrived
    depthframe = inDisparity.getFrame()
    # Normalization for better visualization
    depthframe = (depthframe * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)

    cv2.imshow("disparity", depthframe)

    # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
    depthframe = cv2.applyColorMap(depthframe, cv2.COLORMAP_JET)
    cv2.imshow("disparity_color", depthframe)
#////////////////////////////////////////////////////////////////////////////
    
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:
        break

    # Convert the frame to PIL Image format as expected by the model
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    

    # Perform detection
    results = model(img)

    # Extract bounding box coordinates for 'red' and 'yellow' lights
    for *box, conf, cls in results.xyxy[0]:
        if int(cls) in [1, 2]:  # Check if the detected object is 'red' or 'yellow'
            xmin, ymin, xmax, ymax = map(int, box)  # Convert coordinates to integers
            light_type = 'red' if int(cls) == 1 else 'yellow'
            print(f"Coordinates of detected {light_type} light: (xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax})")
            print(f"Class Probability Score of detected {light_type} light: {conf}")

            # Draw bounding box on the frame
            top_left = (xmin, ymin)
            bottom_right = (xmax, ymax)
            text_helper.rectangle(frame, top_left, bottom_right)

            # Display the name of the light and its score on the frame
            text = f"{light_type}: {conf:.2f}"
            text_helper.putText(frame, text, (xmin, int(ymin - 0.05 * frame.shape[0])))

    # Display the frame
    cv2.imshow('Webcam Feed', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

