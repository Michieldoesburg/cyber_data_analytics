import csv
import sympy
import random
from assignment3.Hashfunction import Hashfunction
from assignment3.min_wise_sample import MinWiseSample
import queue as q

addresses = []
id_to_ip_map = dict()
ip_freq = dict()
ip_amt = 0
reservoir_size = 10000
k = 10
sample = MinWiseSample(reservoir_size)

def sort_dict_by_value(freq, max_val):
    pq = q.PriorityQueue()
    for ip in freq:
        # This is a trick to store frequencies in descending order:
        # subtract the actual frequency of the maximum size of the sample.
        pq.put((max_val - freq[ip], ip))
    res = dict()
    while not pq.empty():
        x = pq.get()
        # Apply correction to get the actual frequencies back.
        res[x[1]] = max_val - x[0]
    return res

def select_first_k(dictionary, k):
    keyset = list(dictionary.keys())
    res = dict()
    for i in range(k):
        key = keyset[i]
        res[key] = dictionary[key]
    return res

def keys_in_common(dict1, dict2):
    count = 0
    for k in dict1:
        if k in dict2:
            count += 1
    return count

def keys_in_same_position(dict1, dict2):
    count = 0
    keys1, keys2 = list(dict1.keys()), list(dict2.keys())
    for i in range(len(keys1)):
        if keys1[i] == keys2[i]:
            count += 1
    return count


# Treat data as a stream.
with open("data\capture20110816-2.pcap.netflow.labeled", "r") as f:
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

                print(ip)


total_freq_sorted = sort_dict_by_value(ip_freq, ip_amt)
sampled_freq_sorted = sample.count_and_sort()

print('Stream reading done.')
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


max_id = 0

### OLD CODE ###

# Create id -> ip map and find max identifier
for ip in addresses:
    nums = ip.split(".")
    identifier = ""
    for arg in nums:
        identifier += str(arg)

    try:
        identifier = int(identifier)

        if identifier > max_id:
            max_id = identifier

        id_to_ip_map[identifier] = ip

    except ValueError as e:
        print(identifier)


hashfunctions = []

# Find a prime modulus for the hash functions bigger than the maximum identifier
modulus = sympy.nextprime(max_id)

# Generate the random hash functions
for x in range(10):
    a = random.randint(0, max_id-1)
    b = random.randint(0, max_id-1)
    hashfunctions.append(Hashfunction(a, b, modulus))


# Compute the min hash for every identifier
for id in id_to_ip_map.keys():
    hashes = []

    for hash_func in hashfunctions:
        hashes.append(hash_func.compute(id))

    min_hash = min(hashes)
