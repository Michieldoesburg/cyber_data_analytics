from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from assignment2.predictors import *
from assignment2.select_data import *

def parser(x):
    return datetime.strptime(x, '%d/%m/%y %H')

# Read data.
series = read_csv('data/BATADAL_train_dataset_1.csv', header=0, parse_dates=[0], index_col=0, date_parser=parser)

# Select keys that you want to analyze.
# This is the complete keyset: ['L_T1', 'L_T2', 'L_T3', 'L_T4', 'L_T5', 'L_T6', 'L_T7', 'F_PU1',
#        'S_PU1', 'F_PU2', 'S_PU2', 'F_PU3', 'S_PU3', 'F_PU4', 'S_PU4', 'F_PU5',
#        'S_PU5', 'F_PU6', 'S_PU6', 'F_PU7', 'S_PU7', 'F_PU8', 'S_PU8', 'F_PU9',
#        'S_PU9', 'F_PU10', 'S_PU10', 'F_PU11', 'S_PU11', 'F_V2', 'S_V2',
#        'P_J280', 'P_J269', 'P_J300', 'P_J256', 'P_J289', 'P_J415', 'P_J302',
#        'P_J306', 'P_J307', 'P_J317', 'P_J14', 'P_J422', 'ATT_FLAG']
# keys = ['S_PU1', 'S_PU2', 'S_PU3', 'S_PU4', 'S_PU5', 'S_PU6', 'S_PU7', 'S_PU8', 'S_PU9']
keys = ['L_T1', 'L_T2', 'F_PU1', 'F_PU2', 'P_J302']

# Select start and stop indices for a given data range.
# (Set end to 8762 and start to 0 for all).
start = 0
end = 300

# Select a subset of data that you want to analyze.
series = select_data(series, keys, start, end)

# Plot data.
# series.plot()
print(series.corr())

pyplot.subplot(1, 2, 1)
handles = list()
for i in keys:
    l, = pyplot.plot(series[i], label=i)
    handles.append(l)

pyplot.legend(handles, keys)

pyplot.subplot(1, 2, 2)
handles = list()
keys_plot2 = list()
keys = ['L_T1', 'F_PU1', 'P_J302']

# Make predictions.
for k in keys:
    predicted_data, actual_data = predict_data_arma(series, k, 0.66, 5, 0)
    label_predict = k + ' (Predicted)'
    label_actual = k + ' (Actual)'
    l, = pyplot.plot(predicted_data, label=label_predict)
    handles.append(l)
    l, = pyplot.plot(actual_data, label=label_actual)
    handles.append(l)
    keys_plot2.append(label_predict)
    keys_plot2.append(label_actual)

pyplot.legend(handles, keys_plot2)
pyplot.show()

series = read_csv('data/BATADAL_train_dataset_1.csv', header=0, parse_dates=[0], index_col=0, date_parser=parser)
keys = ['L_T3', 'P_J302']

series = select_data(series, keys, start, end)
pyplot.plot(series)
pyplot.show()