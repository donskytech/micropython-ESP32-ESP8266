import wifi as wifi

class WiFiNode:

    def __init__(self) -> None:
        self.sta, self.ap = wifi.reset(sta=True, ap=False)

        # Disable power saving mode.     
        self.sta.config(pm=0)

        wifi.status()