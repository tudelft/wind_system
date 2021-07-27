# import socket
# 
# def send(data, port=50000, addr='239.192.1.100'):
#         """send(data[, port[, addr]]) - multicasts a UDP datagram."""
#         # Create the socket
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         # Make the socket multicast-aware, and set TTL.
#         s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20) # Change TTL (=20) to suit
#         # Send the data
#         s.sendto(data, (addr, port))
# 
# def recv(port=50000, addr="239.192.1.100", buf_size=1024):
#         """recv([port[, addr[,buf_size]]]) - waits for a datagram and returns the data."""
# 
#         # Create the socket
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 
#         # Set some options to make it multicast-friendly
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         try:
#                 s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
#         except AttributeError:
#                 pass # Some systems don't support SO_REUSEPORT
#         s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
#         s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)
# 
#         # Bind to the port
#         s.bind(('', port))
# 
#         # Set some more multicast options
#         intf = socket.gethostbyname(socket.gethostname())
#         s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(intf))
#         s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton(intf))
# 
#         # Receive the data, then unregister multicast receive membership, then close the port
#         data, sender_addr = s.recvfrom(buf_size)
#         s.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))
#         s.close()
#         return data
#     
# while True:
#     print(recv(8888, "169.254.179.148", 1024))

import socket

UDP_IP = "169.254.179.148"
UDP_PORT = 8000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    print("aaa")
    try:
        # This is where the shit happens
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print(data)
    except(ValueError):
        continue
