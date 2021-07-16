import random
import socket
import struct
import time

FANDATA_FMT = "hhhhhhhhhh"

fan_ip = [ '192.168.1.103', '192.168.1.104', '192.168.1.105']

def setfans(sock, number, data):
    # Target
    target_port = 8888
    target_ip = fan_ip[number]

    # Data
    print('Fans ', number, ' -> ' ,target_ip, ': ', data)
    
    # Sending
    try:
        ip_data = struct.pack(FANDATA_FMT, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])
        sock.sendto(ip_data, (target_ip, target_port))
    except Exception as e:
        print('Failed to send to',target_ip, e)


def getfans(sock):
    try:
        rcv_data, addr = sock.recvfrom(20)
        rcv_count, rcv_val, val2, val3, val4, val5, val6, val7, val8, val9 = struct.unpack(FANDATA_FMT, rcv_data)
        print('I received count ' + str(rcv_count) + ' and value ' + str(rcv_val) + "," + str(val3) + " from " + str(addr))
        return True
    except Exception as e:
        #print('No reply', e)
        return False


def loop(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.bind(('', port))
   
    count = 0
    
    timetick = time.time() + 1
    while True:
        
        if time.time() > timetick:
            timetick += 0.25
            
            val = random.randint(0,100)
            data = [count, val, 2,3,4,5,6,7,8,9]
            
            # Send to all modules
            i = 0
            for ip in fan_ip:
                setfans(sock, i, data)
                i+=1
            
            count += 1

        #time.sleep(1)

        
        gotdata = getfans(sock)
        
        
        
loop(8000)

                                   