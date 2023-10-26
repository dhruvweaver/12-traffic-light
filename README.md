Central repository for the traffic light detection capstone project.

## Instructions for running YOLO V5 model:
Install Miniconda, Python, and any pip dependencies.
***Note:***
**On macOS, after installing miniconda via Homebrew, add the following to your .zshrc file**
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

Open 'Testing.ipynb' in Jupyter Notebook/Lab.

Scroll to the line that reads:
```Python
!python3 detect.py --weights "./runs/train/epoch70/weights/best.pt" --source 0
```
Run this line.

## For training YOLO V3:
***(Training instructions unfinished)***

Follow instructions to add weights and training files (darknet53.conv.74):
https://pjreddie.com/darknet/yolo/

**To use CUDA change GPU config in Makefile**

Inside of the 'yolov3' directory
```bash
make
```

