from scapy.all import *

packets = rdpcap('data/capture20110816-2.pcap')

print(packets)