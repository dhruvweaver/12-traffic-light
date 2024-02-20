import time
import obd
import RPi.GPIO as GPIO #install the GPIO Python Library

class brakeStatus:
    # create list to store speed value and diff
    def initV(self):
        self.speed = [0] * 5
        self.speedDiff = [0] * 4

    # append and remove the current speed
    def updateSpeed(self, currentSpeed):
        self.speed.append(currentSpeed)
        self.speed.pop(0)

    # calculate speed diff between the latest and oldest entries
    def calSpeedDiff(self):
        diff = self.speed[4] - self.speed[3]
        #update the speed diff list
        self.speedDiff.append(diff)
        self.speedDiff.pop(0)

    # check speed diff are negative to indicate slowing down
    def checkBrakeStatus(self):
        for i in self.speedDiff:
            if speedDiff[i] >= 0:
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
    GPIO.output(26, GPIO.HIGH)
    # wait time
    time.sleep(0.1)
    # create OBD connection and return list of valid USB
    portNum = obd.scan_serial()

    if portNum:
        # connect to the first port in the list
        connection = obd.OBD(portNum[0])
        if connection.is_connected():
            brake_status = brakeStatus()
            GPIO.output(17, GPIO.HIGH)
            
            while True:
                GPIO.output(18, GPIO.HIGH)  
                # send command and recieve response
                speedCmd = connection.query(obd.commands.SPEED)
                if not speedCmd.is_null():
                    speed = speedCmd.value.magnitude
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
                # add a delay between queries to avoid overwhelming the OBD system
                time.sleep(0.5)
        else:
            print("failed to established OBD connection")
    else:
        print("no valid USB ports found")

    GPIO.output(26, GPIO.LOW)