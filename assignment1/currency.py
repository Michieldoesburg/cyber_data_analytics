def currency(amount, currency_code):
    res = 0
    if currency_code == "AUD":
        res = 0.62 * amount
    if currency_code == "MXN":
        res = 0.04 * amount
    if currency_code == "GBP":
        res = 1.14 * amount
    if currency_code == "NZD":
        res = 0.58 * amount
    if currency_code == "SEK":
        res = 0.095 * amount
    return res