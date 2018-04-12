import socket
import time
import os

def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print ("Listening on %s : %d" % (host, port))
    listen(sock)

def listen(sock):
    while True:
        handle(sock)

def handle(sock):
    size = 1024
    try: 
        data, address = sock.recvfrom(size)
        print ("Request from " + address[0])
        sp = data.split('\n')
        if sp[0] == 'GET':
            print ("Sending file %s" % (sp[1]))
            f = open(sp[1], 'rb')
            start = time.time()
            sender(sock, address, f, size)
            end = time.time()
            print("Elapsed time: " + str(end - start) + " seconds")
        elif sp[0] == 'SEND':
            print ("Receiving file %s" % (sp[1]))
            f = open(sp[1], 'wb')
            start = time.time()
            receiver(sock, f, size)
            end = time.time()
            print("Elapsed time: " + str(end - start) + " seconds")
        elif sp[0] == 'LIST':
            print ("Sending file list")
            start = time.time()
            filelist(sock, size)
            end = time.time()
            print("Elapsed time: " + str(end - start) + " seconds")
        else:
            raise error("Expected GET, SEND or LIST")
    except:
        return False

def receiver(sock, f, size):
    while True:
        try:
            data = sock.recv(size)
            sock.settimeout(1)
            if data:
                f.write(data)
            else:
                raise error('Communication ended abruptly')
        except:
            print ("Done!")
            f.close()
            return False

def sender(sock, address, f, size):
    while True:
        try:
            data = f.read(size)
            if data:
                sock.sendto(data, address)
            else:
                raise error('Communication ended abruptly')
        except:
            print ("Done!")
            sock.close()
            f.close()
            return False

def filelist(sock, size):
    current_dir = os.listdir(os.getcwd())
    data = ""
    for x in current_dir:
        data = data + x + "\n"
    try:
        if data:
            sock.send(data)
            print("Sent data")
            sock.close()
        else:
            raise error('Client disconnected')
    except:
        print("Error")
        sock.close()
        return False

if __name__ == "__main__":
    server(socket.gethostname(), 2000)
