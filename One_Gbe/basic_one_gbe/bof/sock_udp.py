import socket
import sys
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('192.168.1.30', 1234)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections

f = open('data', 'ab')

while True:
    # Wait for a connection
    try:

        # Receive the data in small chunks and retransmit it
        while True:
            data = sock.recv(40)
            f.write(data[:])
            #print('{!r}'.format(data))

    finally:
        # Clean up the connection
        f.close()
        sock.close()
