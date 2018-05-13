import csv

from assignment1.white_box.DataEntry import DataEntry


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