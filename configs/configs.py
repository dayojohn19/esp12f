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


files_to_update=["main.py","configs/listnames.txt","configs/esp12settings.json",'test3.txt','test4.txt','test5.txt','clock']
giturl= "https://github.com/dayojohn19/esp12f/"

 