from machine import Pin, I2C, ADC

# Servo control pin
servo = 12  # GPIO12 (D6)

# I2C configuration
scl = 14  # GPIO14 (D5)
sda = 13  # GPIO13 (D7)
i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)

# SQW and 32kHz pins
sqw = 4  # GPIO4 (D2)
k32 = 5  # GPIO5 (D1)

# Analog read pin
analog_pin = ADC(0)  # ADC0