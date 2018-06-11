import csv
import assignment3.countminsketch as cms
from assignment3.utils import *

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

        for i, x in enumerate(args):
            # We are interested in the ip address after the -> arrow.
            if x == "->":
                # Split the IP address from the port number
                ip = args[i+1].split(":")[0]

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