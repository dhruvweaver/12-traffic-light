import obd

ports = obd.scan_serial()
print(f"number of ports found: {len(ports)}")
print(ports)
