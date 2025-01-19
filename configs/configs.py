from machine import Pin, I2C, ADC

clock_sqw = 13 # D7
clock_scl = 14 # D5
clock_sda = 12 # D6|
alarm = {'am':6,'pm':17,'min':44}
essid='Dayo network config'
password='123456789'
server_addr='192.168.4.1'
# Analog read pin
analog_pin = ADC(0)  # ADC0

amAlarm = 7,00  
pmAlarm = 17,00
BatteryPin  =    0
servoPin    =   5

myPhoneNumber="919876543210"
whatsapp_key="2890524"

files_to_update=["main.py","configs/listnames.txt","configs/esp12settings.json",'test3.txt','test4.txt','test5.txt','clock']
giturl= "https://github.com/dayojohn19/esp12f/"

logPath = 'configs/'            
sim_rx=1
sim_tx=2