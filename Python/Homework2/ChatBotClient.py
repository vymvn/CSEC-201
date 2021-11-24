import socket
import string
from threading import Thread
import threading
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import rsa
import time

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
            global algo
            algo = input("Please choose encryption algorithm (DES/Auth)\n>> ")
            if algo.upper() == "DES":
                global doneEncryption
                doneEncryption = False
                loadThread = threading.Thread(target=animate)
                loadThread.start()
                (pubKey, privKey) = rsa.newkeys(2048)
                pubKey_pkcs1 = pubKey.save_pkcs1(format='PEM')
                encryption_packet1 = f"EC,DES"
                encryption_packet2 = pubKey_pkcs1  # Sending packet in 2 parts so the key is received as raw bytes
                s.send(encryption_packet1.encode())
                s.send(encryption_packet2)
                SKpacket = process_packet_string(s.recv(1024))
                doneEncryption = True
                if SKpacket[0] == "SK":
                    SK = s.recv(1024)
                    global sessionKey
                    sessionKey = rsa.decrypt(SK, privKey)
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
        loadThread.join()
        print(f"Welcome to ChatBot {VERSION}")
        if encryption_type == 1:
            if algo.upper() == "DES":
                encrypted_operation_phase() # starting encrypted operation phase
        else:
            operation_phase() # starting operation phase
    elif confirmation_packet[0] == "EE":
        print(confirmation_packet[2])
    else:
        print("Unknown error")


def encrypted_operation_phase():
    """ main loop that sends and receives encrypted packets
    """
    while True:
        msg = input(">> ") # getting users input
        if msg: # Checking for empty input
            if msg.lower() == "end": 
                ## closing phase ##
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
                INpacket = f"IN,{msg}" # making packet
                encryptedPacket, iv = encryptMsg(INpacket, sessionKey) # encrypting packet
                s.send(encryptedPacket) # sending encrypted packet
                s.send(iv) # sending initialization vector needed for decrypting 
                encryptedReply = s.recv(1024)
                iv = s.recv(100)
                decryptedReply = decryptMsg(encryptedReply, sessionKey, iv)
                responsePacket = process_packet_string(decryptedReply)
                if responsePacket[0] == "EE":
                    if responsePacket[1] == "InputError":
                        print(f"[ChatBot]: {responsePacket[2]}")
                elif responsePacket[0] == "GR" or responsePacket[0] == "IR" or responsePacket[0] == "LR" or responsePacket[0] == "TR" or responsePacket[0] == "RR" or responsePacket[0] == "PR":
                    print(f"[ChatBot]: {responsePacket[1]}")

def operation_phase():
    # getting user messages 
    while True:
        msg = input(">> ")
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
                INpacket = f"IN,{msg}"
                s.send(INpacket.encode())
                reply = process_packet_string(s.recv(2048))
                if reply[0] == "EE":
                    if reply[1] == "InputError":
                        print(f"[ChatBot]: {reply[2]}")
                elif reply[0] == "GR" or reply[0] == "IR" or reply[0] == "LR" or reply[0] == "TR" or reply[0] == "RR" or reply[0] == "PR":
                    print(f"[ChatBot]: {reply[1]}")
                    

def encryptMsg(msg, key) -> bytes:
    cipher = DES.new(key, DES.MODE_CBC) # making encryption cipher with session key
    iv = cipher.iv 
    encryptedMsg = cipher.encrypt(pad(msg.encode(), DES.block_size))
    return encryptedMsg, iv

def decryptMsg(encryptedMsg, key, iv) -> str:
    decryptionCipher = DES.new(key, DES.MODE_CBC, iv) # making decryption cipher with session key
    decryptedMsg = unpad(decryptionCipher.decrypt(encryptedMsg), DES.block_size).decode()
    return decryptedMsg


def process_packet_string(packet_string) -> list:
    try:
        temp = packet_string.decode().split(",")
    except:
        temp = packet_string.split(",")
    packet = []
    for i in temp:
        packet.append(i.strip())
    return packet

def animate():
    while doneEncryption == False:
        print('\rEncrypting your connection.. |', end="")
        time.sleep(0.1)
        print('\rEncrypting your connection.. /', end="")
        time.sleep(0.1)
        print('\rEncrypting your connection.. -', end="")
        time.sleep(0.1)
        print('\rEncrypting your connection.. \\', end="")
        time.sleep(0.1)
    print('\rConnection encrypted!                             \n', end="")

def main():
    initConnection("localhost", 6666)
    setUpPhase()
    s.close()
    
if __name__ == "__main__":
    main()