from espnow_node import EspNowNode
from wifi_node import WiFiNode
import urequests

MAC_0 = '78:21:84:C6:38:B0'
b_MAC = [bytes([int(i, 16) for i in mac.split(':')]) for mac in [MAC_0]]

espnow = EspNowNode(peers_mac=b_MAC)
wifi = WiFiNode("donsky-4thFloor", "donsky982")

def main():
    # Test GET request.
    response = urequests.get('http://jsonplaceholder.typicode.com/albums/1')
    print(response.text)

    # Test ESP-NOW.
    for i, peer in enumerate(b_MAC):
        payload = f"Hello peer {i}!"
        response = espnow.node.send(peer, payload, True)
        print(f"msg recieved on {peer} -> {response}")

main()