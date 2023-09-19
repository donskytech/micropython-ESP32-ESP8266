from espnow_node import EspNowNode
from wifi_node import WiFiNode

MAC = 'AA:BB:CC:DD:EE:FF'
b_MAC = bytes([int(i, 16) for i in MAC.split(':')])

wifi = WiFiNode()
espnow = EspNowNode(peer_mac=b_MAC)

def main():
    espnow.node.irq(espnow.recv_cb)

main()
