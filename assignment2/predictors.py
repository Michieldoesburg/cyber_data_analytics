import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA, ARMA
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.metrics import mean_squared_error

def predict_data_arma(df, keys, train_frac, p, d, q):
    filtered_data = df[keys]
    X = filtered_data.values
    size_train = int(len(X) * train_frac)
    test_index = filtered_data[size_train:len(X)].index
    train, test = X[0:size_train], X[size_train:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARMA(history, order=(p, d, q))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
    MSE = mean_squared_error(predictions, test)
    print('MSE for this prediction is: %.5f' % MSE)
    return pd.DataFrame(predictions, test_index), pd.DataFrame(test, test_index)

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
