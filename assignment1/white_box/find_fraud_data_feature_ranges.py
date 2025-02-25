import read_in_data
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

# Find the highest ratio keys
def findHighRatioKeys(dict):
        # As a check, normalize the values first.
        # Compute total sum of values.
        sum = 0.0
        for i in dict.iterkeys():
            sum += dict[i]

        # Normalize all values by dividing over sum.
        for i in dict.iterkeys():
            dict[i] = float(dict[i])/float(sum)

        value = 0.0
        keys = []

        # Find the keys for a dictionary that maps strings to numerical values
        # which, when the values are summed, account for at least 80% of the
        # total sum of values.
        while (value < 0.8):
            max_key = max(dict.iterkeys(), key=(lambda key: dict[key]))
            keys.append(max_key)
            value += dict[max_key]
            dict.pop(max_key)

        return keys

# Find the values of the features for which there is at least one fraudulent transaction with that value.
def findFeatureRanges(data):

    # Count the number of entries to conver counts to ratios later.
    num_entries = 0.0

    isser_country_code_set = set()
    tx_variant_code_set = set()
    bin_set = set()
    shopper_interaction_set = set()
    card_verification_set = set()
    cvc_response_set = set()
    account_code_set = set()

    isser_country_code_dict = {}
    tx_variant_code_dict = {}
    bin_dict = {}
    shopper_interaction_dict = {}
    card_verification_dict = {}
    cvc_response_dict = {}
    account_code_dict = {}

    for entry in data:
        num_entries += 1

        # Add entry features to sets.
        isser_country_code_set.add(entry.issuer_country_code)
        tx_variant_code_set.add(entry.tx_variant_code)
        bin_set.add(entry.bin)
        shopper_interaction_set.add(entry.shopper_interaction)
        card_verification_set.add(entry.card_ver_code_supplied)
        cvc_response_set.add(entry.cvc_response_code)
        account_code_set.add(entry.account_code)

        # Count the occurences of the entry's features.
        isser_country_code_dict[entry.issuer_country_code] = isser_country_code_dict.get(entry.issuer_country_code, 0) + 1
        tx_variant_code_dict[entry.tx_variant_code] = tx_variant_code_dict.get(entry.tx_variant_code, 0) + 1
        bin_dict[entry.bin] = bin_dict.get(entry.bin, 0) + 1
        shopper_interaction_dict[entry.shopper_interaction] = shopper_interaction_dict.get(entry.shopper_interaction, 0) + 1
        card_verification_dict[entry.card_ver_code_supplied] = card_verification_dict.get(entry.card_ver_code_supplied, 0) + 1
        cvc_response_dict[entry.cvc_response_code] = cvc_response_dict.get(entry.cvc_response_code, 0) + 1
        account_code_dict[entry.account_code] = account_code_dict.get(entry.account_code, 0) + 1

    dicts = [isser_country_code_dict,
    tx_variant_code_dict,
    bin_dict,
    shopper_interaction_dict,
    card_verification_dict,
    cvc_response_dict,
    account_code_dict]

    # Convert the counts to ratios
    for dict in dicts:
        for key in dict.keys():
            dict[key] = dict[key] / num_entries

        print(dict)

    feature_ranges = {}

    feature_ranges["issuer_country_code"] = findHighRatioKeys(isser_country_code_dict)
    feature_ranges["tx_variant_code"] = tx_variant_code_set
    feature_ranges["bin"] = bin_set
    feature_ranges["shopper_interaction"] = shopper_interaction_set
    feature_ranges["card_verification"] = card_verification_set
    feature_ranges["cvc_response"] = cvc_response_set
    feature_ranges["account_code"] = account_code_set

    print(feature_ranges["issuer_country_code"])
    print(feature_ranges["tx_variant_code"])
    print(feature_ranges["bin"])
    print(feature_ranges["shopper_interaction"])
    print(feature_ranges["card_verification"])
    print(feature_ranges["cvc_response"])
    print(feature_ranges["account_code"])

    return feature_ranges

