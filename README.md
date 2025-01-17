# Everyday Update

>   - after saving always run the following [git link](https://github.com/dayojohn19/esp12f/tree/main)
>   -   edit the version.json file

watching <span style="color:red;">files_to_update</span>

```
git pull
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
activate virtual environment actual code:
```
source path/to/venv/bin/activate
```
then
```
mpy-cross filename.py
```
store all py file in pytompy folder

all are in pymakr.conf ignore files

<span style="color:orange;">pip3 install mpy-cross</span>

-   `mpy-cross` [path_to_file.py]
-   -   it will be make .mpy file and delete the original .py file for optimization of performance

## <span style="color:red;">Notes:</span>
>   - fast blinking - connecting to wifi
>   - slow blinking - connect to 192.168.4.1 there you have to connect to wifi
>   -   github workflow auto update version.json, that is why we need to pull



### list_html.py
>   - file is on configs/list_names.txt
>   - automatically creates wifi hotspot
>   - shows text data on 192.168.4.1

### networkconfig.py
>   -   led light stays -  created webserver  192.168.4.1 to  download anything in configs folder, refresh the page after clicking download for (temp_server_timeout)
>   -   fast blinking - connecting to wifi from settings
>   -   slow blinking - webserver at 192.168.4.1 asking for wifi config
>   - initially run the <span style="color:orange;">connectWifi([ssid=None],[password=None])</span>
>   
>   -   it will automatically open a webserver named <span style="color:orange;">esp_12_wifi</span> and connect 192.168.4.1 and find a router from there
>   -   

 ### ota_git.py
>   -   updates from [github repo](https://github.com/dayojohn19/esp12f/tree/main) 
>   -   all files indicated in esp12settings.json

### led_signal.mpy
>     from led_signal import *
>   -   start_blinking( [millisecond ])
>   -   stop_blinking()
>   -   led.value(0) or led.value(1)   0 for on 1 for off