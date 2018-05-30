import pandas as pd
import numpy as np

def get_residual_error(predicted, actual):
    index = predicted.index
    yhat = predicted.values
    y = actual.values
    diff = yhat - y
    return pd.DataFrame(diff, index)

def get_mean_stddev(error):
    vals = error.values.T
    abs_vals = np.absolute(vals)
    mean = np.mean(abs_vals)
    stddev = np.std(abs_vals)
    return mean, stddev, abs_vals

def build_lower_upper_bounds(lower, upper, index):
    lower_list, upper_list = list(), list()
    for i in range(len(index)):
        lower_list.append(lower)
        upper_list.append(upper)
    return pd.DataFrame(lower_list, index), pd.DataFrame(upper_list, index)
