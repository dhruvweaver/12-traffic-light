import cv2
import depthai as dai
from calc import HostSpatialsCalc
from utility import *
import numpy as np
import math
import time
import torch

# Load the pre-trained YOLO model
model = torch.hub.load('ultralytics/yolov3', 'custom', path='../vision-prototype/custom-train/weights/best.pt')

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
colorCam = pipeline.create(dai.node.ColorCamera)
monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
stereo = pipeline.create(dai.node.StereoDepth)

# Properties
colorCam.setBoardSocket(dai.CameraBoardSocket.RGB)
colorCam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_720_P)

monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

stereo.initialConfig.setConfidenceThreshold(255)
stereo.setLeftRightCheck(True)
stereo.setSubpixel(False)

# Linking
monoLeft.out.link(stereo.left)
monoRight.out.link(stereo.right)

xoutColor = pipeline.create(dai.node.XLinkOut)
xoutColor.setStreamName("color")
colorCam.video.link(xoutColor.input)

xoutDepth = pipeline.create(dai.node.XLinkOut)
xoutDepth.setStreamName("depth")
stereo.depth.link(xoutDepth.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    # Output queue will be used to get the depth frames from the outputs defined above
    colorQueue = device.getOutputQueue(name="color")
    depthQueue = device.getOutputQueue(name="depth")

    text = TextHelper()
    hostSpatials = HostSpatialsCalc(device)

    while True:
        colorData = colorQueue.get()
        colorFrame = colorData.getCvFrame()

        # Use YOLO model to detect objects
        results = model(colorFrame)

        # For each detected object
        for result in results.xyxy[0]:
            # Get the bounding box coordinates
            x1, y1, x2, y2 = map(int, result[:4])
            

            # Get depth data
            depthData = depthQueue.get()

            # Calculate spatial coordinates from depth frame
            spatials, centroid = hostSpatials.calc_spatials(depthData, (x1, y1, x2, y2))

            # Draw the bounding box and display the spatial coordinates
            text.rectangle(colorFrame, (x1, y1), (x2, y2))
            text.putText(colorFrame, "X: " + ("{:.1f}m".format(spatials['x']/1000) if not math.isnan(spatials['x']) else "--"), (x1, y1 - 20))
            text.putText(colorFrame, "Y: " + ("{:.1f}m".format(spatials['y']/1000) if not math.isnan(spatials['y']) else "--"), (x1, y1 - 35))
            text.putText(colorFrame, "Z: " + ("{:.1f}m".format(spatials['z']/1000) if not math.isnan(spatials['z']) else "--"), (x1, y1 - 50))

        # Show the frame
        cv2.imshow("color", colorFrame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
