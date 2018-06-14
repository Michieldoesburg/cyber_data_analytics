import csv
from assignment3.utils import *
from assignment3.packet import *

file = "data\CTU13-scenario10.pcap.netflow.labeled"

filtered_packets = []
count_skipped = 0
attribute_mapping = dict()

# Implement attribute mapping M_i, i = 0...k as explained in section IV of the paper.
def add_to_attribute_map(x, feature):
    # Check if feature in attribute_mapping
    if feature in attribute_mapping:
        mapping = attribute_mapping[feature]
        if not x in mapping:
            # If the value is not yet registered, encode it.
            encoded_value = len(list(mapping.keys()))
            mapping[x] = encoded_value
    else:
        new_dict = dict()
        new_dict[x] = 0
        attribute_mapping[feature] = new_dict

# Encoding of the netflow using the generated attribute mapping.
def encode_netflow(p, features):
    # define spaceSize
    spaceSize = 1
    for f in features:
        spaceSize = spaceSize*len(list(attribute_mapping[f]))
    code = 0
    for f in features:
        mapping = attribute_mapping[f]
        code += (mapping[p[f]]*int(float(spaceSize)/float(len(mapping.keys()))))
        spaceSize = int(float(spaceSize)/float(len(mapping.keys())))
    return code



# Treat data as a stream.
with open(file, "r") as f:
    reader = csv.reader(f, delimiter=" ")
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
        p = packet(date, new_args[1], new_args[2], new_args[3], new_args[5], new_args[6], new_args[7], new_args[8], new_args[9], new_args[10], new_args[11])

        ip = p.dst.split(":")[0]
        label = p.label

        # Filter the broadcasts and non-ip adresses. Also filter background packets.
        if (ip != "Broadcast") and (ip != "ff02") and (label != 'Background'):
            filtered_packets.append(p)

print('Amount of packets skipped due to reading errors: %i' % count_skipped)

### This is room left for the discretization. ###


print(str.split('abcdefg'))
