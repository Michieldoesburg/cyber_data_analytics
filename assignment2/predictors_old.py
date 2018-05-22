import pandas as pd
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.metrics import mean_squared_error

def prepare_data(df, keys, train_frac):
    filtered_data = df[keys]
    X = filtered_data.values
    size_train = int(len(X) * train_frac)
    test_index = filtered_data[size_train:len(X)].index
    train, test = X[0:size_train], X[size_train:len(X)]
    history = [x for x in train]
    return train, test, test_index, history, list()

def predict_data_expsmoothing(df, keys, train_frac, periods, trend_param, seasonal_param):
    train, test, test_index, history, predictions = prepare_data(df, keys, train_frac)
    for t in range(len(test)):
        model = ExponentialSmoothing(train, seasonal_periods=periods, seasonal=seasonal_param, trend=trend_param)
        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
    MSE = mean_squared_error(predictions, test)
    print('MSE for this prediction is: %.5f' % MSE)
    return pd.DataFrame(predictions, test_index), pd.DataFrame(test, test_index)

def predict_data_VAR(df, keys, train_frac):
    train, test, test_index, history, predictions = prepare_data(df, keys, train_frac)
    for t in range(len(test)):
        model = VAR(history)
        model_fit = model.fit(ic='aic')
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
    MSE = mean_squared_error(predictions, test)
    print('MSE for this prediction is: %.5f' % MSE)
    return pd.DataFrame(predictions, test_index), pd.DataFrame(test, test_index)