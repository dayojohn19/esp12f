from machine import Pin, I2C, ADC

clock_sqw = 13 # D7
clock_scl = 14 # D5
clock_sda = 12 # D6|
sim_rx=2 # D4
sim_tx=15 # D8
sim_pk=4 # D4
sim_uart=1





ap_ssid='Dayo network config'
ap_password='123456789'

server_addr='192.168.4.1'
# Analog read pin

amAlarm = 7,00  
pmAlarm = 17,10
BatteryPin  =    0 # A0
analog_pin = ADC(0)  # ADC0
servoPin    =   1 # D1

myPhoneNumber="919876543210"
whatsapp_key="2890524"

files_to_update=["main.py","configs/listnames.txt","configs/esp12settings.json"]
giturl= "https://github.com/dayojohn19/esp12f/"

rootpath = 'configs/'            

