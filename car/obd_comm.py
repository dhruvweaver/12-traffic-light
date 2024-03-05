# lots of debugging print statements added
# ctrl-F for "debug" and delete them after no longer needed

import time
import obd
import RPi.GPIO as GPIO #install the GPIO Python Library

class brakeStatus:
    # create list to store speed value and diff
    def __init__(self):
        print("inside brakeStatus constructor") # debug
        self.speed = [0] * 5
        self.speedDiff = [0] * 4

    # append and remove the current speed
    def updateSpeed(self, currentSpeed):
        print("inside updateSpeed()") # debug
        self.speed.append(currentSpeed)
        self.speed.pop(0)

    # calculate speed diff between the latest and oldest entries
    def calSpeedDiff(self):
        print("inside calSpeedDiff()") # debug
        diff = self.speed[4] - self.speed[3]
        print(f"speed difference: {diff}") # debug
        #update the speed diff list
        self.speedDiff.append(diff)
        self.speedDiff.pop(0)

    # check speed diff are negative to indicate slowing down
    def checkBrakeStatus(self):
        print("inside checkBrakeStatus()")
        for i in self.speedDiff:
            print(f"speedDiff[{i}] = {self.speedDiff[i]}") # debug | example of intended output: "speedDiff[2] = -20"
            if self.speedDiff[i] >= 0:
                return False
        return True
   
# setup LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14, GPIO.OUT)  # acceleration LED
GPIO.setup(15, GPIO.OUT)  # braking LED
GPIO.setup(17, GPIO.OUT)  # connection OK LED
GPIO.setup(18, GPIO.OUT)  # getting speed measurements LED
GPIO.setup(27, GPIO.OUT)  # Check for programing is running 

while True:
    print("inside while(True)") # debug
    GPIO.output(27, GPIO.HIGH) # turn on running light
    # create OBD connection and return list of valid USB
    portNum = obd.scan_serial()
    print(f"number of ports found: {len(portNum)}") # debug

    if len(portNum) > 0: # if any ports exist in the list
        print("inside if len(portNum)") # debug
        # connect to the first port in the list
        connection = obd.OBD(portNum[0])
        brake_status = brakeStatus() # create new brakeStatus object
        print(f"break status: {bool(brake_status)}") # debug

        print(f"status of connection: {connection.is_connected()}") # debug
        while connection.is_connected():
            print("inside while connection.is_connected()") # debug
            GPIO.output(17, GPIO.HIGH) # turn on connection LED
            # send command and recieve response
            speedCmd = connection.query(obd.commands.SPEED)
            print(f"status of speedCmd.is_null(): {speedCmd.is_null()}") # debug
            if not speedCmd.is_null():
                GPIO.output(18, GPIO.HIGH)  # turn on speed LED if speed data received
                speed = speedCmd.value.to("mph").magnitude
                print(f"Driving speed: {speed} mile/h ")
                
                # update brake status with the current speed and speed diff
                brake_status.updateSpeed(speed)
                brake_status.calSpeedDiff()

                # check and print
                check = brake_status.checkBrakeStatus()
                if check:
                    print("Braking Status: Slowing Down")
                    GPIO.output(15, GPIO.HIGH)  # turn on brake LED
                    GPIO.output(14, GPIO.LOW)   # turn off acceleration LED
                else:
                    print("Braking Status: Not Slowing Down")
                    GPIO.output(14, GPIO.HIGH)  # turn on acceleration LED
                    GPIO.output(15, GPIO.LOW)   #turn off brake LED
            else:
                print("Speed data not received")
                GPIO.output(18, GPIO.LOW) # turn off speed LED
                
            # add a delay between queries to avoid overwhelming the OBD system
            time.sleep(0.1)
                
        print("Failed to establish OBD connection")
        GPIO.output(17, GPIO.LOW) # turn off connection LED
    else:
        print("no valid USB ports found")

    GPIO.output(27, GPIO.LOW) # turn off LED for a moment to create blinking effect
    time.sleep(0.5) # sleep a small amount of time so blinking is visible
