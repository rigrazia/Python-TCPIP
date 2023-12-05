#!/usr/bin/env python3
# netstat-server.py

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
import platform
import os
import re
from prettytable import PrettyTable

# Create formatted table
table = PrettyTable()

# Create temporary socket to get IP address of this device
s_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s_temp.connect(("8.8.8.8", 80))
server_IP = s_temp.getsockname()[0]

# Clear screen
print("\033c", end="")
print(f"\n********************** SERVER STARTED ***********************")

print("\n1. What application, TCP port will this server listen on? (1024 to 65535)")
print("   Note: Well-known port numbers 0 to 1023 require OS permissions.")

# Validate port range
while True:
    server_Port = int(input("Enter TCP port number: "))
    
    if server_Port >= 1024 and server_Port <= 65535:
        break
    else:
        print(f'{server_Port} is an invalid port. Select between 1024 to 65535.')



# Create IPv4 serversocket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Socket - IP + Port
    s.bind((server_IP, server_Port))
   
    # Listen on this socket
    s.listen()

    print(f"\n2. I am listening (waiting for client) on:")
    print(f"   My IP address: {server_IP}")
    print(f"   My TCP port:   {server_Port}")
    
    # Create string of IP and Port for netstat command
    server_IP_string = str(server_IP)
    server_Port_string = str(server_Port)
    server_socket_string = server_IP_string + '.' + server_Port_string
    
    # Use netstat command based on OS
    if platform.system() == 'Windows':
        netstat_command = "netstat -naW | findstr {server_Port}"
    else:
        #netstat_command = "netstat -nal | grep " + server_Port_string + " | grep ESTABLISHED"
        netstat_command = "netstat -nal | grep " + server_IP_string + '.' + server_Port_string 

    # Check OS to display with netstat command
    if platform.system() == 'Darwin':
        my_os = "MacOS"
    elif platform.system() == 'Windows':
        my_os = 'Windows'
    else:
        my_os = "Linux"
    
    ###### LISTENING STATE #######

    # Run the netstat command and retrieve its output
    netstat_output = os.popen(netstat_command).read()
    print(f'\n{my_os}: {netstat_command}')

    # Divide netstat output into separate lines to later parse each line at a time
    lines = netstat_output.split("\n")
        
    # Table header
    table.field_names = ["Protocol", "Source IP", "Source Port", "Destination IP", "Dest. Port", "State"]
    
    # Parse netstat output for desintation IPv4 and port      
    for line in lines:
        
        if 'Proto' in line or not line:
            continue
        
        # Divide nestat output into columns using spaces the delimiter
        columns = re.split(r'\s+', line)
    
        if columns[3] == server_socket_string:

            # Assume IPv4 for now (tcp4)
            proto = "IPv4 TCP"
                
            # SOURCE IP and PORT
        
            # Columns 3 is source-IPv4.source-sort I.I.I.I.P
            split_string = columns[3].split(".")
            
            # Store source IPv4 up to 4th period    
            source_ipv4 = ".".join(split_string[:4])
     
            # Store source port aftter 4th period
            source_port = ".".join(split_string[4:])


            # DESTINATION IP and PORT
            
            # Columns 4 is destin-IPv4.destub-sort I.I.I.I.P     
            split_string = columns[4].split(".")
            
            # Store destin IPv4 up to 4th period          
            destin_ipv4 = ".".join(split_string[:4])
            if destin_ipv4 == '*.*':
                destin_ipv4 = '*'
       
            # Store destin port aftter 4th period
            destin_port = ".".join(split_string[4:])
            if destin_port == '':
                destin_port = '*'
 
            # State of TCP connection
            state = columns[5]
        
            table.add_row([proto, source_ipv4, source_port, destin_ipv4, destin_port, state])
                
    print(table)
    
    
    # Client makes connection
    conn, addr = s.accept()
    
    
    ###### ESTABLISHED AND LISTENING STATE #######
    
    
    with conn:
        
        # Run the netstat command and retrieve its output
        netstat_output = os.popen(netstat_command).read()

        # Divide netstat output into separate lines to later parse each line at a time
        lines = netstat_output.split("\n")
        
        # New table showing Established and Listen states
        table2 = PrettyTable()
        table2.field_names = ["Protocol", "Source IP", "Source Port", "Destination IP", "Dest. Port", "State"]
        
        # Parse netstat output for desintation IPv4 and port   
        # See previous commented code
        for line in lines:
        
            if 'Proto' in line or not line:
                continue
        
            columns = re.split(r'\s+', line)
    
            if columns[3] == server_socket_string:

                proto = "IPv4 TCP"
                       
                split_string = columns[3].split(".")
                
                source_ipv4 = ".".join(split_string[:4])
       
                source_port = ".".join(split_string[4:])

                
                split_string = columns[4].split(".")
                        
                destin_ipv4 = ".".join(split_string[:4])
                if destin_ipv4 == '*.*':
                    destin_ipv4 = '*'     

                destin_port = ".".join(split_string[4:])
                if destin_port == '':
                    destin_port = '*'

                # If destin IP same as source IP (using local computer for both) fake the source IP 
                if destin_ipv4 == source_ipv4:
                    destin_ipv4 = "172.16.1.100"  
            
                state = columns[5]
        
                table2.add_row([proto, source_ipv4, source_port, destin_ipv4, destin_port, state])
                
                # Save Established IP and Port - Next line is a listen and previous variables are changed 
                if columns[5] == "ESTABLISHED":
                    connected_ipv4 = destin_ipv4
                    connected_port = destin_port
        
        print("\n\n************* Connection Established ******************")
        
        print(f'\nTCP 3-way handshake successful: Connected to client at {connected_ipv4} on their port {connected_port}')
        
        print(f'\n{my_os}: {netstat_command}')        
        print(table2)

        # Used to set whether any more data was received from client
        step = "10"
        
        while True:
            
            # Data received from client
            data_fromClient = conn.recv(1024)


            if step == "10":
                print("\n5. Receiving data FROM CLIENT...")
                # Step 13 means no more data from client for next iteration of while
                step = "13"
            else:
                print("\n************* Timeout and Close ******************")
                print("\n8. I will simulate a timeout and close the connection..")
            
            # Display data sent from client
            print(f"   {data_fromClient}")
            
            # Exit while of no more data from client
            if not data_fromClient:
                break
            
            # Server automatically responds with data to client
            print(f"\n6. My turn to send data TO CLIENT... ")
            print(f"   Sent 'Hello CLIENT! <<<<<' TO CLIENT")
            
            data_toServer = " Hello Client! <<<<<"

            conn.sendall(data_toServer.encode('utf-8'))


