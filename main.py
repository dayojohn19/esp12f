import machine
import time
from mpy.led_signal import *
start_blinking(100)
# Create a Pin object for the LED (D4 -> GPIO2)
led = machine.Pin(2, machine.Pin.OUT)
import time
import gc
gc.collect()
try:
    import mpy.ota_git
except Exception as e:
    print("ERROR IMPORTING ota_git ",e)
    import mpy.networkconfig

# import lcd
import gc
gc.collect()
files_to_update=["main.py","configs/listnames.txt","configs/esp12settings.json",'test3.txt','test4.txt','test5.txt','clock']
giturl= "https://github.com/dayojohn19/esp12f/"


print("get try versioning 111 for v8")
print('Added in git')

# scl = 14  # GPIO14 (D5)
# sda = 13  # GPIO13 (D7)
# i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)

# SQW and 32kHz pins
sqw = 2  # GPIO4 (D2)
k32 = 14  # GPIO5 (D1)

from clockconfig import ClockConfig
clock_config = ClockConfig(sqw_pin=2, scl_pin=5, sda_pin=4, k32_pin=13, i2c_freq=50000)  # Set I2C frequency to 50kHz to save energy
# Enable 32kHz output
clock_config.enable_32kHz_output(True)

# Set SQW frequency to 1Hz to save energy
clock_config.set_sqw_frequency(1)

# Set alarms
clock_config.set_alarm_everyday(7, 30)  # Set the first alarm for 7:30 AM
clock_config.set_alarm2_everyday(17, 30)  # Set the second alarm for 5:30 PM

# Get the current date and time
current_time = clock_config.get_time()
print(f"Current Date: {current_time[0]}")
print(f"Current Time: {current_time[1]}")
