import time
import obd
import logging

logging.basicConfig(level=logging.DEBUG, filename="obd_log.log", filemode="a", format="%(asctime)s : %(message)s")

ports = obd.scan_serial()
connection = obd.OBD(ports[0])
cmd = obd.commands.SPEED

logging.debug(f"number of ports found: {len(ports)}")
logging.debug(f"status of connection: {connection.is_connected()}")

while True:
  response = connection.query(cmd)
  speed = response.value.to("mph").magnitude
  logging.debug(f"Driving speed: {speed} mile/h")
  time.sleep(0.5)
