import socket, threading



class clientThread(threading.Thread):
    """ Thread that handles a single client
    """
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
    
    
    def run(self):
        # Set-up phase 
        starting_packet = process_packet_string(self.socket.recv(1024))
        print(f"Received starting packet from {self.address}")
        print(starting_packet) ## DELETE THIS LINE
        if int(starting_packet[3]) == 1:
            encryption_packet = process_packet_string(self.socket.recv(1024))
            print(f"Received encryption packet from {self.address}")
            print(encryption_packet) ## DELETE THIS LINE 
            if encryption_packet[1].upper() == "DES":
                sessionKey = "KEY" ## UPDATE TO GIVE ACTUAL KEY
                SKpacket = f"SK, {sessionKey}"
                self.socket.send(SKpacket.encode("utf-8"))
                print(f"Session key sent to {self.address}")
            elif encryption_packet[1].lower().strip(",") == "auth":
                username = encryption_packet[2].split(":")[0].strip()
                password = encryption_packet[2].split(":")[1].strip()
                print(f"[{self.address}] username: {username} / password: {password}") ## DELETE THIS LINE
        CCpacket = "CC"
        self.socket.send(CCpacket.encode("utf-8"))

        
            
def initServer(HOST, PORT):
    """ initializes server socket to accept connections

    Args:
        HOST (String): IP address 
        PORT (Int): Destination port
    """
    global serverSocket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen()
    print(f"[SERVER STARTED] Listening on port {PORT}")
    
    
def acceptConnections():
    while True:
        clientSocket, address = serverSocket.accept()
        print(f"Got a connection from {address}")
        newClientThread = clientThread(clientSocket, address)
        newClientThread.start()


def process_packet_string(packet_string):
    temp = packet_string.decode().split()
    packet = []
    for i in temp:
        packet.append(i.strip(","))
    return packet


def main():
    HOST = socket.gethostbyname(socket.gethostname())
    initServer("localhost", 6666)
    acceptConnections()
    
if __name__ == "__main__":
    main() 