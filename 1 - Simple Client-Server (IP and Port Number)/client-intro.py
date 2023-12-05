#!/usr/bin/env python3
# client-intro.py

'''
This program is intended to help you learn about networking.
An example of this program is on my YouTube channel (in which 
I receive no revenue). I do this because I like to help. :)

Thank you,
Rick Graziani
'''


__author__ = "Rick Graziani"
__copyright__ = "Copyright 2022"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Rick Graziani"
__email__ = "graziani@cabrillo.edu rgrazian@ucsc.edu"
__status__ = "Production-Education"





import socket

# Option
# server_IP = "127.0.0.1"  # The server's hostname or IP address
# server_Port = 65432  # The port used by the server

print("\033c", end="")
print(f"\n***************** CLIENT *****************")

# SOCKET created
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # CONNECTing to IP {HOST}, destination PORT {PORT} 
    # TCP 3-way handshake
    
    server_IP = input("3. What is the IP address of the server? ")
    server_Port = int(input("   What is the TCP port number of the server? "))
    
    print(f"\nI am a CLIENT and ready to connect TO SERVER at:")
    print(f"   Destination IP address: {server_IP}")
    print(f"   Destination TCP port:   {server_Port}")
    print("\n******************************************************")
    print("4. Press return to make a connection to the SERVER ")
    anykey = input("******************************************************\n")
    
    # Making a connection with the SERVER...
    s.connect((server_IP, server_Port))

    # SENDing data TO SERVER
    print(f"\n5. Connection made with the Server!")

    print("\n******************************************************")
    print("6. Press return to send REQUEST for information to Server")
    print("   Request: What was your favorite class in school?")
    anykey = input("******************************************************\n")
    print(f"   REQUEST SENT... ")
    s.sendall(b" Request: What was your favorite class in school? ")

    # RECVing data FROM SERVER
    data_fromServer = s.recv(1024)

print(f"\n9. Received RESPONSE from Server...")
print(f"   {data_fromServer!r}")

# Connection will timeout and be closed
# CLOSEd connection by Server
print("\n")