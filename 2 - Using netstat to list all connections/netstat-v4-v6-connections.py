#!/usr/bin/env python3
# netstat-v4-v6-connections.py

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



import subprocess
import re
import platform
import os
import json
import urllib.request
from prettytable import PrettyTable


# Function to get the geolocation information of an IP address
def get_ip_geo(ip):
    # Make a request to the IP info API
    url = 'http://ipinfo.io/' + ip + '/json?token=5c116e8d7b9cd1' 
    try:
        response = urllib.request.urlopen(url)
        data = json.load(response)
        org = data['org']
        city = data['city']
        country = data['country']
        region = data['region']

        # Return the organization, city, country, and region of the IP
        return org, city, country, region
    except:
        # Return None if the request fails
        return None, None, None, None


'''
# Run the netstat command to get the list of connections
output = subprocess.check_output(['netstat', '-nal'])


# Decode the output from bytes to string
output = output.decode('utf-8')
print(output)

pause = input('press any key')
'''

print("\033c", end="")

as_org = input('Do you want AS information? (y/n) n ')
location = input('Do you want the AS location? (y/n): n ')



if platform.system() == 'Windows':
    netstat_command = "netstat -naW | findstr ESTABLISHED"
else:
    #netstat_command = "netstat -nal | grep ESTABLISHED"
    netstat_command = "netstat -nal"

# Run the netstat command and retrieve its output
netstat_output = os.popen(netstat_command).read()

lines = netstat_output.split("\n")

# Regular expression to match IPv6 addresses
ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4})$'

table = PrettyTable()
if location == 'y' and as_org == 'y': 
    table.field_names = ["Protocol", "Source IP", "Source Port", "Destination IP", "Dest. Port", "Organization", "City", "Country"]
    table.add_row(["IPv4 TCP", "", "", "", "", "", "", ""])
elif as_org == 'y':
    table.field_names = ["Protocol", "Source IP", "Source Port", "Destination IP", "Dest. Port", "Organization"]
    table.add_row(["IPv4 TCP", "", "", "", "", ""])
elif location == 'y':
    table.field_names = ["Protocol", "Source IP", "Source Port", "Destination IP", "Dest. Port", "City", "Country"]
    table.add_row(["IPv4 TCP", "", "", "", "", "", ""])
else:
    table.field_names = ["Protocol", "Source IP", "Source Port", "Destination IP", "Dest. Port"]
    table.add_row(["IPv4 TCP", "", "", "", ""])
    

#table.add_row(["IPv4 TCP", "", "", "", "", "", "", ""])

# IPv4 TCP - Loop through each line of the output
for line in lines:
    # Skip the header row and any empty rows
    if 'Proto' in line or not line:
        continue
    # Split the line into columns
    columns = re.split(r'\s+', line)
    
    # Check if the local and foreign addresses are IPv6 addresses
    #print("\nColumns", columns[0], columns[1], columns[2], columns[3],columns[4])
    
    
    if columns[0] == 'tcp4':

        proto = "IPv4 TCP"
        #print('\n', columns[0])
 
        split_string = columns[3].split(".")
        
        source_ipv4 = ".".join(split_string[:4])
        #print('Source IPv4 Address = ', source_ipv4)        

        source_port = ".".join(split_string[4:])
        #print('Source Port = ', source_port)


        
        split_string = columns[4].split(".")
                
        destin_ipv4 = ".".join(split_string[:4])
        #print('Destination IPv4 Address = ', destin_ipv4)        

        destin_port = ".".join(split_string[4:])
        #print('Destination Port = ', destin_port)

        org, city, country, region = get_ip_geo(destin_ipv4)

        #print(f'Org {org}, City {city}, Country {country}, Region {region}')

        if ('*' in source_ipv4 or '*' in source_port or '*' in destin_port or '*' in destin_ipv4) or (destin_ipv4.startswith('127.') == True):
        #if ('*' in source_ipv4 or '*' in source_port or '*' in destin_port or '*' in destin_ipv4):
            continue
        elif location == 'y' and as_org == 'y':
            table.add_row(["", source_ipv4, source_port, destin_ipv4, destin_port, org if org else "", city if city else "", country if country else ""])
        elif as_org == 'y':
            table.add_row(["", source_ipv4, source_port, destin_ipv4, destin_port, org if org else ""])
        elif location == 'y':
            table.add_row(["", source_ipv4, source_port, destin_ipv4, destin_port, city if city else "", country if country else ""])
        else:    
            table.add_row(["", source_ipv4, source_port, destin_ipv4, destin_port])




