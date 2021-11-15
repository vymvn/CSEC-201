import socket

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(("localhost", 6666))
ss.listen()
start_packet = ss.recv(1024)
print(start_packet)