import socket
import threading
import string
import time

servicePorts = {"icmp_echo": None}

controlledHosts = []

#Initialize the clients based on the controlled-hosts.txt file located in current directory
def initClients():
    desc = open("controlled-hosts.txt", "r")
    retArr = []
    line = desc.readline()
    while line:
        retArr.append(str(line).split(","))
        line = desc.readline()
    return retArr

#Simple echo for now, later will take on requests and sudden error reporting
def threadFunc(conn, addr):
    print("Hello from threadFunc", flush=True)
    data = None
    while(data != b''):
        data = conn.recv(1024)
        print(data, flush=True)
        conn.sendall(data+b": Rated 10/10")
    return

def clientOutreach(clients):
    #Persistent
    while True:
        #Go through the clients provided by initialization in main
        for client in clients:
            addr = client[1]
            port = client[2]

            print("Sending outreach to "+addr+" on port "+port, flush=True)
            
            #Create socket for communication
            est = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                #Connect to the client at the specified port and address
                est.connect((addr, int(port)))

                #CHECK prefix denotes client-outreach communication
                strToSend = "CHECK|"

                #Gather services to be checked (specified in conf), send outreach message
                for i in range (len(client)):
                    if i < 3:
                        continue
                    strToSend+=str(client[i]).rstrip("\n")+"|"  
                print("Outreach message: " + strToSend)
                est.sendall(bytes(strToSend, "utf-8"))
                
                #Gather data returned from client, process it, close socket and move on
                retdata = est.recv(1024)
                print(retdata.decode("utf-8"))
                est.close()
            except:
                print("Host " + addr + " is unavailable, make sure EasyAdmin software is running on this machine")
                continue

        #Wait 10 seconds before doing the outreach again
        time.sleep(10)


def server():
    print("Starting server\n")

    #Build Hosts from config file
    clients = initClients()
    print("Hosts managed: " + str(clients))

    #Over-time client outreach thread
    threading.Thread(target=clientOutreach, args=[clients], name="Client_Outreach_Thread").start()

    #For counting and naming connections
    connCount = 0

    #Main thread socket
    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new.bind(("", 9015))
    new.listen()
    
    #Main thread for real time error reporting
    while True: 
        #Accept the connection, TODO: authentication based on IP addresses
        conn, addr = new.accept()
        connCount+=1
        print("Connection "+str(connCount)+" established", flush=True)
        threading.Thread(target=threadFunc, args=(conn, addr), name=('client_%d', connCount)).start()

if __name__ == '__main__':
    server()