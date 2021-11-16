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
        data_string = self.socket.recv(1024) # receive starting packet
        print(f"Received starting packet from {self.address}")
        starting_packet = data_string.decode("utf-8").split()
        print(starting_packet)
        if int(starting_packet[3]) == 1:
            data_string = self.socket.recv(1024) # receive encryption packet
            print(f"Received encryption packet from {self.address}")
            encryption_packet = data_string.decode("utf-8").split()
            print(encryption_packet)
        

        
            
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


def main():
    HOST = socket.gethostbyname(socket.gethostname())
    initServer("localhost", 6666)
    acceptConnections()
    
if __name__ == "__main__":
    main() 