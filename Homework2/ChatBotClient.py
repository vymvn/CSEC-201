import socket

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
        algo = input("Please choose encryption algorithm (DES/Auth): : ")
        if algo.upper() == "DES":
            pub_key = input("Please provide your public key: ")
            encryption_packet = f"EC, DES, {pub_key}"
            s.send(encryption_packet.encode("utf-8"))
            SKpacket_string = s.recv(1024)
            SKpacket = SKpacket_string.decode().split()
            if SKpacket[0] == "SK":
                SK = SKpacket[1]
                print(f"Session key is: {SK}")
        elif algo.lower() == "auth":
            username = input("Username: ")
            password = input("Password: ")
            encryption_packet = f"EC, {algo.lower()}, {(username, password)}"
            s.send(encryption_packet.encode("utf-8"))
    confirmation_packet = process_packet_string(s.recv(1024))
    if confirmation_packet[0] == "CC":   
        print("Connected successfully!")
    elif confirmation_packet[0] == "EE":
        print("Error connecting")
    else:
        print("Unknown error")


def process_packet_string(packet_string):
    packet = packet_string.decode().split()
    return packet


def main():
    initConnection("localhost", 6666)
    setUpPhase()
    
if __name__ == "__main__":
    main()