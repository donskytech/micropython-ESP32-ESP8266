import espnow
import espnow_scan

class EspNowNode:

    def __init__(self, peer_mac: bytes):
        self.node = espnow.ESPNow()
        self.node.active(True)
        self.peer_mac = peer_mac

        # Scan network for existing master devices.
        espnow_scan.scan(peer=self.peer_mac, enow=self.node)

    def recv_cb(self, node):
        host, msg = node.recv(0)
        if msg:             # msg == None if timeout in recv()
            print(host, msg)







