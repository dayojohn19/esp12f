
# NFC READER
import machine
import time

import time
import ubinascii
import struct
SPI_SCK = 18  # SPI Clock (SCK)
SPI_MISO = 19  # Master In Slave Out (MISO)
SPI_MOSI = 23  # Master Out Slave In (MOSI)
SPI_CS = 5  # Chip Select (CS)

# SPI configuration (using SPI(1) here)
# spi = machine.SPI(1, baudrate=5000000, polarity=1, phase=1, sck=machine.Pin(SPI_SCK), miso=machine.Pin(SPI_MISO), mosi=machine.Pin(SPI_MOSI))
# spi = machine.SPI(1, baudrate=5000000, polarity=1, phase=1, sck=machine.Pin(SPI_SCK), miso=machine.Pin(SPI_MISO), mosi=machine.Pin(SPI_MOSI))
spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0, sck=machine.Pin(SPI_SCK), miso=machine.Pin(SPI_MISO), mosi=machine.Pin(SPI_MOSI))
# Set up CS pin as an output (Chip Select)
cs = machine.Pin(SPI_CS, machine.Pin.OUT)
# Chip Select (CS) Pin

# Set up CS pin as an output (Chip Select)

cs.value(1)  # Initially deselect the PN532 (set CS HIGH)

# Define function to send command and read response
def send_command(command):
    # Activate PN532 by pulling CS low
    cs.value(0)
    # Send command over SPI
    spi.write(command)
    # Wait a bit for the response
    time.sleep(0.1)
    # Deactivate PN532 by pulling CS high
    cs.value(1)


# Function to read data (with timeout protection)
def read_data(length):
    cs.value(0)  # Select the PN532 by pulling CS low
    response = spi.read(length)  # Read response from PN532
    cs.value(1)  # Deselect the PN532 by pulling CS high
    return response

# Helper function to read the version of the PN532 (as a test)
def get_version():
    # Command to request PN532 version (example command)
    command = b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    send_command(command)
    response = read_data(12)  # Expecting 12 bytes as response
    print("Response:", ubinascii.hexlify(response))

# Function to scan for NFC tags (basic scan)
def scan_for_tags():
    # Command to start passive scanning (example command for tag detection)
    command = b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    send_command(command)
    response = read_data(12)  # Expecting 12 bytes for tag read
    return response
print("Initializing PN532...")

def get_version():
    command = b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    i2c.writeto(0x48, command)  # PN532 I2C address is usually 0x48
    time.sleep(0.1)
    response = i2c.readfrom(0x48, 12)
    print(f"Response: {ubinascii.hexlify(response)}")

output = i2c.scan()
get_version()
print(output, output)


while True:
    tag_data = scan_for_tags()
    if tag_data:
        print("NFC Tag Detected!")
        print(f"Tag Data (Hex): {ubinascii.hexlify(tag_data)}")
    else:
        print("No tag detected. Scanning again...")
    time.sleep(1)  # Delay before scanning again
