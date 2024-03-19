import time
import obd
import logging

# configure logging
#     filemode: "w" is overwrite, "a" is append
logging.basicConfig(level=logging.DEBUG, filename="obd_log.log", filemode="a", format="%(asctime)s : %(message)s")

class brakeStatus:
    # create list to store speed value and diff
    def __init__(self):
        logging.debug("inside brakeStatus constructor") 
        self.speedData = [0] * 5
        self.speedDiff = [0] * 4

    # append and remove the current speed
    def updateSpeed(self, currentSpeed):
        logging.debug(f"inside updateSpeed(), speed = {currentSpeed}") 
        self.speedData.append(currentSpeed)
        self.speedData.pop(0)

    # calculate speed diff between the latest and oldest entries
    def calcSpeedDiff(self):
        diff = self.speedData[4] - self.speedData[3]
        logging.debug(f"inside calcSpeedDiff(), speed difference: {diff}") 
        #update the speed diff list
        self.speedDiff.append(diff)
        self.speedDiff.pop(0)

    # isBraking speed diff are negative to indicate slowing down
    def checkBrakeStatus(self):
        logging.debug(f"inside checkBrakeStatus(), speedDiff = {self.speedDiff[4]}") 
        #for i in self.speedDiff:
         #   print(f"speedDiff[{i}] = {self.speedDiff[i]}")  | example of intended output: "speedDiff[2] = -20"
          #  if self.speedDiff[i] >= 0:
           #     return False
        if self.speedDiff[3] >= 0: # only isBraking most recent measurement
            return False
        else:
            return True

ports = obd.scan_serial()
connection = obd.OBD(ports[0])
cmd = obd.commands.SPEED

logging.debug(f"number of ports found: {len(ports)}")

brake_status = brakeStatus() # create new brakeStatus object

while True:    
    # send command and recieve response
    response = connection.query(obd.commands.SPEED)
    speed = response.value.to("mph").magnitude
    logging.debug(f"Driving speed: {speed} mile/h") 
                
    # update brake status with the current speed and speed diff
    brake_status.updateSpeed(speed)
    brake_status.calcSpeedDiff()

    # isBraking and print
    isBraking = brake_status.checkBrakeStatus()
    
    if isBraking:
        logging.debug("Braking Status: Slowing Down") 
    else:
        logging.debug("Braking Status: Not Slowing Down") 
                
    # add a delay between queries to avoid overwhelming the OBD system
    time.sleep(0.5)
