import socket, threading
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import rsa
import random
from googlesearch import search


class clientThread(threading.Thread):
    """ Thread that handles a single client
    """
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
    

    def run(self):
        ###################### Set-up phase ########################
        starting_packet = process_packet_string(self.socket.recv(1024))
        print(f"Received starting packet from {self.address}")
        if int(starting_packet[3]) == 1:
            encryption_packet = process_packet_string(self.socket.recv(2048))
            print(f"Received encryption packet from {self.address}")
            if encryption_packet[1].upper() == "DES":
                # Making and encrypting session key
                pubKey_pkcs1 = self.socket.recv(2048) # Receiving public key
                pubKey = rsa.key.PublicKey.load_pkcs1(pubKey_pkcs1, format='PEM')
                sessionKey = get_random_bytes(8) # generating a random 8 bytes as the session key
                encryptedSK = rsa.encrypt(sessionKey, pubKey) # encrypting session key with public key
                SKpacket1 = f"SK"
                SKpacket2 = encryptedSK
                self.socket.send(SKpacket1.encode("utf-8"))
                self.socket.send(SKpacket2) # Sending packet in 2 parts so the key is received as raw bytes
                print(f"Session key sent to {self.address}")
                CCpacket = "CC"
                self.socket.send(CCpacket.encode("utf-8"))
        ############################################################
                
                ################## encrypted operation phase #################
                GRcases = ["hi", "hello", "greetings", "good morning", "good evening"]
                GRrespones = ["Hello! How can i help you?", "Hi there! What can i do for you?", "Greetings! Ask me something"]
                while True:
                    # receiving encrypted packet and decrypting it
                    encryptedPacket = self.socket.recv(1024)
                    iv = self.socket.recv(500)
                    received = process_packet_string(decryptMsg(encryptedPacket, sessionKey, iv))
                    # processing the message and choosing and appropriate response packet
                    if received[0] == "ED":
                        # Closing Phase
                        print(f"Closing packet received from {self.address}")
                        break
                    elif received[0] == "IN":
                        # greeting response
                        if received[1].lower() in GRcases:
                            if "morning".lower() in received[1].lower():
                                response = "Good morning! How can i help you?"
                            elif "evening".lower() in received[1].lower():
                                response = "Good evening! How can i help you?"
                            else:
                                response = GRrespones[random.randint(0, len(GRrespones) - 1)]
                            packet = f"GR,{response}"
                            encryptedPacket, vi = encryptMsg(packet, sessionKey)
                            self.socket.send(encryptedPacket)
                            self.socket.send(vi)
                        elif "what" in received[1]:
                            packet = f"IR,it is uhhhh"
                            encryptedPacket, vi = encryptMsg(packet, sessionKey)
                            self.socket.send(encryptedPacket)
                            self.socket.send(vi)
                        
                        elif "where" in received[1]:
                            # self.socket.send(f"LR, well...did you try google maps? ".encode())
                            packet = f"LR,well...did you try google maps?"
                            encryptedPacket, vi = encryptMsg(packet, sessionKey)
                            self.socket.send(encryptedPacket)
                            self.socket.send(vi)

                        elif "when" in received[1]:
                            packet = f"TR,Around 5 mins after too late "
                            encryptedPacket, vi = encryptMsg(packet, sessionKey)
                            self.socket.send(encryptedPacket)
                            self.socket.send(vi)

                        elif "search" in received[1]:
                            query = received[1].lstrip('search')
                            result = search(query,tld='com', lang='en', num=10, start=0, stop=None, pause=2.0)
                            packet = f"RR,{result}"
                            encryptedPacket, vi = encryptMsg(packet, sessionKey)
                            self.socket.send(encryptedPacket)
                            self.socket.send(vi)

                        elif "permission" in received[1]:
                            packet = f"PR,Permission Granted"
                            encryptedPacket, vi = encryptMsg(packet, sessionKey)
                            self.socket.send(encryptedPacket)
                            self.socket.send(vi)
                            
                        else:
                            packet = f"EE, InputError, Sorry i did not get that. Ask me something or type \"bye\" to quit."
                            encryptedPacket, vi = encryptMsg(packet, sessionKey)
                            self.socket.send(encryptedPacket)
                            self.socket.send(vi)
                # Disconnecting after receiving closing packet
                self.socket.close()
                print(f"{self.address} Disconnected")
                
            elif encryption_packet[1].lower().strip(",") == "auth":
                self.username = encryption_packet[2].split(":")[0].strip()
                self.password = encryption_packet[2].split(":")[1].strip()
                CCpacket = "CC"
                self.socket.send(CCpacket.encode("utf-8"))
        else:
            CCpacket = "CC"
            self.socket.send(CCpacket.encode("utf-8"))
        
        
        
        ### Non-encrypted operation phase ###
        GRcases = ["hi", "hello", "greetings", "good morning", "good evening"]
        GRrespones = ["Hello! How can i help you?", "Hi there! What can i do for you?", "Greetings! Ask me something"]
        while True:
            received = process_packet_string(self.socket.recv(100))
            # processing the message and choosing and appropriate response packet
            if received[0] == "ED":
                # Closing Phase
                print(f"Closing packet received from {self.address}")
                break
            elif received[0] == "IN":
                # greeting response
                if received[1].lower() in GRcases:
                    if "morning".lower() in received[1].lower():
                        response = "Good morning! How can i help you?"
                    elif "evening".lower() in received[1].lower():
                        response = "Good evening! How can i help you?"
                    else:
                        response = GRrespones[random.randint(0, len(GRrespones) - 1)]
                        
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



def encryptMsg(msg, key) -> bytes:
    cipher = DES.new(key, DES.MODE_CBC)
    iv = cipher.iv
    encryptedMsg = cipher.encrypt(pad(msg.encode(), DES.block_size))
    return encryptedMsg, iv

def decryptMsg(encryptedMsg, key, iv) -> str:
    decryptionCipher = DES.new(key, DES.MODE_CBC, iv)
    decryptedMsg = unpad(decryptionCipher.decrypt(encryptedMsg), DES.block_size).decode()
    return decryptedMsg


def process_packet_string(packet_string) -> list:
    try:
        temp = packet_string.decode().split(",")
    except:
        temp = packet_string.split(",")
    packet = []
    for i in temp:
        packet.append(i)
    return packet




def main():
    initServer("localhost", 6666)
    acceptConnections()
    
if __name__ == "__main__":
    main() 