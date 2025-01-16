import network
import socket
import ure
import json
import time
import esp  
import machine
timer = None
# Initialize GPIO2 pin as output (Onboard LED for ESP12-F)
led = machine.Pin(2, machine.Pin.OUT)
def blink_led(timer):
    led.value(not led.value())  # Toggle LED state

def start_blinking(speed=500):
    global timer  # Declare timer as global to modify it
    # Create and start the timer (Timer 0)
    if timer is None:  # Only create the timer if it's not already created
        timer = machine.Timer(0)
        timer.init(period=speed, mode=machine.Timer.PERIODIC, callback=blink_led)
        print("LED blinking started.")
def stop_blinking():
    global timer  # Access the global timer
    if timer is not None:
        timer.deinit()  # Stop the timer
        timer = None  # Reset the global timer to None
        print("LED blinking stopped.")

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

server_socket = None

def wait_to_connect(wlan_sta):
    startTime=time.time()
    while not wlan_sta.isconnected() and time.time()-startTime<=10:
        print('connecting')
        time.sleep(0.5)


def send_response(client, payload, status_code=200):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    client.sendall("Content-Length: {}\r\n".format(len(payload)))
    client.sendall("\r\n")
    
    if len(payload) > 0:
        client.sendall(payload)

def handle_root(client):
    response_header = """
        <h1>Wi-Fi Client Setup</h1>
        <form action="configure" method="post">
          <label for="ssid">SSID</label>
          <select name="ssid" id="ssid">
    """
    
    response_variable = ""
    for ssid, *_ in wlan_sta.scan():
        response_variable += '<option value="{0}">{0}</option>'.format(ssid.decode("utf-8"))
    
    response_footer = """
           </select> <br/>
           Password: <input name="password" type="password"></input> <br />
           <input type="submit" value="Submit">
         </form>
    """
    send_response(client, response_header + response_variable + response_footer)

def handle_configure(client, request):
    import time
    match = ure.search("ssid=([^&]*)&password=(.*)", request)
    
    if match is None:
        send_response(client, "Parameters not found", status_code=400)
        return
    
    ssid = match.group(1)
    password = match.group(2)
    
    if len(ssid) == 0:
        send_response(client, "SSID must be provided", status_code=400)
        return

    print(f"\n\n     Creating New Config for {ssid}")
    with open('configs/wifiSettings.json') as f:
        config = json.load(f)
    with open('configs/wifiSettings.json','w') as f:
        config["ssid"] = ssid
        config["ssid_password"] = password
        json.dump(config, f)
    wlan_sta.active(True)
    time.sleep(1)
    wlan_sta.connect(ssid, password)
    wait_to_connect(wlan_sta)
    if wlan_sta.isconnected():
        stop_blinking()
        print("Restarting Wifi")
        import machine
        machine.reset()       
    # handle_root(client)    
    send_response(client, "CANT CONNECT {}".format(ssid))
    

def handle_not_found(client, url):
    send_response(client, "Path not found: {}".format(url), status_code=404)

def stop():
    global server_socket
    
    if server_socket:
        server_socket.close()

def start(port=80):
    start_blinking(1000)
    addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]
    
    global server_socket
    
    stop()
    
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)

    print('listening on', addr)
    
    while True:
        client, addr = server_socket.accept()
        client.settimeout(5.0)
        print('client connected from', addr)
        
        request = b""
        try:
            while not "\r\n\r\n" in request:
                request += client.recv(512)
        except OSError:
            pass
        
        print("Request is: {}".format(request))
        if "HTTP" not in request:
            # skip invalid requests
            client.close()
            continue
        
        url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request.decode('ascii')).group(1).rstrip("/")
        print("URL is {}".format(url))

        if url == "":
            handle_root(client)
        elif url == "configure":
            handle_configure(client, request)
        else:
            handle_not_found(client, url)
        
        client.close()







def connectWifi(wifiSSID=None,wifiPassword=None): # option to put SSID AND PAssword
    start_blinking(150)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    import gc
    # wlan.PM_POWERSAVE
    time.sleep(1)
    gc.collect()
    time.sleep(1)
    esp.osdebug(None)
    time.sleep(1)
    time.sleep(1)
    if wifiSSID==None:
        print('Importing from wifi settings json..')
        with open('configs/wifiSettings.json') as f:
            config = json.load(f)
            wifiSSID = config['ssid']
            wifiPassword = config['ssid_password']
    elif wifiSSID != None:
        print(f"\n\n     Creating New Config for {wifiSSID}")
        with open('configs/wifiSettings.json') as f:
            config = json.load(f)
        with open('configs/wifiSettings.json','w') as f:
            config["ssid"] = wifiSSID
            config["ssid_password"] = wifiPassword
            json.dump(config, f)
        print("Restarting Wifi")
        import machine
        machine.reset()
    time.sleep(1)
    print(f"     Connecting:  {wifiSSID}  {wifiSSID}")
    wlan.connect(wifiSSID,wifiPassword)
    wait_to_connect(wlan)

    time.sleep(1)
    WifiName = wifiSSID
    time.sleep(1)
    WifiConnected = wlan.isconnected()
    time.sleep(1)
    if wlan.isconnected():
        print('Wifi Connected')
        stop_blinking()
        return [True,' Wifi Connected']
    else:
        stop_blinking()
        print('Cant Connect Restarting')
        time.sleep(1)
        start()
        # return [False, ' Wifi not Connected ']
        # import machine
        # machine.reset()






