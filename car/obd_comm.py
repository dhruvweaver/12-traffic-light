import time
import obd


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
        diff = self.speed[4] - self.speed[0]
        # update the speed diff list
        self.speedDiff.append(diff)
        self.speedDiff.pop(0)

    # check speed diff are negative to indicate slowing down
    def checkBrakeStatus(self):
        for i in self.speedDiff:
            if i >= 0:
                return False
        return True


# wait time
time.sleep(0.1)
# create OBD connection and return list of valid USB
portNum = obd.scan_serial()

if portNum:
    # connect to the first port in the list
    connection = obd.OBD(portNum[0])
    if connection.is_connected():
        brake_status = brakeStatus()

        while True:
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
                else:
                    print("Braking Status: Not Slowing Down")
            # add a delay between queries to avoid overwhelming the OBD system
            time.sleep(0.5)
    else:
        print("failed to established OBD connection")
else:
    print("no valid USB ports found")
