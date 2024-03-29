import socket
import threading
import string

servicePorts = {"icmp_echo": None}

controlledHosts = []

def initClients():
    desc = open("controlled-hosts.txt", "r")
    retArr = []
    line = desc.readline()
    while line:
        retArr.append(str(line).split(","))
        line = desc.readline()
    return retArr
    

def threadFunc(conn, addr):
    print("Hello from threadFunc", flush=True)
    data = None
    while(data != b''):
        data = conn.recv(1024)
        print(data, flush=True)
        conn.sendall(data+b": Rated 10/10")
    return


def server():
    print("Starting server\n")
    clients = initClients()
    print("Hosts managed: " + str(clients))
    connCount = 0
    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new.bind(("", 9015))
    new.listen()
    
    while True: 
        conn, addr = new.accept()
        connCount+=1
        print("Connection "+str(connCount)+" established", flush=True)
        threading.Thread(target=threadFunc, args=(conn, addr), name=('client_%d', connCount)).start()
        
    
    #start listening on port x 
    #every once and a while, send a gather info request
    #process the information returned and update the user about it
    


if __name__ == '__main__':
    server()