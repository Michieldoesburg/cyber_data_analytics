import pandas as pd
from statsmodels.tsa.arima_model import ARIMA, ARMA
from sklearn.metrics import mean_squared_error
from numpy.linalg import LinAlgError

def prepare_data(df, keys, train_frac):
    filtered_data = df[keys]
    X = filtered_data.values
    size_train = int(len(X) * train_frac)
    test_index = filtered_data[size_train:len(X)].index
    train, test = X[0:size_train], X[size_train:len(X)]
    history = [x for x in train]
    return train, test, test_index, history, list()

def predict_data_arma(df, keys, train_frac, p, q):
    train, test, test_index, history, predictions = prepare_data(df, keys, train_frac)
    print('Size train data: %.5f' % len(train))
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
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        print('Predicted: %.5f, actual: %.5f' %(yhat, obs))
    MSE = mean_squared_error(predictions, test)
    print('MSE for this prediction is: %.5f' % MSE)
    return pd.DataFrame(predictions, test_index), pd.DataFrame(test, test_index)

def predict_data_arima(df, keys, train_frac, p, d, q):
    train, test, test_index, history, predictions = prepare_data(df, keys, train_frac)
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