from pandas import read_csv
from pandas import datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.api import ExponentialSmoothing
from pandas.plotting import autocorrelation_plot
from sklearn.metrics import mean_squared_error


def get_corrs(df):
    col_correlations = df.corr()
    col_correlations.loc[:, :] = np.tril(col_correlations, k=-1)
    cor_pairs = col_correlations.stack()
    return cor_pairs.to_dict()

def parser(x):
    return datetime.strptime(x, '%d/%m/%y %H')

def predict_data_arima(df, keys, train_frac, p, d, q):
    filtered_data = df[keys]
    X = filtered_data.values
    size_train = int(len(X) * train_frac)
    test_index = filtered_data[size_train:len(X)].index
    train, test = X[0:size_train], X[size_train:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(p, d, q))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
    MSE = mean_squared_error(predictions, test)
    print('MSE for this prediction is: %.5f' % MSE)
    return pd.DataFrame(predictions, test_index), pd.DataFrame(test, test_index)

def predict_data_expsmoothing(df, keys, train_frac, periods, trend_param, seasonal_param):
    filtered_data = df[keys]
    size_data = len(filtered_data.index)
    size_train = int(size_data * train_frac)
    train, test = filtered_data[0:size_train], filtered_data[size_train:size_data]
    fit = ExponentialSmoothing(np.asarray(train), seasonal_periods=periods, seasonal=seasonal_param, trend=trend_param).fit()
    yhat = fit.forecast(len(test.index))
    MSE = mean_squared_error(np.asarray(test), np.asarray(yhat))
    print('MSE for this prediction is: %.5f' % MSE)
    return pd.DataFrame(yhat, test.index), test


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
keys = ['L_T1', 'L_T2', 'F_PU1', 'F_PU2']

# Select start and stop indices for a given data range.
# (Set end to 8762 and start to 0 for all).
start = 0
end = 500

# Select a subset of data that you want to analyze.
series = series[keys]
series = series[start:end]

# Plot data.
# series.plot()
print(series.corr())

# Predict data.
# Necessary parameters for fine-tuning.
key_for_prediction = 'L_T1'
train_frac = 0.66
p = 7
d = 1
q = 0

periods = 10
trend_param = 'add'
seasonal_param = 'mul'

# Predict and plot data.
predicted_data_arima, actual_data = predict_data_arima(series, key_for_prediction, train_frac, p, d, q)
predicted_data_es, actual_data = predict_data_expsmoothing(series, key_for_prediction, train_frac, periods, trend_param, seasonal_param)
pyplot.plot(predicted_data_arima,color='red')
pyplot.plot(predicted_data_es,color='green')
pyplot.plot(actual_data)

pyplot.show()