#!/usr/bin/python3
import fcntl
import struct
import os
import time
from scapy.all import *

TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

# Create the tun interface
tun = os.open("/dev/net/tun", os.O_RDWR)
ifr = struct.pack('16sH', b'SecureVPN%d', IFF_TUN | IFF_NO_PI)
ifname_bytes = fcntl.ioctl(tun, TUNSETIFF, ifr)

# Get the interface name
ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")
print("Interface Name: {}".format(ifname))

os.system("ip addr add 192.168.87.180/24 dev {}".format(ifname))
os.system("ip link set dev {} up".format(ifname))

message = "helloWord"
while True:
    # Get a packet from the tun interface
    packet = os.read(tun, 2048)
    ip = IP(packet)
    rawbytes = ip.payload
    obtained_message = rawbytes.decode('utf-8')
    print(obtained_message)
    newip = IP(src='1.2.3.4', dst=ip.src)
    newip.payload =  str.encode(message)

    os.write(tun, bytes(newip))
