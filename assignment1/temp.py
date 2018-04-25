import csv
import matplotlib.pyplot as plt
import pylab
from random import randint

data = []
fraud_data = []
non_fraud_data = []
currency_codes = set()

with open('data_for_student_case.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        if row[5] == 'amount':
            continue


        amount = float(row[5])
        currency_code = row[6]
        simple_journal = row[9]

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
        if simple_journal == 'Chargeback':
            fraud_data.append(amount)

nf_sample_data = []

while(nf_sample_data.__len__() < 345):

    index = randint(0, non_fraud_data.__len__())

    nf_sample_data.append(non_fraud_data[index])

plt.scatter([xrange(0, fraud_data.__len__())], fraud_data, c="red")
plt.scatter([xrange(0, nf_sample_data.__len__())], nf_sample_data, c="blue")
plt.xlabel('Fraudulent vs non-fraudulent amount in transaction (normalized)')

plt.show()