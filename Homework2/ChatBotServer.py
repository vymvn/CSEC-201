import socket, threading
from Crypto.Cipher import DES
import rsa
import random, string
from googlesearch import search


class clientThread(threading.Thread):
    """ Thread that handles a single client
    """
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
    
    
    def run(self):
        ### Set-up phase ###
        starting_packet = process_packet_string(self.socket.recv(1024))
        print(f"Received starting packet from {self.address}")
        if int(starting_packet[3]) == 1:
            encryption_packet = process_packet_string(self.socket.recv(2048))
            print(f"Received encryption packet from {self.address}")
            if encryption_packet[1].upper() == "DES":
                # Making and encrypting session key
                
                pubKey_pkcs1 = ",".join(encryption_packet[2:],)
                print(pubKey_pkcs1)
                pubKey = rsa.key.PublicKey.load_pkcs1(pubKey_pkcs1.encode(), format='DER')
                # generating a random 8 byte string as the key
                sessionKey = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)).encode("utf-8")
                #encrypting session key with public key
                encryptedSK = rsa.encrypt(sessionKey, pubKey)   
                # cipher = DES.new(key, DES.MODE_OFB) # encrypting messages with key
                # encryptedMsg = cipher.iv + cipher.encrypt(random_string)
                print(sessionKey)
                
                SKpacket = f"SK, {encryptedSK}"
                self.socket.send(SKpacket.encode("utf-8"))
                print(f"Session key sent to {self.address}")
                
            elif encryption_packet[1].lower().strip(",") == "auth":
                username = encryption_packet[2].split(":")[0].strip()
                password = encryption_packet[2].split(":")[1].strip()
                print(f"[{self.address}] username: {username} / password: {password}") ## DELETE THIS LINE
        CCpacket = "CC"
        self.socket.send(CCpacket.encode("utf-8"))
        
        ### Operation Phase ###
        GRcases = ["hi", "hello", "greetings", "good morning", "good evening"]
        GRrespones = ["Hello! How can i help you?", "Hi there! What can i do for you?", "Greetings! Ask me something"]
        while True:
            # processing the message and choosing and appropriate response packet
            received = process_packet_string(self.socket.recv(2048))
            if received[0] == "ED":
                # Closing Phase
                print(f"Closing packet received from {self.address}")
                break
            elif received[0] == "IN":
                # greeting response
                if received[1].lower() in GRcases:
                    if "good morning".lower() in received[1].lower():
                        response = "Good morning! How can i help you?"
                    elif "good evening".lower() in received[1].lower():
                        response = "Good evening! How can i help you?"
                    else:
                        response = GRrespones[random.randint(0, 2)]
                    self.socket.send(f"GR, {response}".encode())
                elif "what" in received[1]:
                    # query = received[1]
                    # result = search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0) # This is for google packet
                    self.socket.send(f"IR, it is...".encode())
                
                elif "where" in received[1]:
                    self.socket.send(f"LR, well...did you try google maps? ".encode())

                elif "when" in received[1]:
                    self.socket.send(f"TR, Around 5 mins after too late ".encode())

                elif "search" in received[1]:
                    query = received[1].lstrip('search')
                    result = search(query,tld='com', lang='en', num=10, start=0, stop=None, pause=2.0)
                    self.socket.send(f"RR, {result}".encode())

                elif "permission" in received[1]:
                    self.socket.send(f"PR, Permission Granted, Godspeed ")
                    
                else:
                    self.socket.send(f"EE, InputError, Sorry i did not get that. Ask me something or type \"bye\" to quit.".encode())
        # Disconnecting after receiving closing packet
        self.socket.close()
        print(f"{self.address} Disconnected")
            

            
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


def process_packet_string(packet_string) -> list:
    temp = packet_string.decode().split(",")
    packet = []
    for i in temp:
        packet.append(i)
    return packet


def main():
    initServer("localhost", 6666)
    acceptConnections()
    
if __name__ == "__main__":
    main() 