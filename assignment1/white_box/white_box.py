import read_in_data
from find_fraud_data_feature_ranges import findFeatureRanges

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

        result.append((entry.simple_journal, predict_fraud))

    return result

unfiltered_data = read_in_data.readInData('data_for_student_case.csv')
data = preProcess(unfiltered_data)

feature_ranges = findFeatureRanges()

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
