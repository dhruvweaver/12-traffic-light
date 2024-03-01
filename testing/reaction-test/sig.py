import os
import signal
import psutil


# funciton to find pid of running process by name
def get_pid(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            return proc.info['pid']
    return None


running = False
# get pid of test program
pid = get_pid('reaction-test.o')
if pid is not None:
    running = True
    print(f'Found process with PID: {pid}')
else:
    print('Process not found')

while running:
    if input('Press the ENTER/RETURN to send a signal\n') == '':
        os.kill(pid, signal.SIGUSR1)

    # keep checking for test program running
    pid = get_pid('reaction-test.o')
    if pid is not None:
        running = True
    else:
        print('Test complete')
        break
