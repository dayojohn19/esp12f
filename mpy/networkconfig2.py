import gc
import network
import socket
import ure
import json
import time
import esp  
import machine
import os

class NetworkConfig:
    def __init__(self, essid='Dayo network config', password='123456789', directory='/configs', server_timeout=40):
        self.timer = None
        self.led = machine.Pin(2, machine.Pin.OUT)
        self.wlan_ap = network.WLAN(network.AP_IF)
        self.wlan_sta = network.WLAN(network.STA_IF)
        self.directory = directory
        self.server_timeout = server_timeout
        self.server_socket = None
        self.setup_network(essid, password)

    def setup_network(self, essid, password):
        self.wlan_ap.active(True)
        self.wlan_ap.config(essid=essid, password=password)

    def blink_led(self, timer):
        self.led.value(not self.led.value())

    def start_blinking(self, speed=500):
        if self.timer is None:
            self.timer = machine.Timer(0)
            self.timer.init(period=speed, mode=machine.Timer.PERIODIC, callback=self.blink_led)

    def stop_blinking(self):
        if self.timer is not None:
            self.timer.deinit()
            self.timer = None
            self.led.value(1)

    def close_server_socket(self):
        if self.server_socket:
            self.server_socket.close()

    def handle_server(self, client, ntimeout):
        server_header = f"""
        <h2>Server Remaining runtime {ntimeout} of {self.server_timeout}</h2>
        <h1>Files in Config</h1>
        <ul>
        """
        server_variable = self.generate_file_list()
        server_footer = """
        </ul>
        <a href="/exit"> EXIT </a>
        """
        self.send_response(client, server_header + server_variable + server_footer)

    def generate_file_list(self):
        server_variable = ""
        files = os.listdir(self.directory)
        for file in files:
            pfile = os.path.join(self.directory, file)
            if os.path.isdir(pfile):
                print('its a path not file')
                continue
            server_variable += f"""<li><a href="/download?file={pfile}">
             {file}</a></li>
               """
        return server_variable

    def extract_file_path(self, request):
        try:
            start_index = request.find('?file=') + 6
            if start_index > 5:
                end_index = request.find(' ', start_index)
                if end_index == -1:
                    end_index = len(request)
                return request[start_index:end_index]
        except Exception as e:
            print(f"Error extracting file path: {e}")
        return None

    def send_response(self, client, response):
        client.send('HTTP/1.1 200 OK\r\n')
        client.send('Content-Type: text/html\r\n')
        client.send('Connection: close\r\n\r\n')
        client.sendall(response)
        client.close()

# Example usage
if __name__ == "__main__":
    network_config = NetworkConfig()
    # Example client and ntimeout values
    client = None  # Replace with actual client object
    ntimeout = 30  # Example timeout value
    network_config.handle_server(client, ntimeout)