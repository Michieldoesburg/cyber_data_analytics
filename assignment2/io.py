from pandas import read_csv
from pandas import datetime

key = 'F_PU2'

def parser(x):
    return datetime.strptime(x, '%d/%m/%y %H')

def read_csv_adapted(string):
    return read_csv(string, header=0, parse_dates=[0], index_col=0, date_parser=parser)