import machine
import time
from mpy.led_signal import *
start_blinking(100)
led = machine.Pin(2, machine.Pin.OUT)
import time
import gc
gc.collect()
try:
    import mpy.networkconfig
    import mpy.ota_git
except Exception as e:
    print("ERROR IMPORTING ota_git ",e)
    time.sleep(1)

# import lcd
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
    clock.set_sqw_frequency(1)

    # Set alarms
    clock.set_alarm_everyday(7, 30)  # Set the first alarm for 7:30 AM
    clock.set_alarm2_everyday(17, 30)  # Set the second alarm for 5:30 PM

    return clock

clock = initialize_clock()

# Get the current date and time
current_time = clock.get_time()
print(f"Current Date: {current_time[0]}")
print(f"Current Time: {current_time[1]}")
