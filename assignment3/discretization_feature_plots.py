file = "data\capture20110818-2.pcap.netflow.labeled"
from assignment3.utils import *
from assignment3.packet import *
import matplotlib.pyplot as plt
import numpy as np
import csv

filtered_packets = []
count_skipped = 0
values_per_letter = 1.0
label_actual = []

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
            filtered_packets.append(p)

        print(z)

good_indeces = []
good_values = []
bad_indeces = []
bad_values = []

for i, p in enumerate(filtered_packets):
    if p.label == "Botnet":
        bad_values.append(int(float(p.bytes) / float(p.packets)))
        bad_indeces.append(i)
    else:
        good_values.append(int(float(p.bytes) / float(p.packets)))
        good_indeces.append(i)

plt.scatter(good_indeces, good_values, c="blue")
plt.scatter(bad_indeces, bad_values, c="red")

plt.show()