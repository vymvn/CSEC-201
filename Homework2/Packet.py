# Packet class to define what a packet contains
class Packet():
    """ Packet class to define what a packet contains
    """
    def __init__(self, packet_type, protocol_name, version, encryption):
        self.packet_type = packet_type
        self.protocol_name = protocol_name
        self.version = version
        self.encryption = encryption