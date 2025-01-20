def setup_webrepl():
    import webrepl
    import network 
    from machine import Pin
    import time
    import json
    with open('configs/wifiSettings.json') as f:
        config = json.load(f)
        wifiSSID = config['ssid']
        wifiPassword = config['ssid_password']
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifiSSID, wifiPassword)
    for i in range(3):
        print(i,'Connecting to ',wifiSSID)
        time.sleep(1)
    wlan.ifconfig()
    wap = network.WLAN(network.AP_IF)
    wap.active(False)
    if wlan.isconnected():
        print("Connected to wifi ")
    elif not wlan.isconnected():
        print("Hotspot setting up")
        led_builtin =Pin(2, Pin.OUT)
        led_builtin.off()
        wap.active(True)
        wlan.active(False)

if __name__ == "__main__":
    print("Setting webrepl")
    setup_webrepl()
    