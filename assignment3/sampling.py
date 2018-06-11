import csv
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

                # Filter the broadcasts
                if (ip != "Broadcast") and (ip != "ff02"):
                    addresses.append(ip)

                print(ip)

max_id = 0

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

print(max_id)

#for x in range(10):
    #hashfunctions.append(Hashfunction())