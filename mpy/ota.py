import network
import urequests
import os
import json
import gc
import machine
from time import sleep

class OTAUpdater:
    """ This class handles OTA updates. It connects to the Wi-Fi, checks for updates, downloads and installs them."""
    def __init__(self, ssid, password, repo_url, filenames=[]):
        self.filenames = filenames
        self.ssid = ssid
        self.password = password
        self.repo_url = repo_url
        if "www.github.com" in self.repo_url :
            print(f"Updating {repo_url} to raw.githubusercontent")
            self.repo_url = self.repo_url.replace("www.github","raw.githubusercontent")
        elif "github.com" in self.repo_url:
            print(f"Updating {repo_url} to raw.githubusercontent'")
            self.repo_url = self.repo_url.replace("github","raw.githubusercontent")            
        self.version_url = self.repo_url + 'main/version.json'
        print(f"version url is: {self.version_url}")
        self.firmware_urls = [] 
        for file in filenames:
            filename = self.repo_url + 'main/' + file
            self.firmware_urls.append(filename)

        # get the current version (stored in version.json)
        if 'version.json' in os.listdir():    
            with open('version.json') as f:
                self.current_version = int(json.load(f)['version'])
            print(f"Current device firmware version is '{self.current_version}'")

        else:
            self.current_version = 0
            # save the current version
            with open('version.json', 'w') as f:
                json.dump({'version': self.current_version}, f)
            
    def connect_wifi(self):
        """ Connect to Wi-Fi."""

        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(self.ssid, self.password)
        while not sta_if.isconnected():
            print('.', end="")
            sleep(0.25)
        print(f'Connected to WiFi, IP is: {sta_if.ifconfig()[0]}')
        
    def fetch_latest_code(self)->bool:
        """ Fetch the latest code from the repo, returns False if not found."""
        for i in range(len(self.firmware_urls)):
            # Fetch the latest code from the repo.
            response = urequests.get(self.firmware_urls[i])
            if response.status_code == 200:
                print(f'Fetched latest firmware code, status: ')
                # Save the fetched code to memory
                self.latest_code = response.text
                with open('latest_code.py', 'w') as f:
                    f.write(self.latest_code)
                    print(f"Updating device... (Renaming latest_code.py to {self.filenames[i]})", end="")
                    print(response.text)
                    print(f"\n Link   {self.firmware_urls[i]} \n\n")
                    # Overwrite the old code.
                    os.rename('latest_code.py', self.filenames[i])  
                    # Restart the device to run the new code.
            elif response.status_code == 404:
                print(f'Firmware not found - {self.firmware_url}.')
                pass
            print('\n\n Done Updating: ',self.filenames[i])
            sleep(1.5)
        
        
        self.current_version = self.latest_version
        # save the current version
        with open('version.json', 'w') as f:
            json.dump({'version': self.current_version}, f)
        
        # free up some memory
        # self.latest_code = None
# Reset the device to run the new code.

        return True

    def update_no_reset(self):
        gc.collect()
        print('Restarting device...')
        self.latest_code = None
        machine.reset()  
        pass

    def update_and_reset(self):
        pass



        
    def check_for_updates(self):
        """ Check if updates are available."""
        
        # Connect to Wi-Fi
        self.connect_wifi()

        print(f'Checking for latest version... on {self.version_url}')
        response = urequests.get(self.version_url)
        
        data = json.loads(response.text)
        
        print(f"data is: {data}, url is: {self.version_url}")
        print(f"data version is: {data['version']}")
        # Turn list to dict using dictionary comprehension
#         my_dict = {data[i]: data[i + 1] for i in range(0, len(data), 2)}
        
        self.latest_version = int(data['version'])
        print(f'latest version is: {self.latest_version}')
        
        # compare versions
        newer_version_available = True if self.current_version < self.latest_version else False
        
        print(f'Newer version available: {newer_version_available}')    
        return newer_version_available
    
    def download_and_install_update_if_available(self):
        """ Check for updates, download and install them."""
        if self.check_for_updates():
            if self.fetch_latest_code():
                self.update_no_reset() 
                self.update_and_reset() 
        else:
            print('No new updates available.')