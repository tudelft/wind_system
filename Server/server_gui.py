import random
import socket
import struct
import time
import numpy as np
from tkinter import *
#sudo apt-get install python-tk


# global variable
fan_value = 0

pwmValues = " ";
rpmValues = " ";

DEBUG = True
FANDATA_FMT = "HHHHHHHHHH"

fan_ip = [ '192.168.1.101','192.168.1.102', '192.168.1.103', '192.168.1.104', '192.168.1.105','192.168.1.106','192.168.1.107','192.168.1.108','192.168.1.109','192.168.1.110','192.168.1.111','192.168.1.112','192.168.1.113','192.168.1.114','192.168.1.115']


def setfans(sock, number, data):
    # Target
    target_port = 8888
    target_ip = fan_ip[number]

    # Data
    if DEBUG:
        printPWM(number, target_ip, data)
    
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
            printRPM(status, rpm(rpm1), rpm(rpm2), rpm(rpm3), rpm(rpm4), rpm(rpm5), rpm(rpm6), rpm(rpm7), rpm(rpm8), rpm(rpm9), addr)
        return True
    except Exception as e:
        return False


#def printRpm(rpm1, rpm2, rpm3,rpm4,rpm5,rpm6,rpm7,rpm8,rpm9,addr):
#    rpmValues = rpmvalues.join('I received', status, rpm(rpm1), rpm(rpm2), rpm(rpm3), rpm(rpm4), rpm(rpm5), rpm(rpm6), rpm(rpm7), rpm(rpm8), rpm(rpm9),"from", addr,"/n") 

def printPWM(number, target_ip, data):
    global pwmValues
    pwmValues = pwmValues +  'PWM Module ' + str(number) + ' -> '
    for ip in target_ip:
        pwmValues += str(ip)
    
    pwmValues = pwmValues + ': '
    for d in data:
        pwmValues += str(d) + " "
    pwmValues = pwmValues + "\n"
    print('Fans!', number, ' -> ' ,target_ip, ': ', data)
    savePWM(pwmValues)

def printRPM(status, rpm1, rpm2, rpm3, rpm4, rpm5, rpm6, rpm7, rpm8, rpm9, addr):
    global rpmValues
    rpmValues += str(status) + ", " \
                + str((rpm1)) + ", "\
                + str((rpm2)) + ", "\
                + str((rpm3)) + ", "\
                + str((rpm4)) + ", "\
                + str((rpm5)) + ", "\
                + str((rpm6)) + ", "\
                + str((rpm7)) + ", "\
                + str((rpm7)) + ", "\
                + str((rpm8)) + ", "\
                + str((rpm9)) + ", "\
                + str(addr) + "\n"
    saveRPM(rpmValues)
  
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
    
    root.after(2000, toggle)

def step():
    global status
    if status == 0:
        throttle(1023)
        status = 1
    else:
        throttle(0)
        status = 0
    
    root.after(20000, step)

def continous():
    throttle(300)
    root.after(20000,continous)

# wait for certain number of seconds before changing PWM
WAIT_GAP = 10 
def step_increase():
	start_time = timer()
    current_time = timer()
    while True:
        elapsed_time = current_time - start_time
        if elapsed_time <= WAIT_GAP:
            throttle(200)
            current_time = timer()
        elif WAIT_GAP < elapsed_time <= 2 * WAIT_GAP:
            throttle(250)
            current_time = timer()
        elif 2 * WAIT_GAP < elapsed_time <= 3 * WAIT_GAP:
            throttle(300)
            current_time = timer()
        elif 3 * WAIT_GAP < elapsed_time <= 4 * WAIT_GAP:
            throttle(350)
            current_time = timer()
        else:
            throttle(350)
            break
    
def savePWM(Values):     
    with open('PWM_data.dat', 'w') as f: #w-writing mode, b- binary mode
        f.write(" FAN DATA \n PWM x15\n")
        f.write(Values)
        f.flush()
    
def saveRPM(Values):
    with open('RPM_data.dat', 'w') as f: #w-writing mode, b- binary mode
        f.write(" FAN DATA \n TACHO x15 \n") 
        f.write(Values) 
        f.flush()

root = Tk()
root.title("FAN WALL")
root.geometry("400x400")

vertical = Scale(root, from_=0, to=1023, command=throttle)

vertical.pack()
root.after(0, FANWALL_Send_Thread)
root.after(0, FANWALL_Read_Thread)
#root.after(0, toggle)
#root.after(0, step)
#root.after(0, continous)
root.after(0,step_increase)

root.mainloop()

        
loop(8000)

                                    