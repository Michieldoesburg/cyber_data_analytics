import csv
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

counts = {}
ratios = {}
num_fraud = 0.0

with open('../data_for_student_case.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        if row[5] == 'amount':
            continue

        amount = float(row[5])
        currency_code = row[6]
        shopper_cc = row[7]
        simple_journal = row[9]

        if(simple_journal) == 'Chargeback':
            num_fraud += 1
            counts[shopper_cc] = counts.get(shopper_cc, 0) + 1

for key in counts.keys():
    ratios[key] = counts[key]/num_fraud

data = counts
names = list(data.keys())
values = list(data.values())

plt.bar(names, values)
plt.suptitle('# of fraudulent transactions per country code')

plt.show()