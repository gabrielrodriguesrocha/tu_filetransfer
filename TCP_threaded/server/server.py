import socket
import threading
import os
import time

def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    print ("Listening on %s : %d" % (host, port))
    listen(sock)

def listen(sock):
    sock.listen(5)
    while True:
        client, address = sock.accept()
        client.settimeout(60)
        threading.Thread(target = handle,args = (client,address)).start()

def handle(client, address):
    size = 1024
    print ("Request from " + address[0])
    try: 
        data = client.recv(size)
        sp = data.split('\n')
        if sp[0] == 'GET':
            print ("Sending file %s" % (sp[1]))
            f = open(sp[1], 'rb')
            start = time.time()
            sender(client, f, size)
            end = time.time()
            print("Elapsed time: " + str(end - start) + " seconds")
        elif sp[0] == 'SEND':
            print ("Receiving file %s" % (sp[1]))
            start = time.time()
            f = open(sp[1], 'wb')
            receiver(client, f, size)
            end = time.time()
            print("Elapsed time: " + str(end - start) + " seconds")
        elif sp[0] == 'LIST':
            print ("Sending file list")
            start = time.time()
            filelist(client, size)
            end = time.time()
            print("Elapsed time: " + str(end - start) + " seconds")
        else:
            raise error("Expected GET, SEND or LIST")
    except:
        client.close()
        return False

def receiver(client, f, size):
    while True:
        try:
            data = client.recv(size)
            if data:
                f.write(data)
            else:
                raise error('Client disconnected')
        except:
            print ("Done!")
            f.close()
            client.close()
            return False

def sender(client, f, size):
    while True:
        try:
            data = f.read(size)
            if data:
                client.send(data)
            else:
                raise error('Client disconnected')
        except:
            print ("Done!")
            f.close()
            client.close()
            return False

def filelist(client, size):
    dir = os.listdir(os.getcwd())
    data = ""
    for file in dir:
        data = data + file + "\n"
    try:
        if data:
            client.send(data)
            client.close()
            print ("Done!")
        else:
            raise error('Client disconnected')
    except:
        client.close()
        return False



if __name__ == "__main__":
    server(socket.gethostname(), 2000)