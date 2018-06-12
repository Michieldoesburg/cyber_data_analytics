import csv
from assignment3.min_wise_sample import MinWiseSample
from assignment3.utils import *
from assignment3.packet import *

addresses = []
ip_freq = dict()
ip_amt = 0
reservoir_size = 10000
k = 10
sample = MinWiseSample(reservoir_size)
file = "data\capture20110816-2.pcap.netflow.labeled"

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
        p = packet(date, new_args[1], new_args[2], new_args[3], new_args[5], new_args[6], new_args[7], new_args[8], new_args[9], new_args[10], new_args[11])

        ip = p.dst.split(":")[0]

        # Filter the broadcasts and non-ip adresses
        if (ip != "Broadcast") and (ip != "ff02"):
            # Add to the min-wise sampling pool.
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
sampled_freq_sorted = sample.count_and_sort()

print('Stream reading done.')
print('The file that was read can be found in %s' % file)
print('There are %i destination IP addresses' % ip_amt)

print('Printing all frequencies:')
print('Total frequencies, sorted by value in descending order:')
print(total_freq_sorted)
print('Frequencies of samples sampled by using min-wise sampling with a reservoir size of %i, sorted by value in descending order:' % reservoir_size)
print(sampled_freq_sorted)
print('')
first_k_all = select_first_k(total_freq_sorted, k)
first_k_sampled = select_first_k(sampled_freq_sorted, k)
print('Printing only the top %i frequencies' % k)
print('Top %i highest frequencies of the total frequencies:' % k)
print(first_k_all)
print('Top %i highest frequencies of the sampled frequencies:' % k)
print(first_k_sampled)
print('These last two sets have %i IP addresses in common, %i of which are in the same position' % (keys_in_common(first_k_all, first_k_sampled), keys_in_same_position(first_k_all, first_k_sampled)))