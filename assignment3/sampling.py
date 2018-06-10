from scapy.all import *

packets = rdpcap('data/capture20110818-2.pcap.netflow.labeled')

print(packets)