import csv
from assignment3.utils import *
from assignment3.packet import *
from assignment3.attribute_mapping import *
from assignment3.SAX_adapted import *
from ngram import NGram
from random import sample

# Note: you will have to download the dataset from the CTU13 website. It could not be put on the Github repo. Sorry.
file = "data\capture20110818.pcap.netflow.labeled"

filtered_packets = []
count_skipped = 0
attribute_mapping = AttMap()
values_per_letter = 1.0
label_actual = []
letters_per_host = dict()
infected_hosts = set()
hosts = []
hosts_all = set()
non_infected_hosts = set()

# This is a custom transformation method to keep only certain elements of the packet.
def transform_packet(p):
    protocol = p.protocol
    flags = p.flags
    result = dict()
    result['Protocol'] = protocol
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
        host = p.src
        ip = p.dst
        label = p.label

        # Filter the broadcasts and non-ip adresses. Also filter background packets.
        if (ip != "Broadcast") and (ip != "ff02") and (label != 'Background'):
            if label == 'LEGITIMATE':
                label_actual.append(0)
            if label == 'Botnet':
                label_actual.append(1)
                infected_hosts.add(host)
            p = transform_packet(p)
            attribute_mapping.add_packet(p)
            filtered_packets.append(p)
            letters_per_host[host] = ''
            hosts.append(host)
            hosts_all.add(host)


print('Amount of packets skipped due to reading errors: %i' % count_skipped)

non_infected_hosts = hosts_all.difference(infected_hosts)

# Create letter list of packets.
signal = attribute_mapping.encode_full_netflow(filtered_packets, filtered_packets[0].keys())
sax = SAX(wordSize=int(float(len(signal)/values_per_letter)), alphabetSize=10)
signal_discretized = ' '.join(sax.to_letter_rep(signal)[0]).split()

# Save discretized netflow per host.
i = 0
for letter in signal_discretized:
    host = hosts[i]
    string = letters_per_host[host]
    new_string = string + letter
    letters_per_host[host] = new_string
    i += 1

# Determine which host is infected and which is not. A host is infected if at least one netflow originating from it is a botnet netflow.
host_infection = dict()
for h in infected_hosts:
    # Host is infected.
    host_infection[h] = 1

for k in letters_per_host.keys():
    if not k in host_infection:
        # Host is not infected.
        host_infection[k] = 0

# Determine one infected host and one non-infected host to use as example.
# The example will be the string that is the longest.
infected_host_profile = ''
non_infected_host_profile = ''

for host in letters_per_host:
    string = letters_per_host[host]
    if host in infected_hosts and len(string) > len(infected_host_profile):
        infected_host_profile = string
    if host in non_infected_hosts and len(string) > len(non_infected_host_profile):
        non_infected_host_profile = string

# Determine TN, FP, FN, TP
tn, fp, fn, tp = 0, 0, 0, 0
ng = NGram([infected_host_profile, non_infected_host_profile])
for k in letters_per_host:
    string = letters_per_host[k]
    label_actual = host_infection[k]
    profile = ng.find(string)
    if profile == infected_host_profile:
        label_predicted = 1
    else:
        label_predicted = 0

    if label_actual == label_predicted and label_actual == 0:
        tn += 1
    if label_actual == label_predicted and label_actual == 1:
        tp += 1
    if label_actual == 1 and label_predicted == 0:
        fn += 1
    if label_actual == 0 and label_predicted == 1:
        fp += 1


print('TP: ' + str(tp))
print('FP: ' + str(fp))
print('TN: ' + str(tn))
print('FN: ' + str(fn))