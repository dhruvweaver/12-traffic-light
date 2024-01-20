import time
import obd


# wait time
time.sleep(0.1)
# create OBD connection and return list of valid USB
portNum = obd.scan_serial()

if portNum:
    # connect to the first port in the list
    connection = obd.OBD(portNum[0])
    if connection.is_connected():
        while True:
            # send command and recieve response
            speedCmd = connection.query(obd.commands.SPEED_MPG)
            if not speedCmd.is_null():
                speed = speedCmd.value.magnitude
                print(f"Driving speed: {speed} mile/h ")
            # add a delay between queries to avoid overwhelming the OBD system
            time.sleep(0.5)
    else:
        print("failed to established OBD connection")
else:
    print("no valid USB ports found")
