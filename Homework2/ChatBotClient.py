import socket

# ChatBot information
VERSION = "v1.0"
PROTOCOL = "TTP"

# Packet class to define what a packet contains
class Packet():
    """ Packet class to define what a packet contains
    """
    def __init__(self, packet_type, protocol_name, version, encryption):
        self.packet_type = packet_type
        self.protocol_name = protocol_name
        self.version = version
        self.encryption = encryption

# Initializing socket
def initConnection(HOST, PORT):
    """ Initializes the socket and connects to it

    Args:
        host (string): IP of host destination
        port (int): The destination port
    """
    global s
    global ADDRESS
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDRESS = (HOST, PORT)
    s.connect(ADDRESS)

        

# Set-up phase
def setUpPhase():
    start_packet = f"SS, {PROTOCOL}, {VERSION}, 0"
    s.send(start_packet.encode("utf-8"))
    print("sent start packet")


def main():
    initConnection("localhost", 6666)
    setUpPhase()
    
if __name__ == "__main__":
    main()