import time
import obd
import logging

# configure logging
#     filemode: "w" is overwrite, "a" is append
logging.basicConfig(level=logging.DEBUG, filename="obd_log.log", filemode="a", format="%(asctime)s : %(message)s")

speedData = [0] * 5
speedDiff = [0] * 3

# append and remove the current speed
def updateSpeed(currentSpeed):
    logging.debug(f"inside updateSpeed(), speed = {currentSpeed}") 
    speedData.pop(0)
    speedData.append(currentSpeed)

# calculate speed diff between the latest and oldest entries
def calcSpeedDiff():
    diff = speedData[len(speedData)-1] - speedData[len(speedData)-2]
    logging.debug(f"inside calcSpeedDiff(), speed difference: {diff}") 
    #update the speed diff list
    speedDiff.pop(0)
    speedDiff.append(diff)
    

# isBraking speed diff are negative to indicate slowing down
def checkBrakeStatus():
    logging.debug("inside checkBrakeStatus()") 
    for i in speedDiff:
        logging.debug(f"speedDiff = {i}")
        if speedData[len(speedData)-1] == 0: # stopped counts as braking
            return True
        elif i >= 0: # if any of the measurements in the speedDiff array are positive, it's not braking
            return False
    return True

ports = obd.scan_serial()
connection = obd.OBD(ports[0])
cmd = obd.commands.SPEED

logging.debug(f"number of ports found: {len(ports)}")

while True:    
    # send command and recieve response
    response = connection.query(obd.commands.SPEED)
    speed = response.value.to("mph").magnitude
    logging.debug(f"Driving speed: {speed} mile/h") 
                
    # update brake status with the current speed and speed diff
    updateSpeed(speed)
    calcSpeedDiff()

    # isBraking and print
    isBraking = checkBrakeStatus()
    
    if isBraking:
        logging.debug("Status: Braking ***********************") 
    else:
        logging.debug("Status: Accelerating") 
                
    # add a delay between queries to avoid overwhelming the OBD system
    time.sleep(0.5)
