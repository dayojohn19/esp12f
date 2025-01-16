# Everyday Update

>   - after saving always run the following [git link](https://github.com/dayojohn19/esp12f/tree/main)
>   -   always edit the version.json file

```
git add .
git commit -am 'code updated'
git push
```

### Values
>       configs folder
<hr>

## Flashing Software
```
esptool.py --port /dev/tty.usbserial-10 erase_flash
```

then flash the software [check this link](https://forum.micropython.org/viewtopic.php?t=3217)

```
esptool.py --port /dev/cu.usbserial-10 --baud 115200 write_flash --flash_mode=dout --flash_size=detect 0 esp8266-20170108-v1.8.7.bin
```

## Better Performance
<span style="color:orange;">pip3 install mpy-cross</span>

-   `mpy-cross` [path_to_file.py]
-   -   it will be make .mpy file and delete the original .py file for optimization of performance

notes:
>   - fast blinking - connecting to wifi
>   - slow blinking - connect to 192.168.4.1 there you have to connect to wifi



>   ### list_html.py
>   - file is on configs/list_names.txt
>   - automatically creates wifi hotspot
>   - shows text data on 192.168.4.1

> ### networkconfig.py
>   - initially run the <span style="color:orange;">connectWifi([ssid=None],[password=None])</span>
>   
>   it will automatically open a webserver named esp_12_wifi and connect 192.168.4.1 and find a router from there