import socket
from Crypto.Cipher import DES
import rsa

# ChatBot information
VERSION = "v1.0"
PROTOCOL = "TTP"


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
    """ Setting up connection and encryption between client and server
    """
    print("Connection established!")
    # asking user for encryption type they want to connect with
    correct = False
    while not correct:
        try:
            encryption_type = int(input("Enter 1 for a secure connection, or 0 for normal connection:\n>> "))
            if encryption_type == 1 or encryption_type == 0:
                correct = True
            else: 
                raise Exception
        except:
            print("[INVALID INPUT] Please try again..")
    start_packet = f"SS,{PROTOCOL},{VERSION},{encryption_type}"
    s.send(start_packet.encode("utf-8"))
    if encryption_type == 1:
        while True:
            algo = input("Please choose encryption algorithm (DES/Auth)\n>> ")
            if algo.upper() == "DES":
                (pubKey, privKey) = rsa.newkeys(2048)
                pubKey_pkcs1 = pubKey.save_pkcs1(format='DER')
                encryption_packet1 = f"EC,DES"
                encryption_packet2 = pubKey_pkcs1  # Sending packet in 2 parts so the key is received as raw bytes
                s.send(encryption_packet1.encode())
                s.send(encryption_packet2)
                SKpacket = process_packet_string(s.recv(1024))
                if SKpacket[0] == "SK":
                    SK = s.recv(1024)
                    sessionKey = rsa.decrypt(SK, privKey)
                    print("Session key received successfully!")
                    global cipher
                    cipher = DES.new(sessionKey, DES.MODE_OFB) # the encryption cipher
                break
            elif algo.lower() == "auth":
                username = input("Username: ")
                password = input("Password: ")
                encryption_packet = f"EC,{algo.lower()},{username}:{password}"
                s.send(encryption_packet.encode("utf-8"))
                break
            else:
                print("[INVALID INPUT] Please try again..")
    confirmation_packet = process_packet_string(s.recv(1024))
    if confirmation_packet[0] == "CC":   
        print(f"Welcome to ChatBot {VERSION}")
    elif confirmation_packet[0] == "EE":
        print("An error occurred")
    else:
        print("Unknown error")


def operation_phase():
    # getting user messages 
    while True:
        msg = input(">> ")
        encryptedMsg = cipher.iv + cipher.encrypt(msg.encode())
        if msg: # Checking for empty input
            if msg.lower() == "end":
                confirm = input("Are you sure you want to quit? (y/n)\n>> ")
                if confirm.lower() == 'y' or confirm.lower() == "yes":
                    print("Goodbye!")
                    EDpacket = f"ED"
                    s.send(EDpacket.encode())
                    break
                elif confirm.lower() == 'n' or confirm.lower() == "no":
                    pass
                else:
                    print("[INVALID INPUT] Please try again..")   
            else:
                INpacket = f"IN,{encryptedMsg}"
                s.send(INpacket.encode())
                decryptedReply = cipher.iv + cipher.decrypt(process_packet_string(s.recv(2048)))
                if decryptedReply[0] == "EE":
                    if decryptedReply[1] == "InputError":
                        print(decryptedReply[2])
                elif decryptedReply[0] == "GR" or decryptedReply[0] == "IR" or decryptedReply[0] == "LR" or decryptedReply[0] == "TR" or decryptedReply[0] == "RR" or decryptedReply[0] == "PR":
                    print(decryptedReply[1])
                    


def process_packet_string(packet_string) -> list:
    temp = packet_string.decode().split(",")
    packet = []
    for i in temp:
        packet.append(i.strip())
    return packet


def main():
    initConnection("localhost", 6666)
    setUpPhase()
    operation_phase()
    s.close()
    
if __name__ == "__main__":
    main()