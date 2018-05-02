import read_in_data

data = read_in_data.readInData('../only_fraud_data.csv')

isser_country_code_set = set()
tx_variant_code_set = set()
bin_set = set()
shopper_interaction_set = set()
card_verification_set = set()
cvc_response_set = set()
account_code_set = set()


for entry in data:
    isser_country_code_set.add(entry.issuer_country_code)
    tx_variant_code_set.add(entry.tx_variant_code)
    bin_set.add(entry.bin)
    shopper_interaction_set.add(entry.shopper_interaction)
    card_verification_set.add(entry.card_ver_code_supplied)
    cvc_response_set.add(entry.cvc_response_code)
    account_code_set.add(entry.account_code)

print(isser_country_code_set)
print(tx_variant_code_set)
print(bin_set)
print(shopper_interaction_set)
print(card_verification_set)
print(cvc_response_set)
print(account_code_set)
