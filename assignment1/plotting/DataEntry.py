class DataEntry:
    def __init__(self, booking_date, issuer_country_code, tx_variant_code, bin, amount, currency_code, shopper_country_code, shopper_interaction,
                 simple_journal, card_ver_code_supplied, cvc_response_code, creation_date, account_code, mail_id, ip_id, card_id):
        self.booking_date = booking_date
        self.issuer_country_code = issuer_country_code
        self.tx_variant_code = tx_variant_code
        self.bin = bin
        self.amount = amount
        self.currency_code = currency_code
        self.shopper_country_code = shopper_country_code
        self.shopper_interaction = shopper_interaction
        self.simple_journal = simple_journal
        self.card_ver_code_supplied = card_ver_code_supplied
        self.cvc_response_code = cvc_response_code
        self.creation_date = creation_date
        self.account_code = account_code
        self.mail_id = mail_id
        self.ip_id = ip_id
        self.card_id = card_id

    def __str__(self):
        return "booking_date:  " + self.booking_date + '\n' + \
        "issuer_country_code: " + self.issuer_country_code + '\n' + \
        "tx_variant_code: " + self.tx_variant_code + '\n' + \
        "bin: " + self.bin + '\n' + \
        "amount: "  + str(self.amount) + '\n' + \
        "currency_code: " + self.currency_code + '\n' + \
        "shopper_country_code: " + self.shopper_country_code  + '\n' + \
        "shopper_interaction: " + self.shopper_interaction  + '\n' + \
        "simple_journal: " + self.simple_journal  + '\n' + \
        "card_ver_code_supplied: " + str(self.card_ver_code_supplied) + '\n' + \
        "cvc_response_code: " + self.cvc_response_code + '\n' + \
        "creation_date: " + self.creation_date  + '\n' + \
        "account_code: " + self.account_code + '\n' + \
        "mail_id: " + self.mail_id + '\n' + \
        "ip_id: " + str(self.ip_id)  + '\n' + \
        "card_id: " + str(self.card_id) + '\n'