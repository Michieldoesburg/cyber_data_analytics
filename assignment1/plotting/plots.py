import csv
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
"""
This file plots the percentage of non-fraudulent vs percentage of fraudulent transactions per issuer.
"""
counts = {}
nf_counts = {}
num_fraud = 0.0
num_nonfraud = 0.0

with open('../data_for_student_case.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        if row[5] == 'amount':
            continue

        tx_variant_code = (row[3])
        amount = float(row[5])
        currency_code = row[6]
        shopper_cc = row[7]
        simple_journal = row[9]

        if(simple_journal) == 'Chargeback':
            counts[tx_variant_code] = counts.get(tx_variant_code, 0) + 1
            num_fraud += 1
        else:
            num_nonfraud += 1
            nf_counts[tx_variant_code] = nf_counts.get(tx_variant_code, 0) + 1

for x in counts.keys():
    counts[x] = counts[x] / num_fraud

for x in nf_counts.keys():
    nf_counts[x] = nf_counts[x] / num_nonfraud

final_dict = {}
for key in nf_counts.keys():
    final_dict[key] = [nf_counts.get(key, 0), counts.get(key, 0)]

data = final_dict
names = list(data.keys())
values = list(data.values())

X = data.keys()
Y = []
Z = []

for x in X:
    Y.append(data.get(x, 0)[0])
    Z.append(data.get(x, 0)[1])

_X = np.arange(len(X))

plt.bar(_X - 0.2, Y, 0.4)
plt.bar(_X + 0.2, Z, 0.4)
plt.xticks(_X, X) # set labels manually

plt.suptitle("Percentage of non-fraudulent vs percentage of fraudulent transactions per issuer.")
plt.show()


#plt.figure()
#plt.subplot(1,1,1)
#plt.bar(names, values)

#plt.subplot(2,1,2)
#plt.bar(names, np.column_stack((values, values2)))

