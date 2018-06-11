import csv

with open("data\capture20110816-2.pcap.netflow.labeled", "r") as f:
    reader = csv.reader(f, delimiter=" ")
    for i, line in enumerate(reader):
        strings = line[1].split(" ")
        strings = strings[0].split("\t")
        print('line[{}] = {}'.format(i, strings[0]))
