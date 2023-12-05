#!/usr/bin/env python3
# netstat-client.py

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
import subprocess
import os
import re
from prettytable import PrettyTable
import ipaddress
#import io
#import sys
#import time


# Get local IPv4
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



# Create formatted table
table = PrettyTable()

# Clear screen
print("\033c", end="")
print(f"\n************************ CLIENT ************************")

# Get local IP address
local_ip = get_local_ip()

# Create IPv4 client socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # Validate IP address is a proper address
    while True:
        server_IP = input("\n3. What is the IP address of the server? ")
        if server_IP == exit:
            exit()

        try:
            # try to create an IPv4 address object
            ip_address = ipaddress.IPv4Address(server_IP)
            #print(f"{server_IP} is a valid IPv4 address")
            break
        except ipaddress.AddressValueError:
            # the address is not a valid IPv4 address
            print(f"    {server_IP} is not a valid IPv4 address... please try again.")
    
    server_Port = int(input("   Which application on the server? \n   The TCP port number the server is listening on? "))
    
    # Create string of IP and Port for netstat command
    server_IP_string = str(server_IP)
    server_Port_string = str(server_Port)
    server_socket_string = server_IP_string + '.' + server_Port_string
    
    # Use netstat command based on OS
    if platform.system() == 'Windows':
        netstat_command = "netstat -naW | findstr {server_Port}"
    else:
        netstat_command = "netstat -nal | grep " + server_Port_string + " | grep ESTABLISHED"

    # Check OS to display with netstat command
    if platform.system() == 'Darwin':
        my_os = "MacOS"
    elif platform.system() == 'Windows':
        my_os = 'Windows'
    else:
        my_os = "Linux"

    
    if local_ip == server_IP_string:
        local_ip = '172.16.1.100'
    
    #print("\n******************************************************")
    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(f'   Local IP is {local_ip}')
    print("   Press return to make a connection to the SERVER ")
    #print("             >>> TCP 3-way handshake <<<")
    anykey = input("- - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
    print('Connection requested...')
    #anykey = input("******************************************************\n")

    
    # run the ping command with a timeout of 2 seconds and suppress output
    ping = subprocess.run(["ping", "-c", "1", "-W", "2", server_IP], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # check the return code of the ping command
    if ping.returncode == 0:
        #print(f"{server_IP} is reachable")
        pass
    else:
        print(f"{server_IP} is not reachable\n")
        exit()
    
    # If address verified attempt connection
    
    s.settimeout(5)

    try:
        s.connect((server_IP, server_Port))
    except:
        print(f"\nConnection refused by {server_IP} on port {server_Port}\n")
        exit()


    ###### ESTABLISHED STATE #######  

    print("\n************* Connection Established ******************")

    print(f"\nTCP 3-way handshake successful: Connected to server at {server_IP} port {server_Port}")
    
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
    
        if columns[4] == server_socket_string:
    
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
            
            # If destin IP same as source IP (using local computer for both) fake the source IP
            if destin_ipv4 == source_ipv4:
                source_ipv4 = "172.16.1.100"       

            # Store destin port aftter 4th period
            destin_port = ".".join(split_string[4:])  
    
            # State of TCP connection
            state = columns[5]
    
            table.add_row([proto, source_ipv4, source_port, destin_ipv4, destin_port, state])
    
    # Print netstat table after connection with server
    print(table)
    
    
    # Send data to Server 
    print(f"\n4. I can now send data TO SERVER...")
    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("   Press return to send REQUEST for information to Server.")
    anykey = input("- - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")
    print(f"   Sent '>>>>>> Hello SERVER ")
          
    s.sendall(b" >>>>>> Hello SERVER ")

    # Receive data from Server
    data_fromServer = s.recv(1024)


# Receive data from server - Server closes connection
print(f"\n7. Received data FROM SERVER...")
print(f"   {data_fromServer!r}")

print("\n************* Timeout and Close ******************")
print(f"\n9. Simulating a timeout and Connection will be closed.")


###### No (CLOSED) STATE ####### 

# Display netstat output after connection is closed

table2 = PrettyTable()

# Run the netstat command and retrieve its output
netstat_output = os.popen(netstat_command).read()
print(f'\n{my_os}: {netstat_command}')
 
# Divide netstat output into separate lines to later parse each line at a time    
lines = netstat_output.split("\n")
    
table2.field_names = ["Protocol", "Source IP", "Source Port", "Destination IP", "Dest. Port", "State"]

# Parse netstat output for desintation IPv4 and port   
# See previous commented code     
for line in lines:
        
    if 'Proto' in line or not line:
        continue
        
    columns = re.split(r'\s+', line)
    
    if columns[4] == server_socket_string:
    
        proto = "IPv4 TCP"
    
        split_string = columns[3].split(".")
            
        source_ipv4 = ".".join(split_string[:4])   

        source_port = ".".join(split_string[4:])
         
        split_string = columns[4].split(".")
                    
        destin_ipv4 = ".".join(split_string[:4])
           
        if destin_ipv4 == source_ipv4:
            source_ipv4 = "172.16.1.100"       

        destin_port = ".".join(split_string[4:])
     
        state = columns[5]
    
        table2.add_row([proto, source_ipv4, source_port, destin_ipv4, destin_port, state])
    
print(table2)
print('\nThis session is over. Go do something else :)\n')