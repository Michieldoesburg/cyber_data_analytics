import csv
import matplotlib.pyplot as plt
import pylab
from random import randint

data = []
fraud_data = []
non_fraud_data = []
fraud_all = {}
non_fraud_all = {}
currency_codes = set()

with open('data_for_student_case.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        if row[5] == 'amount':
            continue


        amount = float(row[5])
        currency_code = row[6]
        simple_journal = row[9]
        id = row[15]

        # 25 april / 2018 exchange rates
        if currency_code == "AUD":
            amount = 0.62 * amount
        if currency_code == "MXN":
            amount = 0.04 * amount
        if currency_code == "GBP":
            amount = 1.14 * amount
        if currency_code == "NZD":
            amount = 0.58 * amount
        if currency_code == "SEK":
            amount = 0.095 * amount

        if simple_journal != 'Chargeback':
            non_fraud_data.append(amount)
            if id in non_fraud_all:
                non_fraud_all[id] = [amount]
            else:
                non_fraud_all[id] = non_fraud_all[id].append(amount)
        if simple_journal == 'Chargeback':
            fraud_data.append(amount)
            if id in fraud_all:
                fraud_all[id] = [amount]
            else:
                fraud_all[id] = fraud_all[id].append(amount)


nf_sample_data = []

non_fraud_avg = {}
fraud_avg = {}
for i in fraud_all:
    fraud_list = fraud_all[i]
    fraud_avg = sum(fraud_list)/float(len(fraud_list))
    non_fraud_list = non_fraud_all[i]
    non_fraud_avg = sum(non_fraud_list)/float(len(non_fraud_list))

while(nf_sample_data.__len__() < 345):

    index = randint(0, non_fraud_data.__len__())

    nf_sample_data.append(non_fraud_data[index])

# Ignore this, was working on something that is not good for the question.
fraud_data = []
non_fraud_data = []

plt.scatter([xrange(0, fraud_data.__len__())], fraud_data, c="red")
#plt.scatter([xrange(0, nf_sample_data.__len__())], nf_sample_data, c="blue")
plt.scatter([xrange(0, non_fraud_data.__len__())], non_fraud_data, c="blue")
plt.xlabel('Fraudulent vs non-fraudulent amount in transaction (normalized)')

plt.show()