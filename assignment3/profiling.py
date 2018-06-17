import csv
from assignment3.utils import *
from assignment3.packet import *
from assignment3.attribute_mapping import *
from nltk.probability import *

file = "data\CTU13-scenario10.pcap.netflow.labeled"

filtered_packets = []
count_skipped = 0
label_actual = []

# This is a custom transformation method to keep only certain elements of the packet.
def transform_packet(p):
    bytes_per_packet = int(float(p.bytes)/float(p.packets))
    flags = p.flags
    result = dict()
    result['Bytes per packet'] = bytes_per_packet
    result['Flags'] = flags
    return result

# Treat data as a stream.
with open(file, "r") as f:
    reader = csv.reader(f, delimiter=" ")
    print('Started reading...')
    for z, line in enumerate(reader):
        if z < 1:
            continue

        # Split the arguments in the line
        args = line[1].split("\t")
        new_args = remove_empty_strings(args)
        if len(new_args) < 12:
            count_skipped += 1
            continue
        # print(new_args)
        date = line[0] + ' ' + new_args[0]
        p = packet(date, new_args[1], new_args[2], new_args[3].split(':')[0], new_args[5].split(':')[0], new_args[6], new_args[7], new_args[8], new_args[9], new_args[10], new_args[11])

        ip = p.dst
        label = p.label

        # Filter the broadcasts and non-ip adresses. Also filter background packets.
        if (ip != "Broadcast") and (ip != "ff02") and (label != 'Background'):
            if label == 'LEGITIMATE':
                label_actual.append(0)
            if label == 'Botnet':
                label_actual.append(1)
            p = transform_packet(p)
            filtered_packets.append(p)

print('Amount of packets skipped due to reading errors: %i' % count_skipped)