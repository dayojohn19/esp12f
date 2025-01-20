from mpy.text_recorder import TextRecorder
from configs.configs import clock_scl,clock_sda,clock_sqw,amAlarm,pmAlarm,servoPin,BatteryPin,rootpath
import time
import gc
def initialize_clock():

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


    def when_alarm():
        alarmrecord = TextRecorder('alarms.txt')
        alarmrecord.add(f'\n  Alarm Start...  \n')
        startServo =servorunner(servoPin)
        alarmrecord.add(startServo)
        try:
            alarmrecord.send()
            alarmrecord.add('Mesaage sent to cloud')
        except:
            alarmrecord.add('Failed to send to cloud')
        alarmrecord.save()
        # Add func that servo Run
        print('\n ALarmes \n')
        time.sleep(3)
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
        print( f'Clock initialized successfully')
        return clock
    except Exception as e:
        print( f"Error while initializing clock: {e}")
clock = initialize_clock()
gc.collect()




def start_esp():
    def try_import_with_timeout(module_name, timeout_minutes=1):
        start_time = time.time()
        retries = 0
        max_retries = 1
        while retries < max_retries:
            try:
                __import__(module_name)
                print(f"Successfully imported {module_name}")
                return True
            except ImportError as e:
                print("\n Reason: ",e)
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout_minutes * 60:
                    print(f"Timed out after {timeout_minutes} minutes, could not import {module_name}.")
                    return False
                retries += 1
                print(f"Failed to import {module_name}, retrying... (retries: {retries}) \n")
                time.sleep(2) 
    try_import_with_timeout('mpy.esp_start', 5)



start_esp()




import mpy.clear_import
import gc
gc.collect()
import machine
import time
from configs.configs import *
import network 

from mpy.text_recorder import TextRecorder


def initialize_clock():

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

    def when_alarm():
        alarmrecord = TextRecorder(logPath=rootpath,fpath='alarms.txt')
        alarmrecord.add(f'\n  Alarm Start...  \n')
        startServo =servorunner(servoPin)
        alarmrecord.add(startServo)
        try:
            alarmrecord.send()
            alarmrecord.add('Mesaage sent to cloud')
        except:
            alarmrecord.add('Failed to send to cloud')
        alarmrecord.save()
        # Add func that servo Run
        print('\n ALarmes \n')
        time.sleep(3)
    try:
        from mpy.main_clock import Clock
        clock = Clock(sqw_pin=clock_sqw, scl_pin=clock_scl, sda_pin=clock_sda, handler_alarm=when_alarm, i2c_freq=50000)  # Set I2C frequency to 50kHz to save energy
        gc.collect()
        # Enable 32kHz output
        clock.enable_32kHz_output(True)
        # Set SQW frequency to 1Hz to save energy
        # Set alarms
        clock.set_alarm_everyday(amAlarm[0], amAlarm[1])  # Set the first alarm for 7:30 AM
        clock.set_alarm2_everyday(pmAlarm[0], pmAlarm[1])  # Set the second alarm for 5:30 PM
        clock.i2c_freq=1
        print( f'Clock initialized successfully')
        return clock
    except Exception as e:
        print( f"                   Error while initializing clock: {e}")
clock = initialize_clock()
current_time = clock.get_time()
clockstamp = f"{current_time[0]} {current_time[1]}"

def read_battery(BatteryPin):
    def scale_value(value, min_val=490, max_val=690, new_min=0, new_max=100):
        return ((value - min_val) / (max_val - min_val)) * (new_max - new_min) + new_min
    adc = machine.ADC(BatteryPin)
    total = 0
    num_samples = 5
    for _ in range(num_samples):
        total += adc.read()
        time.sleep(0.01)
    average_value = total / num_samples
    return f'Reading: {average_value} ' # Raw Data

record = TextRecorder()
batval = read_battery(BatteryPin)
record.add(f'Starting...   Battery : {batval} \n')
record.save()


network.WLAN().active(True)
gc.collect()
print("Add func to reset devices every/after 24 hours")
