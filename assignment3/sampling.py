import csv
from assignment3.min_wise_sample import MinWiseSample
from assignment3.utils import *
from assignment3.packet import *

reservoir_size_range = [100, 1000, 10000, 100000]

samples = []
addresses = []
ip_freq = dict()
ip_amt = 0
k = 10
# Define the host IPs you are interested in.
infected_host_ips = ['147.32.84.165']
# Set to true if you want to bypass the host IP check.
scan_all = False


for x in reservoir_size_range:
    samples.append(MinWiseSample(x))

file = "data\capture20110818-2.pcap.netflow.labeled"

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
        p = packet(date, new_args[1], new_args[2], new_args[3].split(':')[0], new_args[5].split(':')[0], new_args[6], new_args[7], new_args[8], new_args[9], new_args[10], new_args[11])

        src = p.src
        ip = p.dst

        # Filter the broadcasts and non-ip adresses
        if (ip != "Broadcast") and (ip != "ff02") and (scan_all or src in infected_host_ips):
            # Add to the min-wise sampling pool.
            for sample in samples:
                sample.add(ip)
            # Add to the frequency counter.
            if ip in ip_freq:
                ip_freq[ip] += 1
            else:
                ip_freq[ip] = 1
            # Increment the amount of IP's gathered. This is useful in the future.
            ip_amt += 1
            addresses.append(ip)


total_freq_sorted = sort_dict_by_value(ip_freq, ip_amt)
for i, sample in enumerate(samples):
    samples[i] = sample.count_and_sort()

print('Stream reading done.')
print('The file that was read can be found in %s' % file)
print('There are %i destination IP addresses' % ip_amt)

# print('Printing all frequencies:')
# print('Total frequencies, sorted by value in descending order:')
# print(total_freq_sorted)
#
# for i, sample in enumerate(samples):
#     print('Frequencies of samples sampled by using min-wise sampling with a reservoir size of %i, sorted by value in descending order:' % 10**(i+2))
#     print(sample)

print('')
first_k_all = select_first_k(total_freq_sorted, k)
print('Printing only the top %i frequencies' % k)
print('Top %i highest frequencies of the total frequencies:' % k)
print(first_k_all)

for i, sample in enumerate(samples):
    first_k_sampled = select_first_k(sample, k)
    print('Top {} highest frequencies of the sampled frequencies with reservoir size {}:'.format(k,  10**(i+2)))
    print(first_k_sampled)
    print('This set has %i IP addresses in common with the normal sample, %i of which are in the same position' % (keys_in_common(first_k_all, first_k_sampled), keys_in_same_position(first_k_all, first_k_sampled)))
    print()