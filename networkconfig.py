import gc
import network
import socket
import ure
import json
import time
import esp  
import machine
from mpy.led_signal import *
wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)
temp_server_timeout = 180
server_socket = None

def wait_to_connect(wlan_sta):
    startTime=time.time()
    while not wlan_sta.isconnected() and time.time()-startTime<=10:
        print('connecting')
        time.sleep(0.5)
    stop_blinking()


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
    # if not wlan_sta.isconnected():
        # print("Restarting Wifi")
        # import machine
        # machine.reset()       
    # handle_root(client)    
    send_response(client, "CANT CONNECT {}".format(ssid))
    

def handle_not_found(client, url):
    send_response(client, "Path not found: {}".format(url), status_code=404)

def stop():
    global server_socket
    
    if server_socket:
        server_socket.close()


def handle_server(client, ntimeout):
    import os
    server_header = f"""
    <h2>Server Remaining runtime {ntimeout} of {temp_server_timeout}</h2>
    <h1>Files in Config</h1>
    <ul>
    """
    server_variable = ""
    directory = '/configs'  # Change to your desired path
    files = os.listdir(directory)
    for file in files:
        pfile = directory+'/'+file
        if os.stat(pfile)[0] == 0x4000:
            print('its a path not file')
            pass
        else:
            server_variable += f"""<li><a  href="/download?file={pfile}" >
             {file}</a></li>
               """

    server_footer = """
    </ul>

    <a href="/exit"> EXIT </a>
    """
    send_response(client, server_header + server_variable + server_footer)

def extract_file_path(request):
    # Manually parse the file parameter from the query string in the URL
    print('REquest: ',request)
    try:
        # Extract the part after '?file=' in the request URL
        start_index = request.find('?file=') + 6  # 'file=' is 5 characters, plus 1 for the '='
        if start_index > 5:  # Check if '?file=' was found in the URL
            end_index = request.find(' ', start_index)  # Find the next space after the file name
            if end_index == -1:
                end_index = len(request)  # If no space is found, take the rest of the string
            return request[start_index:end_index]  # Return the filename
    except Exception as e:
        print(f"Error extracting file path: {e}")
    return None

def handle_download(client, fpath):
    import os
    if not os.stat(fpath):
        client.send('HTTP/1.1 404 Not Found\r\n')
        client.send('Content-Type: text/plain\r\n')
        client.send('Connection: close\r\n\r\n')
        client.send("File not found!")
        return
    client.send('HTTP/1.1 200 OK\r\n')
    client.send('Content-Type: application/octet-stream\r\n')
    client.send(f'Content-Disposition: attachment; filename="{fpath}"\r\n')  # Force download
    client.send('Connection: close\r\n\r\n')
    # client.send(fpath)
    with open(fpath, 'rb') as f:
        # file_content = f.read()
        chunk = f.read(1024)
        while chunk:
            client.send(chunk)
            chunk = f.read(1024)


def temporary_server():
    led.value(0)
    addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]
    global server_socket
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)
    server_socket.setblocking(False)
    # server_socket.settimeout(5)
    print('60sec listenings on', addr)
    start_time = time.time()
    while True:
        try:
            ntimeout = time.time() - start_time
            if ntimeout > temp_server_timeout:
                led.value(1)
                gc.collect()
                break
            print('TimeOUT: ',ntimeout)
            client, addr = server_socket.accept()
            client.settimeout(5.0)
            print('client connected from', addr)
            request = b""
            try:
                while not "\r\n\r\n" in request:
                    request += client.recv(512)
            except OSError:
                pass
            if "HTTP" not in request:
                client.close()
                continue
            url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request.decode('ascii')).group(1).rstrip("/")
            if url == "":
                handle_server(client,ntimeout)
            if '/download' in request:
                request = request.decode('utf-8')
                file_path = extract_file_path(request)
                print('Found path: ',file_path)
                # client.send()
                    # Handle the download request
                handle_download(client, file_path)
            if '/exit' in request:
                client.close()
                server_socket.close()
                gc.collect()
                break
        except OSError as e:
            if e.errno == 11: 
                print("No client connected, waiting...")
                time.sleep(0.5)
            else:
                print(f"Socket error: {e}")
                break
    server_socket.close()
    return

def start(port=80):
    start_blinking(1000)
    addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]
    global server_socket
    stop()
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)
    server_socket.setblocking(False)
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
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('Temporary Making Server')
    temporary_server() # Temporary open a server
    start_blinking(150)
    
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
        # print("Restarting Wifi")
        # import machine
        # machine.reset()
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



connectWifi()

