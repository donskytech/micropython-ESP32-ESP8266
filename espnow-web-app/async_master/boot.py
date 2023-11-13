# boot.py -- run on boot-up
import network


def do_connect_sta():
    # Replace the following with your WIFI Credentials
    SSID = "<PLACE_YOUR_SSID_HERE>"
    SSI_PASSWORD = "<PLACE_YOUR_WIFI_PASWORD_HERE>"
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Connected! Network config:', sta_if.ifconfig())
    
    
def do_connect_ap():
    # Replace the following with your WIFI Credentials
    ssid = 'smart_farming_tupt'
    password = 'team-tupt'
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    while ap.active() == False:
        pass
    print('Connection successful')
    print(ap.ifconfig())
    
print("Connecting to your wifi...")
# do_connect()
do_connect_ap()