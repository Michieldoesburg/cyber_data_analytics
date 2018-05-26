from pandas import read_csv
from pandas import datetime
from assignment2.select_data import *
from assignment2.SAX import *
from assignment2.NGram_methods import *
from matplotlib import pyplot
import pandas as pd
import ngram as ng

def get_PAA_sequence(df, key, ws):
    sax = SAX(wordSize=ws)
    res = sax.to_PAA(sax.normalize(df[key].values))
    mean = np.mean(df[key].values)
    std = np.std(df[key].values)
    values = res[0]
    tuples = res[1]
    discretized_data = list()
    for i in range(len(values)):
        value = values[i]
        tuple = tuples[i]
        r = tuple[1] - tuple[0]
        for i in range(r):
            discretized_data.append(value)
    discretized_data = [x*std for x in discretized_data]
    discretized_data = [x + mean for x in discretized_data]
    return pd.DataFrame(index=df.index, data=discretized_data)

def parser(x):
    return datetime.strptime(x, '%d/%m/%y %H')

def find_malicious_data(scores, mean, std):
    potential_malicious_indices = list()
    min_threshold = max(mean - 3.0*std, 0.3)
    for i in scores.keys():
        if scores[i] < min_threshold:
            potential_malicious_indices.append(i)
    return combine_tuples(potential_malicious_indices)

def combine_tuples(tuples):
    if len(tuples) == 0:
        return list()
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
window_size = 3.0
wordsize = int(size/window_size)

wordsizes = dict()
for k in series.keys():
    wordsizes[k] = wordsize

series = select_data(series, series.keys(), start, end)

ngm = NGram_methods(series, wordsizes)

pyplot.plot(series['L_T1'])
pyplot.plot(get_PAA_sequence(series, 'L_T1', wordsize))
pyplot.show()

series_malicious = read_csv('data/BATADAL_test_dataset.csv', header=0, parse_dates=[0], index_col=0, date_parser=parser)
signal = series_malicious[key].values
dict = ngm.analyze_signal(signal, key)
ngm.overview_scores(list(dict.values()))
mean, std, _, _ = ngm.get_scores(list(dict.values()))
malicious_indices = find_malicious_data(dict, mean, std)
print('These parts of the signal might contain attacks:')
print(malicious_indices)