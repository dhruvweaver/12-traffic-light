import cv2
import depthai as dai
import numpy as np
import time
from utility import *
from PIL import Image
import torch

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
        if int(cls) in [1, 2]:
            xmin, ymin, xmax, ymax = map(int, box)
            light_type = 'red' if int(cls) == 1 else 'yellow'
            print(f"Coordinates of detected {light_type} light: (xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax})")
            print(f"Class Probability Score of detected {light_type} light: {conf}")

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

    cv2.imshow('Webcam Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
