import read_in_data


# Find the highest ratio keys
def findHighRatioKeys(dict):
        value = 0.0
        keys = []

        while (value < 0.8):
            max_key = max(dict.iterkeys(), key=(lambda key: dict[key]))
            keys.append(max_key)
            value += dict[max_key]
            dict.pop(max_key)

        return keys


def findFeatureRanges():
    data = read_in_data.readInData('only_fraud_data.csv')

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
    '''
    print(isser_country_code_set)
    print(tx_variant_code_set)
    print(bin_set)
    print(shopper_interaction_set)
    print(card_verification_set)
    print(cvc_response_set)
    print(account_code_set)

    print(isser_country_code_dict)
    print(tx_variant_code_dict)
    print(bin_dict)
    print(shopper_interaction_dict)
    print(card_verification_dict)
    print(cvc_response_dict)
    print(account_code_dict)'''

    feature_ranges = {}
    '''
    feature_ranges["issuer_country_code"] = isser_country_code_set
    feature_ranges["tx_variant_code"] = tx_variant_code_set
    feature_ranges["bin"] = bin_set
    feature_ranges["shopper_interaction"] = shopper_interaction_set
    feature_ranges["card_verification"] = card_verification_set
    feature_ranges["cvc_response"] = cvc_response_set
    feature_ranges["account_code"] = account_code_set'''

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
    print( feature_ranges["card_verification"])
    print(feature_ranges["cvc_response"])
    print(feature_ranges["account_code"] )

    return feature_ranges

