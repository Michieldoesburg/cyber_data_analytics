from pandas import read_csv
from pandas import datetime
from assignment2.select_data import *
from assignment2.SAX import *

def parser(x):
    return datetime.strptime(x, '%d/%m/%y %H')

# Read data.
series = read_csv('data/BATADAL_train_dataset_1.csv', header=0, parse_dates=[0], index_col=0, date_parser=parser)

# Select start and stop indices for a given data range.
# (Set end to 8762 and start to 0 for all).
start = 0
end = 1000

# determine word size.
size = float(end - start)
window_size = 15.0
wordsize = int(size/window_size)

key_for_prediction = 'L_T1'
train_frac = 0.66

series = select_data(series, series.keys(), start, end)

sax = SAX(wordSize=wordsize)

register = dict()

for key in series.keys():
    vals = series[key]
    SAX_discretized_data_string = sax.to_letter_rep(vals.values.T)[0]
    register[key] = SAX_discretized_data_string

