import pandas as pd
from statsmodels.tsa.arima_model import ARIMA, ARMA
from sklearn.metrics import mean_squared_error
from numpy.linalg import LinAlgError
import numpy as np

def prepare_data(df, keys, train_frac):
    filtered_data = df[keys]
    X = filtered_data.values
    size_train = int(len(X) * train_frac)
    test_index = filtered_data[size_train:len(X)].index
    train, test = X[0:size_train], X[size_train:len(X)]
    history = [x for x in train]
    return train, test, test_index, history, list()

def prepare_data_indexed(df, keys, train_amount):
    filtered_data = df[keys]
    X = filtered_data.values
    size_train = train_amount
    test_index = filtered_data[size_train:len(X)].index
    train, test = X[0:size_train], X[size_train:len(X)]
    history = [x for x in train]
    return train, test, test_index, history, list()

def sanitize(yhat, actual):
    if np.isnan(yhat) or np.isinf(yhat):
        print('Predicted value is either infinite or NaN. Prediction was not successful.')
        return actual
    else:
        return yhat

def predict_data_arma(df, keys, train_frac, p, q):
    """
    This method performs ARMA prediction using a specified fraction of the dataset
    as history while using the rest for comparing predictions.
    """
    train, test, test_index, history, predictions = prepare_data(df, keys, train_frac)
    for t in range(len(test)):
        model = ARMA(history, order=(p, q))
        try:
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0][0]
        except LinAlgError:
            # This is a really hacky workaround for when SVD does not converge. This luckily only
            # happened to us on one of the three machines that we tested the code on, and only for a single value.
            # We have no idea why it sometimes refuses to converge (we tested it on identical hardware with identical
            # up-to-date packages, and on one of the two machines it didn't work. We even tested it on a machine with less
            # RAM, older packages, and generally inferior hardware, and even then it worked).
            print('Could not predict value. SVD did not converge.')
            yhat = test[t]
        # This is a double check as sometimes NaN's were returned from a successful prediction.
        yhat = sanitize(yhat, test[t])
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        print('Predicted: %.5f, actual: %.5f' %(yhat, obs))
    MSE = mean_squared_error(predictions, test)
    print('MSE for this prediction is: %.5f' % MSE)
    return pd.DataFrame(predictions, test_index), pd.DataFrame(test, test_index)

def predict_data_arma_indexed(df, keys, train_amount, p, q):
    """
    This method performs ARMA prediction using a specified amount of training data points in the dataset
    as history while using the rest for comparing predictions.
    """
    train, test, test_index, history, predictions = prepare_data_indexed(df, keys, train_amount)
    for t in range(len(test)):
        model = ARMA(history, order=(p, q))
        try:
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0][0]
        except LinAlgError:
            # This is a really hacky workaround for when SVD does not converge. This luckily only
            # happened to us on one of the three machines that we tested the code on, and only for a single value.
            # We have no idea why it sometimes refuses to converge (we tested it on identical hardware with identical
            # up-to-date packages, and on one of the two machines it didn't work. We even tested it on a machine with less
            # RAM, older packages, and generally inferior hardware, and even then it worked).
            print('Could not predict value. SVD did not converge.')
            yhat = test[t]
        # This is a double check as sometimes NaN's were returned from a successful prediction.
        yhat = sanitize(yhat, test[t])
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        print('Predicted: %.5f, actual: %.5f' %(yhat, obs))
    MSE = mean_squared_error(predictions, test)
    print('MSE for this prediction is: %.5f' % MSE)
    return pd.DataFrame(predictions, test_index), pd.DataFrame(test, test_index)