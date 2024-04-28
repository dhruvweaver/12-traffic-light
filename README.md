# Team 12 Capstone Project: Traffic Light Detection
Central repository for the traffic light detection capstone project.

***Documentation for each component of the project (car communication, testing, and computer vision) will be within each respective directory, and updated as progress is made.***

### Overview:
This repository contains three sections, each with their own directory.

Clone the repository into your working directory:

***You can also rename the repo to something more simple when you clone it, as shown:***
```bash
cd development
git clone https://github.com/dhruvweaver/12-traffic-light.git capstone
```
You now have a local copy of the repo on your computer. Go to that directory:
```bash
cd capstone
```

#### Car:
*Python script* - [`obd_comm.py`](https://github.com/dhruvweaver/12-traffic-light/blob/main/car/obd_comm.py): reads speed from car and transmits data over serial.

*Startup script* - [`startup.sh`](https://github.com/dhruvweaver/12-traffic-light/blob/main/car/startup.sh): script that runs the Python program at launch.
#### Testing:
*Reaction test* - Program for testing traffic light recognition speed while using full detection software.
#### Vision:
*Detect* - Contains [`detect_and_warn.py`](https://github.com/dhruvweaver/12-traffic-light/blob/main/vision/detect/distance_and_warn.py) script which implements full system integration.

*Quantize* - Contains scripts  and files necessary for quantization, pulled from Xilinx repositories.

*Training* - Directories containing training tools and training output.
## Getting Started:
***All READMEs are written with macOS and Linux in mind:***
For running the `detect_and_warn.py` script you will need to install the required Python libraries:
```bash
pip install -r requirements.txt
```

**Visit each section's directories for more instructions.**
