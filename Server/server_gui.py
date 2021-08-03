import random
import socket
import struct
import time
from tkinter import *
#sudo apt-get install python-tk


# global variable
fan_value = 0


DEBUG = True
FANDATA_FMT = "HHHHHHHHHH"

fan_ip = [ '192.168.1.101','192.168.1.102', '192.168.1.103', '192.168.1.104', '192.168.1.105','192.168.1.106','192.168.1.107','192.168.1.108','192.168.1.109','192.168.1.110','192.168.1.111','192.168.1.112','192.168.1.113','192.168.1.114','192.168.1.115']


def setfans(sock, number, data):
    # Target
    target_port = 8888
    target_ip = fan_ip[number]

    # Data
    if DEBUG:
        print('Fans ', number, ' -> ' ,target_ip, ': ', data)
    
    # Sending
    try:
        ip_data = struct.pack(FANDATA_FMT, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])
        sock.sendto(ip_data, (target_ip, target_port))
    except Exception as e:
        if DEBUG:
            print('Failed to send to',target_ip, e)


def rpm(val):
    if val <= 0:
        return 0
    return round(15000000 / val,1)


def getfans(sock):
    try:
        rcv_data, addr = sock.recvfrom(20)
        status, rpm1, rpm2, rpm3, rpm4, rpm5, rpm6, rpm7, rpm8, rpm9 = struct.unpack(FANDATA_FMT, rcv_data)
        if DEBUG:
            print('I received', status, rpm(rpm1), rpm(rpm2), rpm(rpm3), rpm(rpm4), rpm(rpm5), rpm(rpm6), rpm(rpm7), rpm(rpm8), rpm(rpm9),"from", addr)
        return True
    except Exception as e:
        return False


###################################
## ETHERNET
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)
sock.bind(('', 8000))
   

    
def FANWALL_Send():
    global sock, fan_value
            
    data = [fan_value, fan_value, fan_value, fan_value, fan_value, fan_value, fan_value, fan_value, fan_value, fan_value]
            
    # Send to all modules
    i = 0
    for ip in fan_ip:
        setfans(sock, i, data)
        i+=1
        
def FANWALL_Send_Thread():
    FANWALL_Send()
    root.after(250, FANWALL_Send_Thread)
    
    

def FANWALL_Read_Thread():
    gotdata = getfans(sock)
    root.after(1, FANWALL_Read_Thread)


        
def throttle(var):
    global fan_value
    fan_value = int(var)
    FANWALL_Send()


status = 0
def toggle():
    global status
    if status == 0:
        throttle(1023)
        status = 1
    else:
        throttle(400)
        status = 0
    
    root.after(1000, toggle)


root = Tk()
root.title("FAN WALL")
root.geometry("400x400")

vertical = Scale(root, from_=0, to=1023, command=throttle)
vertical.pack()

root.after(0, FANWALL_Send_Thread)
root.after(0, FANWALL_Read_Thread)
#root.after(0, toggle)

root.mainloop()

        
loop(8000)

                                    