from machine import Pin, I2C, RTC 
import clock
import time


class ClockConfig:
    def __init__(self, sqw_pin=13, scl_pin=14, sda_pin=12, k32_pin=15, i2c_freq=100000):
        from machine import RTC
        self.clock_sqw = sqw_pin  # D7
        self.clock_scl = scl_pin  # D5
        self.clock_sda = sda_pin  # D6
        self.clock_k32 = k32_pin  # D8
        self.clock_i2c = I2C(scl=Pin(self.clock_scl), sda=Pin(self.clock_sda), freq=i2c_freq)  # Example with GPIO14 and GPIO12 SDA=D6 SCL=D5
        self.clockmodule = clock.DS3231(self.clock_i2c)
        self.rtc = RTC()
        self.setup_pins()
        self.sync_rtc_with_ds3231()

    def sync_rtc_with_ds3231(self):
        print('Syncing RTC with DS3231')
        time.sleep(3)  # Wait for the RTC to stabilize
        self.rtc.datetime(self.clockmodule.datetime())

    def get_time(self):
        date = "{}/{}/{}".format(self.rtc.datetime()[1], self.rtc.datetime()[2], self.rtc.datetime()[0])
        time = "{}:{}:{}".format(self.rtc.datetime()[4], self.rtc.datetime()[5], self.rtc.datetime()[6])
        return [date, time]


    def setup_pins(self):
        self.sqw_pin = Pin(self.clock_sqw, Pin.IN, Pin.PULL_UP)
        # self.k32_pin = Pin(self.clock_k32, Pin.IN, Pin.PULL_UP)
        self.sqw_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.alarm_handler)
        # self.k32_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.alarm_handler2)

    def enable_32kHz_output(self, enable=False):
        self.clockmodule.output_32kHz(enable)

    def alarm_handler(self, pin):
        print("SQW Interrupt Triggered by PIN:", pin)
        self.clockmodule.check_alarm(1)
        print(self.clockmodule.datetime())
        print('\n')

    def alarm_handler2(self, pin):
        print("32kHz Interrupt Triggered by PIN:", pin)
        self.clockmodule.check_alarm(2)
        print(self.clockmodule.datetime())
        print('\n')

    def set_alarm_everyday(self, hrs, min, sec=0):
        self.clockmodule.alarm1((sec, min, hrs), match=self.clockmodule.AL1_MATCH_HMS)
        print(f"Alarm Set for {hrs}h : {min}m : {sec}s")

    def set_alarm2_everyday(self, hrs=1, min=1, day=1):
        self.clockmodule.alarm2((min, hrs, day), match=self.clockmodule.AL2_MATCH_HM)
        print(f"Everyday Alarm {hrs} : {min}m")

# Example usage
if __name__ == "__main__":
    clock_config = ClockConfig(i2c_freq=50000) # set to 50000 to save energy
    clock_config.enable_32kHz_output(True)
    clock_config.set_alarm_everyday(7, 30)  # Set the first alarm for 7:30 AM
    clock_config.set_alarm2_everyday(17, 30)