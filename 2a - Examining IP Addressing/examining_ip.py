# examining_IP.py
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


'''
Here is an example of a Python program that uses the socket module and implements HTTPS with TLS:
This program uses the socket module to create a TCP socket and the ssl module to wrap the socket 
in an SSL/TLS context. The connect() method is used to connect to the server, and the 
sendall() and recv() methods are used to send a request and receive a response, respectively. 
Finally, the close() method is used to close the connection.
'''


import socket
import ssl
import sys
import ipaddress
import warnings
import requests
from requests import get
#import dnspython as dns
import dns.resolver


###############################################################################################

warnings.filterwarnings("ignore", category=DeprecationWarning) 

print("\033c", end="")
print("Viewing the IP addresses")
print("----------------------------------------------------")
#print("For simplicity, this program creates a connection using HTTP (port 80) only.") 
# print("An HTTPS version is under construction.")
#print("\nWould you like explanations of what you see? (y/n) - coming")


ip_selected = input("Which version of IP do you want? (4 or 6)? ")
# Make IPv4 default
if ip_selected != "6":
    ip_selected = "4"    

'''
port_selected = input("Are you using HTTP port 80 or HTTPS port 443 (80 or 443)? ")
# Make IPv4 default
if port_selected == "80":
    port = 80
else:
    port = 443 
'''

port = 443

# Get Server IPv4 or IPv6 address from URL

while True:
    try:
        # url_Entered = 'info.cern.ch'
        url_Entered = input("\nEnter an HTTPS URL (such as www.cisco.com) or q to quit: ")
        if url_Entered == 'q' or url_Entered == 'Q':
            break
        # socket.gethostbyname(url_Entered) Translate a host name to IPv4 address format. 
        # The IPv4 address is returned as a string, such as '100.50.200.5'.
        # ? should use getaddrinfo() for dual stack support ?
        if ip_selected == "4":
            server_ip = socket.getaddrinfo(url_Entered, None, socket.AF_INET)[0][4][0]
        else:
            server_ip = socket.getaddrinfo(url_Entered, None, socket.AF_INET6)[0][4][0] 
            #Verify if GUA
            # if ipaddress.ip_address(server_ip).is_global  == True:
            if server_ip.startswith("2") or server_ip.startswith("3"):
                # IPv6 GUA verified
                pass
            else:
                # Force IPv4
                print("No IPv6 global unicast address... changing to IPv4...")
                server_ip = socket.getaddrinfo(url_Entered, None, socket.AF_INET)[0][4][0]
                ip_selected == "4"                 
    except:
        print(f"Invalid input {url_Entered}, try again...")
    else:
        break

if url_Entered == 'q' or url_Entered == 'Q':
    sys.exit()  

request = "GET / HTTP/1.1\r\nHost: "+url_Entered+"\r\n\r\n"

request = request.encode()

###############################





###############################################################################################


# Connect to the example.com server over HTTPS with TLS
#response = connect_via_https_tls("www.cisco.com", 443)
#host = "www.cisco.com"
#port = 443

# Create a TCP socket
if ip_selected == "4":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
else:
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)




# Wrap the socket in an SSL/TLS context
tls_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)

# Connect to the server
tls_sock.connect((url_Entered, port))


####### 

if ip_selected == "4":
    if ipaddress.ip_address(tls_sock.getsockname()[0]).is_private  == True:
        print(f'\nYour private IPv4 address is {tls_sock.getsockname()[0]}')
    else:
        print(f'\nYour IPv4 address is {tls_sock.getsockname()[0]}')
    f = requests.request('GET', 'http://myip.dnsomatic.com')
    ipv4_public = f.text

    if '<html>' in ipv4_public or 'Too Many Requests' in ipv4_public:
        ipv4_public = get('https://api.ipify.org').text
        if '<html>' in ipv4_public or 'Too Many Requests' in ipv4_public:
            print("No public IPv4 address available. Please try again later.")
            ipv4_public = "Unavailable"
    else: 
        if ipaddress.ip_address(tls_sock.getsockname()[0]).is_private  == True:
            print('Translated to the public IPv4 Address is: {}'.format(ipv4_public))  
        else:
            print('Note: Your device is using a public IPv4 address.')  
