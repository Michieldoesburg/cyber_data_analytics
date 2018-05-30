from assignment2.select_data import *
from assignment2.SAX import *
from assignment2.NGram_methods import *
from matplotlib import pyplot
import pandas as pd
from assignment2.io import read_csv_adapted

def get_PAA_sequence(df, key, ws):
    """
    This function takes a sequence, and outputs the PP-discretization of the sequence.
    """
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

def get_timestamps_from_tuples(tuples, timestamps):
    res = list()
    for t in tuples:
        res.append((timestamps[t[0]], timestamps[t[1]]))
    return res

def find_malicious_data(scores, mean, std, min):
    """
    This function takes the scores and checks if they are below the minimum threshold.
    This threshold is the largest of either the mean minus three times the standard deviation,
    or 0.3.
    """
    potential_malicious_indices = list()
    min_threshold = max(mean - 3.0*std, min)
    for i in scores.keys():
        if scores[i] <= min_threshold:
            potential_malicious_indices.append(i)
    return combine_tuples(potential_malicious_indices)

def combine_tuples(tuples):
    """
    This function takes a list of tuples, and combines
    these tuples if they have overlapping ranges. For example,
    if the tuples (1, 5) and (3, 8) are in the list, the new list would contain a tuple
    with values (1, 8)
    """
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
series = read_csv_adapted('data/BATADAL_train_dataset_1.csv')

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

key = 'F_PU1'

#pyplot.plot(series[key])
#pyplot.plot(get_PAA_sequence(series, key, wordsize))
#pyplot.show()

series_malicious = read_csv_adapted('data/BATADAL_test_dataset.csv')
signal = series_malicious[key].values
word_size_test = len(series_malicious[key])/window_size
dict = ngm.analyze_signal(signal, word_size_test, key)
ngm.overview_scores(list(dict.values()))
mean, std, min, _ = ngm.get_scores(list(dict.values()))
malicious_indices = find_malicious_data(dict, mean, std, min)

print('These parts of the signal might contain attacks:')
print(malicious_indices)

for x in malicious_indices:
    pyplot.axvspan(x[0], int(x[0]+5), facecolor='0.2', alpha=0.5)


malicious_timestamps = get_timestamps_from_tuples(malicious_indices, series_malicious.index)
print('These time periods might contain attacks:')
print(malicious_timestamps)

pyplot.plot(signal)
pyplot.show()