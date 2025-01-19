
import time

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


def start_esp():
    print("Starting ESP")
    from mpy.led_signal import led
    led.value(0)
    try_import_with_timeout('mpy.networkconfig', 5)
    import gc
    gc.collect()
    try_import_with_timeout('mpy.ota_git', 1)
start_esp()

# import time




# import lcd
import machine
import time
import gc
gc.collect()

def when_alarm():
    print('\n ALarmes \n')
    time.sleep(3)
from configs.configs import *

def initialize_clock():
    from clockconfig import ClockConfig
    clock = ClockConfig(sqw_pin=clock_sqw, scl_pin=clock_scl, sda_pin=clock_sda, handler_alarm=when_alarm, i2c_freq=50000)  # Set I2C frequency to 50kHz to save energy
    # Enable 32kHz output
    clock.enable_32kHz_output(True)

    # Set SQW frequency to 1Hz to save energy
    clock.i2c_freq(1)

    # Set alarms
    clock.set_alarm_everyday(7, 30)  # Set the first alarm for 7:30 AM
    clock.set_alarm2_everyday(17, 30)  # Set the second alarm for 5:30 PM

    return clock

clock = initialize_clock()

# Get the current date and time
current_time = clock.get_time()
print(f"Current Date: {current_time[0]}")
print(f"Current Time: {current_time[1]}")
