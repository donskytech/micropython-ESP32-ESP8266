import aioespnow
import espnow_scan

class EspNowNode:

    def __init__(self, peer_mac: bytes):

        self.node = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
        self.node.active(True)
        self.peer_mac = peer_mac

        # Scan network for existing master devices.
        espnow_scan.scan(peer=self.peer_mac)