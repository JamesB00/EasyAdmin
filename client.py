import socket
import time
import os

serviceDict = {
    "dns": ["named", "bind"], 
    "nft": ["nftables"],
    "http": ["httpd", "apache2"],
    "dhcp": ["dhcpd", "iso-dhcp"]
    }

timerVal = 0

#Returns the status of specified service (for now just uses systemctl, will expand later)
def determineServiceStatus(service):
    found = False
    for alias in serviceDict[service]:
        status = str(os.system(("sudo systemctl status " + alias))).split('\n')
        if not (status[0].find('could not be found')):
            found = True

    if found == False:
        return None

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
        
        services = info.decode('utf-8').split("|")[1:]
        
        sendPacket = "System info:\n"

        #Get service statuses
        for service in services:
            if service == "":
                continue
            stat = determineServiceStatus(service)
            if not stat:
                sendPacket += service + " was not found on machine\n"
                continue
            sendPacket += service + " status: " + stat + "\n"

        #Send back information gathered on the system
        conn.send(bytes(sendPacket, 'utf-8'))
        counter+=1
        
