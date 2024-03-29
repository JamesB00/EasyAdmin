import socket
import time

if __name__ =='__main__':
    counter = 0

    desc = open("client.conf", "r")
    temp = desc.readline().split("=")
    sysInfo = {}
    sysInfo[temp[0]] = temp[1]
    port = sysInfo['PORT']
    print("Port from conf: " + port)

    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new.bind(("", 3030))
    new.listen()
    conn, addr = new.accept()
    while(1):
        new.send("Info about system: counter = "+str(counter)+"\n")
        counter+=1
        time.sleep(5)
        
