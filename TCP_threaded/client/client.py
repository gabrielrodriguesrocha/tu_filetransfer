import socket
import sys
import time

def client(host, port):
    size = 1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    if (sys.argv[1] == 'SEND'):
        try:
            f = open(sys.argv[2], "rb")
        except:
            raise error('File does not exist')
            sock.close()
        print ("Sending file: " + sys.argv[2])
        sock.send(sys.argv[1] + "\n" + sys.argv[2] + "\n")
        start = time.time()
        sender(sock, f, size)
        end = time.time()
        print("Elapsed time: " + str(end - start) + " seconds")
    elif (sys.argv[1] == 'GET'):
        try:
            f = open(sys.argv[2], "wb")
        except:
            raise error('File does not exist')
            sock.close()
        print ("Receiving file: " + sys.argv[2])
        sock.send(sys.argv[1] + "\n" + sys.argv[2] + "\n")
        start = time.time()
        receiver(sock, f, size)
        end = time.time()
        print("Elapsed time: " + str(end - start) + " seconds")
    elif (sys.argv[1] == 'LIST'):
        print ("Files in server:\n")
        sock.send(sys.argv[1] + "\n")
        start = time.time()
        filelist(sock, size)
        end = time.time()
        print("Elapsed time: " + str(end - start) + " seconds")
    else:
        print ("Unrecognized command: " + sys.argv[1])
        print ("Expected GET, SEND or LIST")

def receiver(sock, f, size):
    while True:
        try:
            data = sock.recv(size)
            if data:
                f.write(data)
            else:
                raise error('Server disconnected')
        except:
            f.close()
            sock.shutdown(socket.SHUT_WR)
            sock.close()
            return False

def sender(sock, f, size):
    while True:
        try:
            data = f.read(size)
            if data:
                sock.send(data)
            else:
                raise error('Server disconnected')
        except:
            f.close()
            sock.shutdown(socket.SHUT_WR)
            sock.close()
            return False

def filelist(sock, size):
    while True:
        try:
            data = sock.recv(size)
            if data:
                print(data)
            else:
                raise error('Server disconnected')
        except:
            sock.shutdown(socket.SHUT_WR)
            sock.close()
            return False

if __name__ == "__main__":
    if (len(sys.argv) < 2): 
        print ("Usage: python client.py <GET | SEND | LIST> <filename>")
    else:
        client(socket.gethostname(), 2000)