###### LISTENING STATE #######

# Create a new socket and listening on same IP and Port (next version - just close existing connection)
# See previous commented code
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((server_IP, server_Port))
   
    s.listen()

    # Run the netstat command and retrieve its output
    netstat_output = os.popen(netstat_command).read()

    lines = netstat_output.split("\n")
         
    # New table - just listening
    table3 = PrettyTable()
    table3.field_names = ["Protocol", "Source IP", "Source Port", "Destination IP", "Dest. Port", "State"]
            
    for line in lines:
            
        if 'Proto' in line or not line:
            continue
            
        columns = re.split(r'\s+', line)
        
        if columns[3] == server_socket_string:

            proto = "IPv4 TCP"
            
            split_string = columns[3].split(".")
                    
            source_ipv4 = ".".join(split_string[:4])
       
            source_port = ".".join(split_string[4:])

                   
            split_string = columns[4].split(".")
                            
            destin_ipv4 = ".".join(split_string[:4])
            if destin_ipv4 == '*.*':
                destin_ipv4 = '*'
      
            destin_port = ".".join(split_string[4:])
            if destin_port == '':
                destin_port = '*'
  
                    
            if destin_ipv4 == source_ipv4:
                destin_ipv4 = "172.16.1.100"  
                
            state = columns[5]
            
            table3.add_row([proto, source_ipv4, source_port, destin_ipv4, destin_port, state])
            

            
    print(f'\n{my_os}: {netstat_command}')        
    print(table3)
    print(f'\nListening and waiting for another client to connect to me at {server_IP} on my port {server_Port}\n')