else:
    print(f'\nYour IPv6 address is {tls_sock.getsockname()[0]}')

########

dns_resolver = dns.resolver.Resolver()
print(f'\nDNS server {dns_resolver.nameservers[0]} resolved {url_Entered} to {server_ip}')

#######


# Send a request to the server
#tls_sock.sendall(b"GET / HTTP/1.1\r\nHost: "+url_Entered+"\r\n\r\n")
tls_sock.sendall(request)

# Receive the response
response = tls_sock.recv(2048)

#print(response.decode())


######## ---  ########

print("\n- - - - - - -  CLIENT - [ After TCP 3-Way Handshake ] - - - - - - -")

# print('\nFrom Client:')
# print('------------')
print(f'\nHTTP GET Request: GET / HTTP/1.1\ Host: {url_Entered}')

if ipaddress.ip_address(tls_sock.getsockname()[0]).is_private  == True:
    client_ip = "Private"
else:
    client_ip = "Public "


if ip_selected == "4":
    print("\nCLIENT ------->>>>>  SERVER")
    print(f"|----------------------------------  IPv4 Header  ---------------------------------------|")
    print(f"|    Source IPv4 Address                    |    Destination IPv4 Address                |")
    print(f"|  {tls_sock.getsockname()[0]:<15} (Client's {client_ip} IPv4)  |        {server_ip:<15}                     |")
    if ipaddress.ip_address(tls_sock.getsockname()[0]).is_private  == True:
        print(f"|  {ipv4_public:<15} (Client's Public IPv4)   |                                            |")
    print(f"|----------------------------------------------------------------------------------------|")


    if ipaddress.ip_address(tls_sock.getsockname()[0]).is_private  == True:
        print(f'\nPrivate source address {tls_sock.getsockname()[0]} translated by NAT to public address {ipv4_public}')

if ip_selected == "6":
    print("\nCLIENT ------->>>>>  SERVER")
    print(f"|----------------------------------  IPv6 Header  ---------------------------------------|")
    print(f"|    Source IPv6 Address                    |    Destination IPv6 Address                |")
    print(f"|  {tls_sock.getsockname()[0]:<39}  | {server_ip:<39}    |")
    print(f"|----------------------------------------------------------------------------------------|")


    print("\nNo NAT needed with IPv6!")



#any_key = input('\nPress enter key to see packet/segment reply from the SERVER...')


print("\n- - - - - - -  SERVER - - - - - - - - - - - - - - - - - - - - -")

print("\nCLIENT   <<<<<------- SERVER")

if ip_selected == "4":
    print(f"|----------------------------------  IPv4 Header  ---------------------------------------|")
    print(f"|    Source IPv4 Address                    |    Destination IPv4 Address                |")
    print(f"|      {server_ip:<15}                      |  {ipv4_public:<15} (Client's Public IPv4)    |")
    if ipaddress.ip_address(tls_sock.getsockname()[0]).is_private  == True:
        print(f"|                                           |  {tls_sock.getsockname()[0]:<15} (Client's Private IPv4)   |")
    print(f"|----------------------------------------------------------------------------------------|")

    if ipaddress.ip_address(tls_sock.getsockname()[0]).is_private  == True:
        print(f'\nPublic destination IPv4 address {ipv4_public} translated by NAT to private address {tls_sock.getsockname()[0]}')


if ip_selected == "6":
    print(f"|----------------------------------  IPv6 Header  ---------------------------------------|")
    print(f"|    Source IPv6 Address                    |    Destination IPv6 Address                |")
    print(f"|  {server_ip:<39}  | {tls_sock.getsockname()[0]:<39}    |")
    print(f"|----------------------------------------------------------------------------------------|")

    print("\nNo NAT needed with IPv6!")
    
######## ---  ########

print("\n")

# Close the connection

tls_sock.close()