import socket
import urllib.request
import threading


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IP = socket.gethostbyname(socket.gethostname())
PORT = 1337
ADDRESS = (IP, PORT)


def readContent(url, address):
        response = urllib.request.urlopen(url)
        content = response.read()
        serverSocket.sendto(content, address)
        print(f'Sent web conent to {address}')


def main():
    while True:
        data, address = serverSocket.recvfrom(4096)
        url = data.decode()
        print(f'Recevied {url} from {address}')
        readThread = threading.Thread(target=readContent, args=[url, address])
        readThread.start()


if __name__ == "__main__":
    main()