import socket
import time
import os

def determineDNS():
    status = str(os.system('sudo systemctl status named')).split('\n')

    if(status[0].find('could not be found')):
        return "Service not found on this host"

    for line in status:
        temp = line.split(": ")
        if(temp[0] == "Active"):
            return temp[1]

#Open configuration file, process it into relevant sysInfo dictionary entry (just port for now)
def popSysInfo():
    desc = open("client.conf", "r")
    temp = desc.readline().split("=")
    sysInfo = {}
    sysInfo[temp[0]] = temp[1]
    return sysInfo
    

if __name__ =='__main__':
    counter = 0

    sysInfo = popSysInfo()

    port = sysInfo['PORT']
    print("Port from conf: " + port)
    
    #Create socket for receiving requests from main server
    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new.bind(("", int(port)))
    new.listen()

    #Accept the server connection, TODO: authenticate based on IP of server specified in conf
    conn, addr = new.accept()
    while(1):
        info = conn.recv(1024)

        #If connection is over (null message) break
        if info == b'':
            print("Session over")
            break
        
        print("Received: " + str(info))
        
        dnsRes = ""
        #Change this to determine function from request based on hashmap
        if(info.decode('utf-8').split("|")[1] == "dns"):
            dnsRes = determineDNS()

        print("dnsRes = " + str(dnsRes))
        #Send back information gathered on the system
        conn.send(b"Info about system: DNS = "+bytes(str(dnsRes), 'utf-8')+b"\n")
        counter+=1
        
