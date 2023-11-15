import aioespnow

class EspNowNode:

    def __init__(self, peers_mac: list[str]) -> None:
        self.node = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
        self.node.active(True)
        self.peers_mac = peers_mac

        for peer_mac in self.peers_mac:
            try:
                print(f"Adding peer's MAC address : {self.peers_mac}")
                self.node.add_peer(peer_mac)      # Must add_peer() before send()
            except OSError:
                print("Peer already exists")
                