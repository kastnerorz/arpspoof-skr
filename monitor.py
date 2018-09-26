from scapy.all import *
from optparse import OptionParser
import os
import signal
import sys
import threading
import time

# Given an IP, get the MAC. Broadcast ARP Request for a IP Address. Should recieve
# an ARP reply with MAC Address
def get_mac(ip_address):
    # ARP request is constructed. sr function is used to send/ receive a layer 3 packet
    # Alternative Method using Layer 2: resp, unans =  srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1, pdst=ip_address))
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s, r in resp:
        return r[ARP].hwsrc
    return None

if __name__ == '__main__':
    
    print('[*] Enable ARP Spoof Monitor')
    while True:
        try:
            packets = sniff(filter="arp" iface=conf.iface, count=3)
            for packet in packets:
                if packet.type is '0x806':
                    print(packet.summary())
        except KeyboardInterrupt:
            print(f"[*] Stopping Network Monitor")
            sys.exit(0)