import csv
import assignment3.countminsketch as cms
from assignment3.utils import *
from assignment3.packet import *

file = "data\capture20110816-2.pcap.netflow.labeled"
table_size = 50
hash_functions = 10
ip_set = set()
ip_amt = 0
k = 10

sketch = cms.CountMinSketch(table_size, hash_functions)

# Treat data as a stream.
with open(file, "r") as f:
    reader = csv.reader(f, delimiter=" ")
    for z, line in enumerate(reader):
        if z < 1:
            continue

        # Split the arguments in the line
        args = line[1].split("\t")
        new_args = remove_empty_strings(args)
        date = line[0] + ' ' + new_args[0]
        p = packet(date, new_args[1], new_args[2], new_args[3], new_args[5], new_args[6], new_args[7], new_args[8],
                    new_args[9], new_args[10], new_args[11])

        ip = p.dst.split(":")[0]

        # Filter the broadcasts and non-ip adresses
        if (ip != "Broadcast") and (ip != "ff02"):
            sketch.add(ip)
            ip_set.add(ip)
            ip_amt += 1

print('Stream reading done.')
print('The file that was read can be found in %s' % file)
print('There are %i destination IP addresses' % ip_amt)

ip_dict = dict()
for ip in ip_set:
    ip_dict[ip] = sketch[ip]

ip_dict = sort_dict_by_value(ip_dict, ip_amt)
print('Total sketched frequencies, generated with table_size=%i and hash_functions=%i, sorted by value in descending order:' % (table_size, hash_functions))
print(ip_dict)
top_k = select_first_k(ip_dict, k)
print('Top %i highest sketched frequencies:' % k)
print(top_k)