## Flashing Software
`
esptool.py --port /dev/tty.usbserial-10 erase_flash
`

then flash the software [check this link](https://forum.micropython.org/viewtopic.php?t=3217)

`
esptool.py --port /dev/cu.usbserial-10 --baud 115200 write_flash --flash_mode=dout --flash_size=detect 0 esp8266-20170108-v1.8.7.bin
`

notes:
>   - fast blinking - connecting to wifi
>   - slow blinking - connect to 192.168.4.1 there you have to connect to wifi



>   list_html
>   - shows text data on 192.168.4.1

