import time
import obd
import logging

# configure logging
#     filemode: "w" is overwrite, "a" is append
logging.basicConfig(level=logging.DEBUG, filename="obd_log.log", filemode="a", format="%(asctime)s : %(message)s")

speedData = [0] * 5
speedDiff = [0] * 4

# append and remove the current speed
def updateSpeed(currentSpeed):
    logging.debug(f"inside updateSpeed(), speed = {currentSpeed}") 
    speedData.pop(0)
    speedData.append(currentSpeed)

# calculate speed diff between the latest and oldest entries
def calcSpeedDiff():
    diff = speedData[4] - speedData[3]
    logging.debug(f"inside calcSpeedDiff(), speed difference: {diff}") 
    #update the speed diff list
    speedDiff.pop(0)
    speedDiff.append(diff)
    

# isBraking speed diff are negative to indicate slowing down
def checkBrakeStatus():
    logging.debug(f"inside checkBrakeStatus(), speedDiff = {speedDiff[3]}") 
    #for i in speedDiff:
     #   print(f"speedDiff[{i}] = {speedDiff[i]}")  | example of intended output: "speedDiff[2] = -20"
      #  if speedDiff[i] >= 0:
       #     return False
    if speedDiff[3] >= 0: # only isBraking most recent measurement
        return False
    else:
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
        logging.debug("Braking Status: Slowing Down") 
    else:
        logging.debug("Braking Status: Not Slowing Down") 
                
    # add a delay between queries to avoid overwhelming the OBD system
    time.sleep(0.5)
