# Testing
This directory is for the testing software developed for this project.

The sub-directory `reaction-test` contains the only software test program developed to this point.

## Getting started:
The reaction test uses operating system signals to communicate between the
testing program and the detection program.

The testing program sequentially displays a user-specified number of traffic light images.
When an image is presented the testing program waits for the detection software
to send a signal indicating that a light has been detected.
Then the detection program is paused until right before the next image is shown.

The process is repeated for all images.

### Build the program:
The test program is written in C and invokes Preview or EOG on macOS and Linux,
respectively to show the images. The directory already contains the executable
but if you need to rebuild it, a Makefile is provided:

```bash
make
```

## Running reaction test
```bash
./reaction-test.o 4
```
The argument `4` tells the program to show a sequence of four images.

Once the test program is running, start the detection program in another terminal:
```bash
python yolo-reaction.py
```
Point the camera towards the display and press return or enter in the first
terminal to continue begin the testing sequence.
