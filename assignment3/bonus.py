import csv
from assignment3.utils import *
from assignment3.packet import *
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix

# Note: you will have to download the dataset from the CTU13 website. It could not be put on the Github repo. Sorry.
file = "data\capture20110818.pcap.netflow.labeled"

filtered_packets = []
filtered_packets_host = []
count_skipped = 0
label_actual = []

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

        ip = p.dst
        label = p.label

        # Filter the broadcasts and non-ip adresses. Also filter background packets.
        if (ip != "Broadcast") and (ip != "ff02") and (label != 'Background'):
            if label == 'LEGITIMATE':
                label_actual.append(0)
            if label == 'Botnet':
                label_actual.append(1)
            filtered_packets_host.append(p)
            p = transform_packet(p)
            filtered_packets.append(p)


print('Amount of packets skipped due to reading errors: %i' % count_skipped)

# Parameters for label encoding.
cat_feat = [0, 1]
le = LabelEncoder()

arr = pd.DataFrame(filtered_packets).as_matrix().T
ls_is_set = False
ls = 0
size = arr.shape
amt_rows = size[0]
for i in range(amt_rows):
    row = arr[i]
    row = le.fit_transform(row)
    if not ls_is_set:
        ls = np.array([row])
        ls_is_set = True
    else:
        ls = np.append(ls, [row], 0)
X = ls.T
y = np.array(label_actual).T

kfold = KFold(n_splits=10).split(X)

TP, FP, TN, FN = 0, 0, 0, 0

for fold in kfold:
    train_indices = fold[0]
    test_indices = fold[1]
    X_train, y_train = X[train_indices], y[train_indices]
    X_test, y_test = X[test_indices], y[test_indices]
    clf = LinearRegression()
    clf_fit = clf.fit(X_train, y_train, len(train_indices))
    y_predict = clf.predict(X_test)
    # If score is greater than 0.5, then it is probably malicious, else it is probably benign (basic Bayesian classification)
    y_predict = y_predict > 0.5
    cm = confusion_matrix(y_test, y_predict)
    tn, fp, fn, tp = cm.ravel()
    TP += tp
    FP += fp
    TN += tn
    FN += fn

print('Printing results for packet-level classification using linear regression.')
print('TP: ' + str(TP))
print('FP: ' + str(FP))
print('TN: ' + str(TN))
print('FN: ' + str(FN))

# Host level classification.
# Done by counting the amount of netflows per host and trying to get info from that.

ip_is_infected = dict()
key_set = set()
netflows_per_host = dict()
destinations_per_host = dict()

# Define infected and non-infected hosts. A host is infected if there is at least one botnet netflow with that host as source. Also count the amount of netflows per host, as well as all destinations per host.
for p in filtered_packets_host:
    label = p.label
    host = p.src
    dest = p.dst
    if not host in netflows_per_host:
        netflows_per_host[host] = 1
    else:
        netflows_per_host[host] = netflows_per_host[host] + 1
    if not host in destinations_per_host:
        s = set()
        s.add(dest)
        destinations_per_host[host] = s
    else:
        s = destinations_per_host[host]
        s.add(dest)
        destinations_per_host[host] = s
    key_set.add(host)
    if label == 'Botnet':
        ip_is_infected[host] = 1

for k in key_set:
    if not k in ip_is_infected.keys():
        ip_is_infected[k] = 0

X_1 = []
X_2 = []
y = []
for k in key_set:
    X_1.append(netflows_per_host[k])
    X_2.append(len(destinations_per_host[k]))
    y.append(ip_is_infected[k])

X = np.array([X_1])
# Note: using the amount of destinations per host resulted in a far higher FPR. As such, we ditched it.
# X = np.append(X, [X_2], 0)
X = X.T
y = np.array(y).T

kfold = KFold(n_splits=10).split(X)

TP, FP, TN, FN = 0, 0, 0, 0

for fold in kfold:
    train_indices = fold[0]
    test_indices = fold[1]
    X_train, y_train = [X[i] for i in train_indices], [y[i] for i in train_indices]
    X_train, y_train = SMOTE().fit_sample(X_train, y_train)
    X_test, y_test = [X[i] for i in test_indices], [y[i] for i in test_indices]
    clf = LinearRegression()
    clf_fit = clf.fit(X_train, y_train, len(train_indices))
    y_predict = clf.predict(X_test)
    # If score is greater than 0.5, then it is probably malicious, else it is probably benign (basic Bayesian classification)
    y_predict = y_predict > 0.5
    cm = confusion_matrix(y_test, y_predict)
    tn, fp, fn, tp = cm.ravel()
    TP += tp
    FP += fp
    TN += tn
    FN += fn

print('Printing results for host-level classification using linear regression.')
print('TP: ' + str(TP))
print('FP: ' + str(FP))
print('TN: ' + str(TN))
print('FN: ' + str(FN))