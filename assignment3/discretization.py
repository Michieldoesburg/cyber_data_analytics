import csv
from assignment3.utils import *
from assignment3.packet import *
from assignment3.attribute_mapping import *
from assignment3.SAX_adapted import *
from nltk import ngrams
from nltk.probability import *
import numpy as np
from sklearn.metrics import confusion_matrix

file = "data\CTU13-scenario10.pcap.netflow.labeled"

filtered_packets = []
count_skipped = 0
attribute_mapping = AttMap()
values_per_letter = 1.0
label_actual = []

# This is a custom transformation method to keep only certain elements of the packet.
def transform_packet(p):
    bytes_per_packet = int(float(p.bytes)/float(p.packets))
    flags = p.flags
    result = dict()
    result['Bytes per packet'] = bytes_per_packet
    result['Flags'] = flags
    return result

def build_conditional_freq_model(ngram):
    cfd = ConditionalFreqDist()
    for g in ngram:
        key = ''
        for i in range(n - 1):
            key += g[i]
        value = g[n - 1]
        cfd[key][value] += 1
    return cfd

def get_conditional_probabilities(ngram, cfd):
    freq = []
    for g in ngram:
        key = ''
        for i in range(n - 1):
            key += g[i]
        value = g[n - 1]
        total_for_key = 0.0
        for k in cfd[key].keys():
            total_for_key += float(cfd[key][k])
        amt = float(cfd[key][value])
        f = amt / total_for_key
        freq.append(f)
    return freq

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
        p = packet(date, new_args[1], new_args[2], new_args[3], new_args[5], new_args[6], new_args[7], new_args[8], new_args[9], new_args[10], new_args[11])

        ip = p.dst.split(":")[0]
        label = p.label

        # Filter the broadcasts and non-ip adresses. Also filter background packets.
        if (ip != "Broadcast") and (ip != "ff02") and (label != 'Background'):
            if label == 'LEGITIMATE':
                label_actual.append(0)
            if label == 'Botnet':
                label_actual.append(1)
            p = transform_packet(p)
            attribute_mapping.add_packet(p)
            filtered_packets.append(p)

print('Amount of packets skipped due to reading errors: %i' % count_skipped)

# Create letter list of packets.
signal = attribute_mapping.encode_full_netflow(filtered_packets, filtered_packets[0].keys())
sax = SAX(wordSize=int(float(len(signal)/values_per_letter)), alphabetSize=10)
signal_discretized = sax.to_letter_rep(signal)
signal_preprocessed = ' '.join(list(signal_discretized[0]))

label_classified = [0, 0]

# Use NLTK's implementation of N-grams to detect anomalies.
n = 3
ngram = ngrams(signal_preprocessed.split(), n)
# First, build the model.
cfd = build_conditional_freq_model(ngram)

# Need to re-initiate the ngram.
ngram = ngrams(signal_preprocessed.split(), n)
# Second, check probabilities of all combinations.
freq = get_conditional_probabilities(ngram, cfd)

labels_predicted = [1 if x < 0.005 else 0 for x in freq]
for x in labels_predicted:
    label_classified.append(x)

cm = confusion_matrix(label_actual, label_classified)
print(cm)

tn, fp, fn, tp = cm.ravel()
print('TP: ' + str(tp))
print('FP: ' + str(fp))
print('TN: ' + str(tn))
print('FN: ' + str(fn))