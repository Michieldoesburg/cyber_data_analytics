import csv
import sympy
import random
from Hashfunction import Hashfunction

addresses = []
id_to_ip_map = dict()

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
                    addresses.append(ip)

                print(ip)

max_id = 0

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
