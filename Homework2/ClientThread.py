import socket, threading

class clientThread(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
    
    
    def run():
        data_string = socket.recv(2024)
        print(data_string.decode("utf-8"))