import socket
from Crypto.PublicKey import RSA

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
    start_packet = f"SS, {PROTOCOL}, {VERSION}, {encryption_type}"
    s.send(start_packet.encode("utf-8"))
    if encryption_type == 1:
        while True:
            algo = input("Please choose encryption algorithm (DES/Auth)\n>> ")
            if algo.upper() == "DES":
                pub_key = f"My public key" ## UPDATE TO GIVE ACTUAL PUBLIC KEY
                encryption_packet = f"EC, DES, {pub_key}"
                s.send(encryption_packet.encode("utf-8"))
                SKpacket = process_packet_string(s.recv(1024)) ## DECRYPT WITH PRIVATE KEY
                if SKpacket[0] == "SK":
                    SK = SKpacket[1]
                    print(f"Session key is:\n{SK}")
                break
            elif algo.lower() == "auth":
                username = input("Username: ")
                password = input("Password: ")
                encryption_packet = f"EC, {algo.lower()}, {username}:{password}"
                s.send(encryption_packet.encode("utf-8"))
                break
            else:
                print("[INVALID INPUT] Please try again..")
    confirmation_packet = process_packet_string(s.recv(1024))
    if confirmation_packet[0] == "CC":   
        print("Connected successfully!")
    elif confirmation_packet[0] == "EE":
        print("An error occurred")
    else:
        print("Unknown error")


def operation_phase():
    # getting user messages 
    while True:
        msg = input(">> ")
        if msg: # Checking for empty input
            if msg.lower() == "bye":
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
                INpacket = f"IN, {msg}"
                s.send(INpacket.encode())
                reply = process_packet_string(s.recv(2048))
                if reply[0] == "EE":
                    if reply[1] == "InputError":
                        print(reply[2])
                elif reply[0] == "GR":
                    print(reply[1])
                elif reply[0] == "IR":
                    print(reply[1])
                    


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