import socket


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 6666
serversocket.bind((host, port))
serversocket.listen()
clientsocket, addr = serversocket.accept()
print(f"Got a connection from {addr}")
data_string = clientsocket.recv(2024)
print(data_string)