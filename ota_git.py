from mpy.ota import OTAUpdater
# from WIFI_CONFIG import SSID, PASSWORD
import json
import time
from mpy.led_signal import *

start_blinking(50)
print("Do you want to update?")
for i in range(6):
    print('     Updating in ',i)
    time.sleep(1)
with open('configs/wifiSettings.json') as f:
    config = json.load(f)
    SSID = config['ssid']
    PASSWORD = config['ssid_password']

# with open('configs/esp12settings.json') as f:
#     config = json.load(f)
#     giturl = config['giturl']
#     files   = config['files']
#     stop_blinking()
#     firmware_url = giturl
#     for file in files:
#         print(f"updating: ",{file})
#         led.value(0)
#         ota_updater = OTAUpdater(SSID,PASSWORD,firmware_url,file)
#         ota_updater.download_and_install_update_if_available()
#         led.value(1)
#         time.sleep(3)
from main import files_to_update, giturl
for file in files_to_update:
    print(f'updating {file} ')
    led.value(0)
    ota_updater = OTAUpdater(SSID,PASSWORD,giturl,file)
    ota_updater.download_and_install_update_if_available()    
    led.value(1)
    time.sleep(3)


led.value(1)
time.sleep(5)

# ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "test.text")


# stop_blinking()