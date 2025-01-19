import time
time.sleep(3)
print("Main Starting in 3 v1")
print("Main Starting in 3 v1")
print("Main Starting in 3 v2")
time.sleep(3)
def try_import_with_timeout(module_name, timeout_minutes=1):
    start_time = time.time()
    retries = 0
    max_retries = 1
    while retries < max_retries:
        try:
            __import__(module_name)
            print(f"Successfully imported {module_name}")
            return True
        except ImportError:
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout_minutes * 60:
                print(f"Timed out after {timeout_minutes} minutes, could not import {module_name}.")
                return False
            retries += 1
            print(f"Failed to import {module_name}, retrying... (retries: {retries}) \n")
            time.sleep(2) 
    return False


def dynamic_import(file_name, class_name):
    with open(file_name, 'r') as f:
        code = f.read()

    # Execute the code to define the class in the current namespace
    exec(code)

    # Now, `class_name` is a valid class, so we can instantiate it
    if class_name in globals():
        class_obj = globals()[class_name]
        return class_obj
    else:
        raise ValueError(f"Class {class_name} not found in {file_name}")


def start_esp():
    try_import_with_timeout('mpy.esp_start', 5)
start_esp()




import sys

def clear_all_imported_modules():
    # List of modules to ignore, like '__main__', 'sys', etc.
    ignore_modules = {'sys', '__main__', 'builtins'}

    # Iterate over all modules in sys.modules
    for module in list(sys.modules.keys()):
        if module not in ignore_modules:
            del sys.modules[module]  # Remove the module from the cache

    # Optionally, also delete references in the global namespace if needed
    for module in list(globals().keys()):
        if module not in ignore_modules:
            del globals()[module]

import gc
gc.collect()
# import lcd
import machine
import time
from configs.configs import *
def initialize_clock():
    try:
        from mpy.main_clock import Clock
        clock = Clock(sqw_pin=clock_sqw, scl_pin=clock_scl, sda_pin=clock_sda, handler_alarm=when_alarm, i2c_freq=50000)  # Set I2C frequency to 50kHz to save energy
        gc.collect()
        # Enable 32kHz output
        clock.enable_32kHz_output(True)
        # Set SQW frequency to 1Hz to save energy
        clock.i2c_freq=1
        # Set alarms
        clock.set_alarm_everyday(amAlarm[0], amAlarm[1])  # Set the first alarm for 7:30 AM
        clock.set_alarm2_everyday(pmAlarm[0], pmAlarm[1])  # Set the second alarm for 5:30 PM
        record.add( f'Clock initialized successfully')
        return clock
    except Exception as e:
        record.add( f"Error while initializing clock: {e}")
clock = initialize_clock()
current_time = clock.get_time()
clockstamp = f"{current_time[0]} {current_time[1]}"

def read_battery(BatteryPin):
    def scale_value(value, min_val=490, max_val=690, new_min=0, new_max=100):
        return ((value - min_val) / (max_val - min_val)) * (new_max - new_min) + new_min
    total = 0
    num_samples = 5
    for _ in range(num_samples):
        total += adc.read()
        time.sleep(0.01)
    average_value = total / num_samples
    adc = machine.ADC(BatteryPin)
    return f'Reading: {average_value} ' # Raw Data

def servorunner(ServoPin, runTimes=1):
    machine.Pin(ServoPin)
    servo = machine.PWM(ServoPin)
    max_duty = 7864
    min_duty = 1802
    half_duty = int(max_duty/2)
    frequency = 500
    def runServo(times=1):
        for i in range(int(times)):
            x = 500
            while x <=4000:
                x+=30
                servo.duty_u16(x)
                print(x)
                time.sleep(0.01)
            time.sleep(5)
        servo.deinit()
        led = machine.Pin(2, machine.Pin.OUT)
        led.value(1)
    runServo(runTimes)
    return '\nMotor Run Successfully'


class Text_Recorder:
    def __init__(self, fpath='records.txt'):
        self.text = ''
        self.path = logPath+fpath

    def add(self,text):
        self.text += '  ',text,'  '
        print('Adding to record: ',text)

    def save(self):
        print("Recording...")
        with open(self.path, 'a') as file:
            file.write(self.text + machine.RTC().datetime())
            file.write('\n')    

    def send(self):
        try:
            print('Trying to send...')
            messenger = dynamic_import('mpy/network_messenger.py', 'Sim')
            wmg = messenger.sendWhatsapp(message = self.text)
            self.add(wmg)
            del messenger
            gc.collect()
        except:
            self.add('Failed to connect to send record ')
        print("Recorded")

record = Text_Recorder()
record.add(f'Starting... \n {clockstamp}    Battery : {read_battery(BatteryPin)} \n')

def when_alarm():
    alarmrecord = Text_Recorder('alarms.txt')
    newtime = clock.getTime()
    alarmrecord.add(f'\n  Alarm Start...{newtime[0]} {newtime[1]}  \n')
    alarmrecord.add(servorunner(servoPin))
    alarmrecord.save()
    alarmrecord.save_to_cloud()
    # Add func that servo Run
    print('\n ALarmes \n')
    time.sleep(3)


