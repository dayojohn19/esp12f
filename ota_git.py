from ota import OTAUpdater
# from WIFI_CONFIG import SSID, PASSWORD
import json
import time
from led_signal import *

start_blinking(50)
print("Do you want to update?")
for i in range(6):
    print('     Updating in ',i)
    time.sleep(1)
with open('configs/wifiSettings.json') as f:
    config = json.load(f)
    SSID = config['ssid']
    PASSWORD = config['ssid_password']

firmware_url = "https://github.com/dayojohn19/esp12f/"

# ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "test.text")

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
ota_updater.download_and_install_update_if_available()

stop_blinking()