#table.add_row(["IPv4 UDP", "", "", "", "", "", "", ""])
if location == 'y' and as_org == 'y': 
    table.add_row(["IPv4 UDP", "", "", "", "", "", "", ""])
elif as_org == 'y':
    table.add_row(["IPv4 UDP", "", "", "", "", ""])
elif location == 'y':
    table.add_row(["IPv4 UDP", "", "", "", "", "", ""])
else:
    table.add_row(["IPv4 UDP", "", "", "", ""])



# IPv4 UDP - Loop through each line of the output
for line in lines:
    # Skip the header row and any empty rows
    if 'Proto' in line or not line:
        continue
    # Split the line into columns
    columns = re.split(r'\s+', line)
    
    # Check if the local and foreign addresses are IPv6 addresses
    #print("\nColumns", columns[0], columns[1], columns[2], columns[3],columns[4])
    
    
    if columns[0] == 'udp4':

        proto = "IPv4 UDP"
        #print('\n', columns[0])
 
        split_string = columns[3].split(".")
        
        source_ipv4 = ".".join(split_string[:4])
        #print('Source IPv4 Address = ', source_ipv4)        

        source_port = ".".join(split_string[4:])
        #print('Source Port = ', source_port)


        
        split_string = columns[4].split(".")
                
        destin_ipv4 = ".".join(split_string[:4])
        #print('Destination IPv4 Address = ', destin_ipv4)        

        destin_port = ".".join(split_string[4:])
        #print('Destination Port = ', destin_port)

        org, city, country, region = get_ip_geo(destin_ipv4)

        #print(f'Org {org}, City {city}, Country {country}, Region {region}')


        if ('*' in source_ipv4 or '*' in source_port or '*' in destin_port or '*' in destin_ipv4) or (destin_ipv4.startswith('127.') == True):
        #if ('*' in source_ipv4 or '*' in source_port or '*' in destin_port or '*' in destin_ipv4):
            continue
        elif location == 'y' and as_org == 'y':
            table.add_row(["", source_ipv4, source_port, destin_ipv4, destin_port, org if org else "", city if city else "", country if country else ""])
        elif as_org == 'y':
            table.add_row(["", source_ipv4, source_port, destin_ipv4, destin_port, org if org else ""])
        elif location == 'y':
            table.add_row(["", source_ipv4, source_port, destin_ipv4, destin_port, city if city else "", country if country else ""])
        else:    
            table.add_row(["", source_ipv4, source_port, destin_ipv4, destin_port])


#table.add_row(["IPv6 TCP", "", "", "", "", "", "", ""])
if location == 'y' and as_org == 'y': 
    table.add_row(["IPv6 TCP", "", "", "", "", "", "", ""])
elif as_org == 'y':
    table.add_row(["IPv6 TCP", "", "", "", "", ""])
elif location == 'y':
    table.add_row(["IPv6 TCP", "", "", "", "", "", ""])
else:
    table.add_row(["IPv6 TCP", "", "", "", ""])

