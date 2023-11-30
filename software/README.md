# Team 12 Capstone Project: Traffic Light Detection
Central repository for the traffic light detection capstone project.

### Table of Contents

[Getting started](https://github.com/dhruvweaver/12-traffic-light#getting-started)
    
[Training YOLOv3](https://github.com/dhruvweaver/12-traffic-light#training-yolov3)

[Running YOLOv3](https://github.com/dhruvweaver/12-traffic-light#running-yolov3-model)

_[Running YOLOv5 Demo](https://github.com/dhruvweaver/12-traffic-light#instructions-for-running-yolov5-model-for-demo-only) (legacy)_

## Getting started:
To begin working you will need to clone this repository.
Choose a directory you would like to work in (such as a 'development' directory).

Then clone the repository into that directory.
***You can also rename the repo to something more simple when you clone it, as shown:***
```bash
[foo@bar]$ cd development
[foo@bar]$ git clone https://github.com/dhruvweaver/12-traffic-light.git capstone
```

You now have a local copy of the repo on your computer. Go to that directory:
```bash
[foo@bar]$ cd capstone
```

### Set up miniconda environment:
A conda environment allows you to install packages to your dev environment in a self contained space.
This means that packages installed in your conda environment won't affect your other dependencies.

***Install on [Linux](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html)***

***Install on macOS:***

Make sure [Homebrew](https://brew.sh/) is installed.
```zsh
foo@bar ~ % brew install miniconda
```
_Note:_
On macOS, after installing miniconda via Homebrew, add the following to your .zshrc file
```zsh
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/homebrew/Caskroom/miniconda/base/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh" ]; then
        . "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh"
    else
        export PATH="/opt/homebrew/Caskroom/miniconda/base/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
```

(Optional) Disable conda by default:
```bash
[foo@bar]$ conda config --set auto_activate_base false
```

***Restart your terminal.***

Activate conda environment:
```bash
[foo@bar]$ conda activate
```

When your conda environment is active, your terminal prompt will look something like:
```bash
(base)[foo@bar]$
```
## Custom Data Set (Traffic light Detection for only red and yellow lights):
Used Roboflow to collect images and labels. It(version 9) contains 2065 images of red and yellow light. Download this dataset to train Yolo.
<a href="https://universe.roboflow.com/traffic-light-detection-qsrxn/traffic-light-oq7uj">
    <img src="https://app.roboflow.com/images/download-dataset-badge.svg"></img>
</a>

## Training YOLOv3:
Visit source GitHub page for more: https://github.com/ultralytics/yolov3

Open directory
```bash
[foo@bar]$ cd yolov3-ultralytics
```

***Make sure you are in your conda environment***

Install requirements:
```bash
[foo@bar]$ pip install -r requirements.txt
```

Open Jupyter Notebook/Lab
```bash
[foo@bar]$ jupyter notebook
```
_or_
```bash
[foo@bar]$ jupyter lab
```

The Jupyter app should launch in your browser, and from there you can open the file:

_traffic_light_train.ipynb_

The notebook contains code that will download the dataset as well as train the model.

**Training without a powerful GPU (especially without CUDA) will be pretty slow, especially at high epochs.**

## Running YOLOv3 model:
After the model is trained, place the results in the 'vision-prototype' directory.

To test the model, run the following command within the 'yolov3-ultralytics' directory:
```bash
[foo@bar]$ python3 detect.py --weights "../vision-prototype/exp5/weights/best.pt" --source 0
```
## Changing weight file(.pt) to .pb 

Run the following command to change .pt file(Pytorch) to .pb file(TensorFlow GraphDef)
```bash
[foo@bar]$ python3 export.py --weights "../vision-prototype/custom-train/weights/best.pt" --include pb

```

## Instructions for running YOLOv5 model (for demo only, directory archived):
Install the following pip dependencies:

torch, numpy, ultralytics

Open 'Testing.ipynb' in Jupyter Notebook/Lab.

Scroll to the line that reads:
```Python
!python3 detect.py --weights "./runs/train/epoch70/weights/best.pt" --source 0
```
Run this line.


