import csv
from DataEntry import DataEntry
import matplotlib.pyplot as plt
import numpy as np

"""
This file plots the amount of fraud vs non fraud transactions per credit card number and email. 
"""

data_entries = []
def readInData():
    with open('../data_for_student_case.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[5] == 'amount':
                continue

            """(self, booking_date, issuer_country_code, tx_variant_code, bin, amount, currency_code, shopper_country_code, shopper_interaction,
                simple_journal, card_ver_code_supplied, cvc_response_code, creation_date, account_code, mail_id, ip_id, card_id)"""

            booking_date = row[1]
            issuer_country_code = row[2]
            tx_variant_code = (row[3])
            bin = row[4]
            amount = float(row[5])
            currency_code = row[6]
            shopper_country_code = row[7]
            shopper_interaction = row[8]
            simple_journal = row[9]
            card_ver_code_supplied = bool(row[10])
            cvc_response_code = row[11]
            creation_date = row[12]
            account_code = row[13]
            mail_id = row[14]
            ip_id = row[15]
            card_id = row[16]

            data_entry = DataEntry(booking_date, issuer_country_code, tx_variant_code, bin, amount, currency_code, shopper_country_code, shopper_interaction,
                                   simple_journal, card_ver_code_supplied, cvc_response_code, creation_date, account_code, mail_id, ip_id, card_id)

            data_entries.append(data_entry)

readInData()


num_trans_per_cc_dict = {}

for entry in data_entries:
    num_trans_per_cc_dict[entry.card_id] = num_trans_per_cc_dict.get(entry.card_id, 0) + 1

data = num_trans_per_cc_dict
names = list(data.keys())
values = list(data.values())

X = data.keys()
X = X[:1000]
Y = []
#Z = []]

for x in X:
    Y.append(data.get(x, 0))
    #Z.append(data.get(x, 0)[1])

_X = np.arange(len(X))

plt.bar(_X - 0.2, Y, 0.4)
#plt.bar(_X + 0.2, Z, 0.4)
plt.xticks(_X, X) # set labels manually

plt.show()
