import socket 
import sys
ip = 'localhost'
port = 12345
if __name__ == '__main__':
    cmd = sys.argv[1]
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    client.sendall(cmd.encode())
    data = client.recv(1024)
    print(data)
    