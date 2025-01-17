import time
from machine import Pin

# Define GPIO pin for reading RX
rx_pin = Pin(14, Pin.IN)  # Set RX pin (change pin number as needed)
baud_rate = 9600
bit_time = 1 / baud_rate

def read_bit():
    return rx_pin.value()

def read_byte():
    byte = 0
    for i in range(8):
        byte |= (read_bit() << i)
        time.sleep(bit_time)
    return byte

def read_data():
    while True:
        # Wait for start bit (low signal)
        while read_bit() != 0:
            pass
        # Read one byte of data
        byte = read_byte()
        print("Received byte:", byte)

# Call read_data in a loop
# read_data()