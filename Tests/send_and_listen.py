import socket


# print(socket.gethostname())

HOST = '' # '169.254.179.148' # '192.168.0.177' # '169.254.255.255'
PORT =  8888

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.connect((HOST, PORT))
    print("Binded!")
    while True:
        print("while...")
        rcv_data, rcv_addr = sock.recvfrom(1024)
        print("Received", repr(rcv_data))


