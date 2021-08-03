import random
import socket
import struct
import time

DEBUG = True
FANDATA_FMT = "hhhhhhhhhh"

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


def getfans(sock):
    try:
        rcv_data, addr = sock.recvfrom(20)
        status, rpm1, rpm2, rpm3, rpm4, rpm5, rpm6, rpm7, rpm8, rpm9 = struct.unpack(FANDATA_FMT, rcv_data)
        if DEBUG:
            print('I received', status, rpm1, rpm2, rpm3, rpm4, rpm5, rpm6, rpm7, rpm8, rpm9,"from", addr)
        return True
    except Exception as e:
        return False

ROWS = 9
COLS = 15


# TODO: modulate the wall

fans = [ [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         ]

def fan_init( val ):
    global fans
    for x in range(0,COLS):
        for y in range(0,ROWS):
            fans[y][x] = val
            
fan_init(10)

def fan_print(fans):
    for r in fans:
        print(r)
 

fan_print(fans)

def loop(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.bind(('', port))
   
    count = 0
    
    timetick = time.time() + 1
    while True:
        
        if time.time() > timetick:
            timetick += 2.0 # in seconds: e.g. 0.05 = 20Hz
            
            val = random.randint(0,100)
            data = [count, 400, 0, 400, 0, 1000, 0, 400 , 0, 400]
            data = [count, 400, 0, 400, 0, 1000, 0, 400 , 0, 400]
            data = [count, 400, 0, 0, 0, 0, 0, 0 , 0, 0]
            data = [count, 400, 400, 400, 400, 400, 400, 400 , 400, 400]
            #data = [count, 800, 800, 800, 800, 800, 800, 800 , 800, 800]

            
            # Send to all modules
            i = 0
            for ip in fan_ip:
                setfans(sock, i, data)
                i+=1
            
            count += 1

        #time.sleep(1)

        for ip in fan_ip:
            gotdata = getfans(sock)
        
        
        
loop(8000)

                                   