from ota import OTAUpdater
# from WIFI_CONFIG import SSID, PASSWORD
import json

with open('configs/wifiSettings.json') as f:
    config = json.load(f)
    SSID = config['ssid']
    PASSWORD = config['ssid_password']
firmware_url = "https://github.com/dayojohn19/ota_test/main/"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "test_ota.py")

ota_updater.download_and_install_update_if_available()