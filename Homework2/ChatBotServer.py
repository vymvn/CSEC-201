import socket, threading



class clientThread(threading.Thread):
    """[summary]

    Args:
        threading ([type]): [description]
    """
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
    
    
    def run(self):
        # Set-up phase 
        data_string = self.socket.recv(1024)
        print(f"Received starting packet from {self.address}")
        starting_packet = process_data_string(data_string.decode("utf-8"))
        if starting_packet["Encryption"] == 1:
            self.socket.send("Give me encryption packet".encode("utf-8"))
        print(starting_packet)
            


def process_data_string(data_string) -> dict:
    packet = {}
    data = data_string.split()
    packet["Packet type"] = data[0]
    packet["Protocol name"] = data[1]
    packet["Version"] = data[2]
    packet["Encryption"] = data[3]
    return packet


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
    initServer("localhost", 6666)
    acceptConnections()
    
if __name__ == "__main__":
    main()