#!/usr/bin/python
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
Disable Scapy Warnings at beginning of output
WARNING: No IPv4 address found on en5 !
WARNING: No IPv4 address found on ap1 !
WARNING: more No IPv4 address found on awdl0 !
'''
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import socket
from scapy.all import *

'''

'''



'''
Get free source port
'''
sock = socket.socket()
sock.bind(('', 0))
my_source_port = sock.getsockname()[1]
print(my_source_port)

'''
Create random TCP sequence number from 2^21 to 2^31
'''
my_seq_number = random.randrange(2097152,2147483648)

###############################################################################

print("\033c", end="")
print("Viewing the TCP 3-Way Handshake")
print("--------------------------------")
print("This program creates a connection using HTTP (port 80) only. HTTPS (port 443) coming.") 
#print("Would you like explanations of what you see? (y/n) - coming")
print("NOTE: After entering in the URL, you will have 30 seconds to complete 3-way handshake.")


# ip_selected = input("Which version of IP do you want? (4 or 6)? ")
# Make IPv4 default
ip_selected = "4"
if ip_selected != "6":
    ip_selected = "4"    

# Get Server IPv4 or IPv6 address from URL

while True:
    try:
        # url_Entered = 'info.cern.ch'
        url_Entered = input("\nEnter an HTTP URL (such as info.cern.ch) or q to quit: ")
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

###### -------------------------------------------------------------######

# Create a new IPv4 socket (s) using the given address family (AFNET = IPv4), 
# socket type (SOCK_STREAM = TCP) and protocol number. 
'''
if ip_selected == "4":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
else:
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
'''
 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   
s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])

###############################################################################
#
#     1. SYN
#
###############################################################################

seq = my_seq_number

# scapy 
ip=IP(src=s.getsockname()[0], dst=server_ip)
TCP_SYN=TCP(sport=my_source_port, dport=80, flags="S", seq=seq)

'''
print("\nSYN")
print("ip.show()")
ip.show()
print("TCP_SYN.show()")
TCP_SYN.show()
'''
print("\n1. SYN sent by the client")
print("-------------------------")
print("IP")
print(f"   Source IPv4 address: {ip.src}")
print(f"   Destination IPv4 address: {ip.dst}")
print("TCP")
print(f"   Source port: {TCP_SYN.sport}")
print(f"   Destination port {TCP_SYN.dport}")
print(f"   Flags: SYN")
print(f"   Sequence #: {TCP_SYN.seq}")
print(f"   Acknowledgement #: {TCP_SYN.ack}")
print(f"   Window size: {TCP_SYN.window}")

seq_end = str(TCP_SYN.seq)
seq_end = seq_end[-2::]

print(f"\nCLIENT --- [Flags: SYN] Relative Seq = 0 [{seq_end}] ------->>>>> ")

###############################################################################
#
#     2. SYN ACK
#
###############################################################################

# scapy
TCP_SYNACK=sr1(ip/TCP_SYN, verbose = 0)

any_key = input("\nPress return to see part 2 of 3....")

'''
print("\nSYN ACK")
print("ip.show()")
ip.show()
print("TCP_SYNACK.show()")
TCP_SYNACK.show()
'''

if TCP_SYNACK[TCP].flags.S:
    synack_syn_flag = True
    prn_flag = "SYN"
else:
    synack_syn_flag = False

if TCP_SYNACK[TCP].flags.A:
    synack_ack_flag = True
    prn_flag = "SYN ACK"
else:
    synack_ack_flag = False

    
print("\n2. SYN-ACK sent by the server")
print("---------------------------")
print("IP")
print(f"   Source IPv4 address: {TCP_SYNACK.src}")
print(f"   Destination IPv4 address: {TCP_SYNACK.dst}")
print("TCP")
print(f"   Source port: {TCP_SYNACK.sport}")
print(f"   Destination port {TCP_SYNACK.dport}")
#print(f"Flags: {TCP_SYNACK.flags}")
if synack_syn_flag == True and synack_ack_flag == True:
    print(f"   Flags: SYN ACK")
elif synack_syn_flag == True and synack_ack_flag == False: 
    print(f"   Flags: SYN")
elif synack_syn_flag == False and synack_ack_flag == True: 
    print(f"   Flags: ACK")
print(f"   Sequence #: {TCP_SYNACK.seq}")
print(f"   Acknowledgement #: {TCP_SYNACK.ack}")
print(f"   Window size: {TCP_SYNACK.window}")

seq_end = str(TCP_SYNACK.seq)
seq_end = seq_end[-2::]

ack_end = str(TCP_SYNACK.ack)
ack_end = ack_end[-2::]

print(f"\n<<<<<--- [Flags: {prn_flag}] Relative Seq = 0 [{seq_end}], Relative Ack = 1 [{ack_end}]----  SERVER ")

any_key = input("\nPress return to see part 3 of 3....")

###############################################################################
#
#     3. ACK
#
###############################################################################


seq = seq + 1

my_ack = TCP_SYNACK.seq + 1

# scapy
TCP_ACK=TCP(sport=my_source_port, dport=80, flags="A", seq=seq, ack=my_ack)
send((ip/TCP_ACK), verbose = False)

'''
print("\nACK")
print("ip.show()")
ip.show()
print("TCP_ACK.show()")
TCP_ACK.show()
'''

if TCP_ACK[TCP].flags.S:
    ack_syn_flag = True
else:
    ack_syn_flag = False
 
if TCP_ACK[TCP].flags.A:
    ack_ack_flag = True
else:
    ack_ack_flag = False

    
print("\n3. ACK sent by the client")
print("-------------------------")
print("IP")
print(f"   Source IPv4 address: {ip.src}")
print(f"   Destination IPv4 address: {ip.dst}")
print("TCP")
print(f"   Source port: {TCP_ACK.sport}")
print(f"   Destination port {TCP_ACK.dport}")
#print(f"Flags: {TCP_ACK.flags}")
if ack_syn_flag == True and ack_ack_flag == True:
    print(f"   Flags: SYN ACK")
elif ack_syn_flag == True and ack_ack_flag == False: 
    print(f"   Flags: SYN")
elif ack_syn_flag == False and ack_ack_flag == True: 
    print(f"   Flags: ACK")
print(f"   Sequence #: {TCP_ACK.seq}")
print(f"   Acknowledgement #: {TCP_ACK.ack}")
print(f"   Window size: {TCP_ACK.window}")

seq_end = str(TCP_ACK.seq)
seq_end = seq_end[-2::]

ack_end = str(TCP_ACK.ack)
ack_end = ack_end[-2::]

print(f"\nCLIENT --- [Flags: ACK] Relative ACK = 1 [{ack_end}], Relative Seq = 1 [{seq_end}] ------->>>>> ")

print("\n<<< End of TCP 3-Way Handshake >>>")
any_key = input("\nPress return to see HTTP GET Request sent by Client....")

###############################################################################
#
#     HTTP GET
#
###############################################################################


seq = seq + 1

my_payload="GET / HTTP/1.1\r\nHost: "+url_Entered+"\r\n\r\n"
TCP_PUSH=TCP(sport=my_source_port, dport=80, flags="PA", seq=seq, ack=my_ack)

send(ip/TCP_PUSH/my_payload, verbose = 0)

'''
print("Data")
print("ip.show()")
ip.show()
print("TCP_PUSH.show()")
TCP_PUSH.show()
'''

print("\nHTTP GET Request sent by the client")
print("-----------------------------------")
print("IP")
print(f"   Source IPv4 address: {ip.src}")
print(f"   Destination IPv4 address: {ip.dst}")
print("TCP")
print(f"   Source port: {TCP_PUSH.sport}")
print(f"   Destination port {TCP_PUSH.dport}")
#print(f"Flags: {TCP_PUSH.flags}")
print(f"   Flags:", end ="")
if TCP_PUSH[TCP].flags.F:
    print(" FIN ", end ="")
if TCP_PUSH[TCP].flags.S:
    print(" SYN ", end ="")
if TCP_PUSH[TCP].flags.A:
    print(" ACK ", end ="")
if TCP_PUSH[TCP].flags.R:
    print(" RST ", end ="")
if TCP_PUSH[TCP].flags.P:
    print(" PSH ", end ="")
if TCP_PUSH[TCP].flags.U:
    print(" URG ", end ="")
if TCP_PUSH[TCP].flags.E:
    print(" ECE ", end ="")
if TCP_PUSH[TCP].flags.C:
    print(" CWR ", end ="")


print(f"\n   Sequence #: {TCP_PUSH.seq}")
print(f"   Acknowledgement #: {TCP_PUSH.ack}")
print(f"   Window size: {TCP_PUSH.window}")

my_payload_indented="   GET / HTTP/1.1\r\n   Host: "+url_Entered+""

print(f"\nData: \n{my_payload_indented}")
print("\n")

seq_end = str(TCP_PUSH.seq)
seq_end = seq_end[-2::]

ack_end = str(TCP_PUSH.ack)
ack_end = ack_end[-2::]

print(f"\nCLIENT --- [Flags: ACK PSH] Relative ACK = 1 [{ack_end}], Relative Seq = 2 [{seq_end}] ------->>>>> ")
print("\n")


