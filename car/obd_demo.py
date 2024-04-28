import time
#import obd
#import logging
import serial
import random

# configure logging
#     filemode: "w" is overwrite, "a" is append
#logging.basicConfig(level=logging.DEBUG, filename="/home/team12/obd_log.log", filemode="a", format="%(asctime)s : %(message)s")

#configure the serial port
ser = serial.Serial("/dev/ttyS0", 9600)

speedData = [0] * 5
speedDiff = [0] * 3
speed = 50

# remove oldest speed from array, add current speed
def updateSpeed(currentSpeed):
    #logging.debug(f"inside updateSpeed(), speed = {currentSpeed}") 
    speedData.pop(0)
    speedData.append(currentSpeed)

# calculate speed difference between latest two measurements
# remove oldest difference from array, add current
def calcSpeedDiff():
    diff = speedData[len(speedData)-1] - speedData[len(speedData)-2]
    #logging.debug(f"inside calcSpeedDiff(), speed difference: {diff}") 
    speedDiff.pop(0)
    speedDiff.append(diff)

def randomSpeed(prevSpeed):
    if random.randint(0,1) == 0:
        return prevSpeed - 5*random.random()
    else:
        return prevSpeed + 5*random.random()
    

# check if vehicle is braking over multiple measurements
# return true if stopped
# return false if any speed differences in array are positive
# return true otherwise
def checkBrakeStatus():
    #logging.debug("inside checkBrakeStatus()") 
    for i in speedDiff:
        #logging.debug(f"speedDiff = {i}")
        if speedData[len(speedData)-1] == 0: # stopped counts as braking
            return True
        elif i >= 0: # accelerating and constant speed are not braking
            return False
    return True # if execution made it this far without returning, it must be braking

#logging.debug("------------------ start of new session ------------------")

# find port of OBD adapter and connect to it
#ports = obd.scan_serial()
#logging.debug(f"number of ports found: {len(ports)}")
#logging.debug(f"ports: {ports}")
#connection = obd.OBD(ports[0])
# connection = obd.OBD() # autoconnect

# prepare the command to query speed
#cmd = obd.commands.SPEED

while True:    
    # send command and recieve response
    #response = connection.query(obd.commands.SPEED)
    speed = randomSpeed(speed)
    if speed < 0:
        speed = 0
    #logging.debug(f"Driving speed: {speed} mile/h") 
                
    # update current speed and speed difference
    updateSpeed(speed)
    calcSpeedDiff()

    # determine whether vehicle is braking
    isBraking = checkBrakeStatus()

    if isBraking:
        #logging.debug("Status: Braking ***********************") 
        sendData = f"B {speed:07.3f}\r\n"
        print(sendData)
        ser.write(bytes(sendData,'utf-8'))
    else:
        #logging.debug("Status: Accelerating")
        sendData = f"A {speed:07.3f}\r\n"
        print(sendData)
        ser.write(bytes(sendData,'utf-8'))
                
    # add a delay between queries to avoid overwhelming the OBD system
    time.sleep(0.5)
