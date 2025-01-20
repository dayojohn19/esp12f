# # This file is executed on every boot (including wake-boot from deepsleep)
# #import esp
# #esp.osdebug(None)
# import os, machine
# #os.dupterm(None, 1) # disable REPL on UART(0)
# import gc
# import webrepl
# import json
# import network 
# import time
# with open('configs/wifiSettings.json') as f:
#     config = json.load(f)
#     wifiSSID = config['ssid']
#     wifiPassword = config['ssid_password']
# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect(wifiSSID, wifiPassword)
# for i in range(3):
#     print(i,'Connecting to ',wifiSSID)
#     time.sleep(1)
# wlan.ifconfig()
# wap = network.WLAN(network.AP_IF)
# wap.active(False)
# if wlan.isconnected():
#     print("Connected to wifi ")
#     print("Connect WebREPL : ", wlan.ifconfig()[0])
# elif not wlan.isconnected():
#     print("cant connect to wifi setting up")
#     led_builtin =machine.Pin(2, machine.Pin.OUT)
#     led_builtin.off()
#     wap.active(True)
#     wlan.active(False)
#     print("Connect WebREPL: ",wap.ifconfig()[0])
# webrepl.start()
# print("WebREPL started in ")
# time.sleep(5)
# gc.collect()
