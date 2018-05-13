import read_in_data
from find_fraud_data_feature_ranges import findFeatureRanges
from assignment1.currency import currency
import csv
from DataEntry import DataEntry

def readInData(filename):
    """
    Read in all the entries from the .csv and create a list of objects out of it.
    :return:
    """
    data_entries = []

    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[5] == 'amount': #skip the header row
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
            card_ver_code_supplied = row[10]
            cvc_response_code = row[11]
            creation_date = row[12]
            account_code = row[13]
            mail_id = row[14]
            ip_id = row[15]
            card_id = row[16]

            data_entry = DataEntry(booking_date, issuer_country_code, tx_variant_code, bin, amount, currency_code, shopper_country_code, shopper_interaction,
                                   simple_journal, card_ver_code_supplied, cvc_response_code, creation_date, account_code, mail_id, ip_id, card_id)

            data_entries.append(data_entry)

    return data_entries


def preProcess(data_entries):
    """
    Remove all the entries from the list we don't want.
    :param data_entries:
    :return:
    """
    final_list = []

    for entry in data_entries:
        if entry.simple_journal == "Refused":
            continue

        final_list.append(entry)

    return final_list

def classify(data, feature_ranges):
    result = []

    predict_fraud = True

    for entry in data:
        if not entry.bin in feature_ranges["bin"]:
            predict_fraud = False
        if not entry.tx_variant_code in feature_ranges["tx_variant_code"]:
            predict_fraud = False
        if not entry.issuer_country_code in feature_ranges["issuer_country_code"]:
            predict_fraud = False
        if not entry.card_ver_code_supplied in feature_ranges["card_verification"]:
            predict_fraud = False
        if not entry.cvc_response_code in feature_ranges["cvc_response"]:
            predict_fraud = False
        if not entry.account_code in feature_ranges["account_code"]:
            predict_fraud = False
        if not entry.shopper_interaction in feature_ranges["shopper_interaction"]:
            predict_fraud = False
        amount_in_euros = currency(entry.amount, entry.currency_code)
        if amount_in_euros > 80000.0:
            predict_fraud = False

        result.append((entry.simple_journal, predict_fraud))

    return result

unfiltered_data = readInData('data_for_student_case.csv')
data = preProcess(unfiltered_data)
train_data = readInData('only_fraud_data.csv')

feature_ranges = findFeatureRanges(train_data)

result = classify(data, feature_ranges)

TP, FP, TN, FN = 0, 0, 0, 0

for tuple in result:
    if tuple[0] == 'Chargeback' and tuple[1] == True:
        TP += 1
    if tuple[0] == 'Settled' and tuple[1] == True:
        FP += 1
    if tuple[0] == 'Chargeback' and tuple[1] == False:
        FN += 1
    if tuple[0] == 'Settled' and tuple[1] == False:
        TN += 1

print("TP: " + str(TP))
print("FP: " + str(FP))
print("TN: " + str(TN))
print("FN: " + str(FN))
