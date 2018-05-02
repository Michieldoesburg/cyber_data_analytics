import read_in_data

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

def classify(data):
    result = []

    for entry in data:
        actual_chargeback = entry.simple_journal

        #if entry.amount < 800 && entry.shopper_country_code == "MX"


unfiltered_data = read_in_data.readInData('data_for_student_case.csv')
data = preProcess(unfiltered_data)

