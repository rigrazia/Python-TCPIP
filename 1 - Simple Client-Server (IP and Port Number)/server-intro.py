# server-intro.py
#!/usr/bin/env python3

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

# Optional
# server_IP = "127.0.0.1"  # Standard loopback interface address (localhost)
# server_Port = 65432  # Port to listen on (non-privileged ports are > 1023) 

s_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s_temp.connect(("8.8.8.8", 80))
server_IP = s_temp.getsockname()[0]

print("\033c", end="")
print(f"\n***************** SERVER STARTED *****************")

print("\n1. What TCP port will this server listen on? (suggest 65000 to 65500)")
server_Port = int(input("Enter TCP port number: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # BINDing {HOST},{PORT}
    s.bind((server_IP, server_Port))

   
    s.listen()
    # LISTENing on address {HOST} and port {PORT}"
    print(f"\n2. I am listening (waiting) on:")
    print(f"   My IP address: {server_IP}")
    print(f"   My TCP port:   {server_Port}")
    
    conn, addr = s.accept()
    # ACCEPTed connection from {addr}
    """
    print('''New socket object created used to communicate with the client. 
             It is distinct from the listening socket that the server is 
             using to accept new connections''')
    """
    
    with conn:
        # TCP Handshake 
        print(f"\n5. Connection made with a Client!")
        print(f"   Waiting for Request from this Client...")

        step = "10"
        
        while True:
            # RECVing data FROM CLIENT {data_fromClient}
            data_fromClient = conn.recv(1024)
            

            if step == "10":
                print("\n7. Received a Request from the Client...")
                step = "13"
            else:
                # done
                pass
            
            
            if not data_fromClient:
                # CLOSE connection...
                print("\n")
                break
            
            print(f"   {data_fromClient}")
            
            print("\n******************************************************")
            print("8. Press return to send my RESPONSE... ")
            print("   My favorite class was Introduction to Networking ")
            anykey = input("******************************************************\n")
            print(f"   RESPONSE SENT...")
            data_toServer = "My favorite class was Introduction to Networking"
            # SENDing data TO CLIENT: {data_toServer}
            conn.sendall(data_toServer.encode('utf-8'))

