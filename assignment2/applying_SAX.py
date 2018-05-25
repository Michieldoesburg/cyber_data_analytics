from pandas import read_csv
from pandas import datetime
from assignment2.select_data import *
from assignment2.SAX import *
from assignment2.NGram_methods import *
import ngram as ng

def parser(x):
    return datetime.strptime(x, '%d/%m/%y %H')

def find_malicious_data(scores, mean, std):
    potential_malicious_indices = list()
    min_threshold = mean - 2.0*std
    for i in scores.keys():
        if scores[i] < min_threshold:
            potential_malicious_indices.append(i)
    return combine_tuples(potential_malicious_indices)

def combine_tuples(tuples):
    res = list()
    temp_tuple = tuples[0]
    for i in range(1, len(tuples)):
        new_tuple = tuples[i]
        # If tuples overlap, merge them.
        if new_tuple[0] <= temp_tuple[1]:
            temp_tuple = (temp_tuple[0], new_tuple[1])
        else:
            res.append(temp_tuple)
            temp_tuple = new_tuple
    return res

key = 'F_PU2'

# Read data.
series = read_csv('data/BATADAL_train_dataset_1.csv', header=0, parse_dates=[0], index_col=0, date_parser=parser)

# Select start and stop indices for a given data range.
# (Set end to 8762 and start to 0 for all).
start = 0
end = 8700

# determine word size.
size = float(end - start)
window_size = 5.0
wordsize = int(size/window_size)

wordsizes = dict()
for k in series.keys():
    wordsizes[k] = wordsize

series = select_data(series, series.keys(), start, end)

ngm = NGram_methods(series, wordsizes)
print(ngm.dictionary)

series_malicious = read_csv('data/BATADAL_test_dataset.csv', header=0, parse_dates=[0], index_col=0, date_parser=parser)
signal = series_malicious[key].values
dict = ngm.analyze_signal(signal, key)
ngm.overview_scores(list(dict.values()))
mean, std, _, _ = ngm.get_scores(list(dict.values()))
malicious_indices = find_malicious_data(dict, mean, std)
print('These parts of the signal might contain attacks:')
print(malicious_indices)