# IPv6 TCP - Loop through each line of the output
for line in lines:
    # Skip the header row and any empty rows
    #print(line)
    if 'Proto' in line or not line:
        continue
    # Split the line into columns
    columns = re.split(r'\s+', line)
    
    # Check if the local and foreign addresses are IPv6 addresses
    #print("\nColumns", columns[0], columns[1], columns[2], columns[3],columns[4])
    
    #table = PrettyTable()
    #table.field_names = ["Source IP", "Source Port", "Destination IP", "Dest. Port", "Organization", "City", "Country"]
    
    if columns[0] == 'tcp6':

        #print('\n', columns[0])
        proto = "IPv6 TCP"

        # Find the index of the first period in the string
        period_index = columns[3].find('.')


        if period_index != -1:
            source_ipv6 = columns[3][:period_index]
            #print('source ipv6 address = ', source_ipv6)
        else:
            print("No period found in the string.")

        # Print the substring starting from the first period
        if period_index != -1:
            source_port = columns[3][period_index:][1:]
            #print ('source port = ', source_port)
        else:
            print("No period found in the string.")

        # Find the index of the first period in the string
        period_index = columns[4].find('.')

        if period_index != -1:
            destin_ipv6 = columns[4][:period_index]
            #print('destination ipv6 address = ', destin_ipv6)
        else:
            print("No period found in the string.")    


        # Print the substring starting from the first period
        if period_index != -1:
            destin_port = columns[4][period_index:][1:]
            #print ('destination port = ', destin_port)
        else:
            print("No period found in the string.")


        org, city, country, region = get_ip_geo(destin_ipv6)
        #print(f'Org {org}, City {city}, Country {country}, Region {region}')

        if ('*' in source_ipv6 or '*' in source_port or '*' in destin_port or '*' in destin_ipv6) or (destin_ipv6.startswith('fe80') == True):
        #if ('*' in source_ipv6 or '*' in source_port or '*' in destin_port or '*' in destin_ipv6):
            #print(destin_ipv6)
            continue
        elif location == 'y' and as_org == 'y':
            table.add_row(["", source_ipv6, source_port, destin_ipv6, destin_port, org if org else "", city if city else "", country if country else ""])
        elif as_org == 'y':
            table.add_row(["", source_ipv6, source_port, destin_ipv6, destin_port, org if org else ""])
        elif location == 'y':
            table.add_row(["", source_ipv6, source_port, destin_ipv6, destin_port, city if city else "", country if country else ""])
        else:    
            table.add_row(["", source_ipv6, source_port, destin_ipv6, destin_port])




#table.add_row(["IPv4 UDP", "", "", "", "", "", "", ""])
if location == 'y' and as_org == 'y': 
    table.add_row(["IPv6 UDP", "", "", "", "", "", "", ""])
elif as_org == 'y':
    table.add_row(["IPv6 UDP", "", "", "", "", ""])
elif location == 'y':
    table.add_row(["IPv6 UDP", "", "", "", "", "", ""])
else:
    table.add_row(["IPv6 UDP", "", "", "", ""])

# IPv6 UDP - Loop through each line of the output
for line in lines:
    # Skip the header row and any empty rows
    #print(line)
    if 'Proto' in line or not line:
        continue
    # Split the line into columns
    columns = re.split(r'\s+', line)
    
    if columns[0] == 'udp6':

        #print('\n', columns[0])
        proto = "IPv6 UDP"

        # Find the index of the first period in the string
        period_index = columns[3].find('.')


        if period_index != -1:
            source_ipv6 = columns[3][:period_index]
            #print('source ipv6 address = ', source_ipv6)
        else:
            print("No period found in the string.")

        # Print the substring starting from the first period
        if period_index != -1:
            source_port = columns[3][period_index:][1:]
            #print ('source port = ', source_port)
        else:
            print("No period found in the string.")

        # Find the index of the first period in the string
        period_index = columns[4].find('.')

        if period_index != -1:
            destin_ipv6 = columns[4][:period_index]
            #print('destination ipv6 address = ', destin_ipv6)
        else:
            print("No period found in the string.")    


        # Print the substring starting from the first period
        if period_index != -1:
            destin_port = columns[4][period_index:][1:]
            #print ('destination port = ', destin_port)
        else:
            print("No period found in the string.")


        org, city, country, region = get_ip_geo(destin_ipv6)
        #print(f'Org {org}, City {city}, Country {country}, Region {region}')

        if ('*' in source_ipv6 or '*' in source_port or '*' in destin_port or '*' in destin_ipv6) or (destin_ipv6.startswith('fe80:') == True):
        #if ('*' in source_ipv6 or '*' in source_port or '*' in destin_port or '*' in destin_ipv6):
            continue
        elif location == 'y' and as_org == 'y':
            table.add_row(["", source_ipv6, source_port, destin_ipv6, destin_port, org if org else "", city if city else "", country if country else ""])
        elif as_org == 'y':
            table.add_row(["", source_ipv6, source_port, destin_ipv6, destin_port, org if org else ""])
        elif location == 'y':
            table.add_row(["", source_ipv6, source_port, destin_ipv6, destin_port, city if city else "", country if country else ""])
        else:    
            table.add_row(["", source_ipv6, source_port, destin_ipv6, destin_port])




print(table)