import time
import wifi as wifi

class WiFiNode:

    def __init__(self, ssid: str=None, password: str=None)->None:
        self.sta, self.ap = wifi.reset(sta=True, ap=False)
        wifi.connect(ssid, password)

        # Wait until connected...
        while not self.sta.isconnected():  
            time.sleep(0.1)

        wifi.status()

        # Disable power saving mode. 
        self.sta.config(pm=0)