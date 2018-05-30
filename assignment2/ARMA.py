from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from assignment2.predictors import *
from statsmodels.tsa.arima_model import ARMAResults
from assignment2.select_data import *
from assignment2.residual_error import *
from math import inf

def determine_params_by_AIC(df, keys, train_frac):
    """
    This function determines ideal p and q by using the AIC as a measure.
    """
    _, _, _, history, _ = prepare_data(df, keys, train_frac)
    potential_p = range(7)
    potential_q = range(3)
    best_p, best_q = 0, 0
    min_AIC = inf
    for i in potential_p:
        for j in potential_q:
            try:
                print('Testing: (%i, %i)' % (i, j))
                model = ARMA(history, order=(i,j))
                model_fit = model.fit(disp=0)
                candidate_AIC = float(ARMAResults.summary(model_fit).tables[0].data[3][3])
                if candidate_AIC < min_AIC:
                    min_AIC = candidate_AIC
                    best_p = i
                    best_q = j
            except RuntimeWarning:
                pass
            except:
                pass
    return best_p, best_q

def parser(x):
    return datetime.strptime(x, '%d/%m/%y %H')

# Read data.
series = read_csv('data/BATADAL_train_dataset_1.csv', header=0, parse_dates=[0], index_col=0, date_parser=parser)
all_keys = series.keys()

# Select keys that you want to analyze.
# This is the complete keyset: ['L_T1', 'L_T2', 'L_T3', 'L_T4', 'L_T5', 'L_T6', 'L_T7', 'F_PU1',
#        'S_PU1', 'F_PU2', 'S_PU2', 'F_PU3', 'S_PU3', 'F_PU4', 'S_PU4', 'F_PU5',
#        'S_PU5', 'F_PU6', 'S_PU6', 'F_PU7', 'S_PU7', 'F_PU8', 'S_PU8', 'F_PU9',
#        'S_PU9', 'F_PU10', 'S_PU10', 'F_PU11', 'S_PU11', 'F_V2', 'S_V2',
#        'P_J280', 'P_J269', 'P_J300', 'P_J256', 'P_J289', 'P_J415', 'P_J302',
#        'P_J306', 'P_J307', 'P_J317', 'P_J14', 'P_J422', 'ATT_FLAG']
# keys = ['S_PU1', 'S_PU2', 'S_PU3', 'S_PU4', 'S_PU5', 'S_PU6', 'S_PU7', 'S_PU8', 'S_PU9']

# Select start and stop indices for a given data range.
# (Set end to 8762 and start to 0 for all).
start = 0
end = 300

key_for_prediction = 'L_T1'
train_frac = 0.95

series = select_data(series, series.keys(), start, end)
p, q = determine_params_by_AIC(series, key_for_prediction, train_frac)
print('Best parameter combination: (p,q) = ('+str(p)+','+str(q)+')')

predicted_data_arma, actual_data = predict_data_arma(series, key_for_prediction, train_frac, p, q)
pyplot.subplot(1, 2, 1)
pyplot.plot(predicted_data_arma,color='red')
pyplot.plot(actual_data)
pyplot.subplot(1, 2, 2)
error = get_residual_error(predicted_data_arma, actual_data)

mean, stddev, abs_err = get_mean_stddev(error)
lower = -mean - 3.0*stddev
upper = mean + 3.0*stddev
print('Lower bound: %.5f, upper bound: %.5f' % (lower, upper))

attack_indices = list()
for i in range(len(abs_err)):
    if abs_err[0][i] > upper:
        attack_indices.append(abs_err.index[i])

print('Indices with potential attacks:')
print(attack_indices)

lower_bound, upper_bound = build_lower_upper_bounds(lower, upper, error.index)
pyplot.plot(error)
pyplot.plot(lower_bound,color='red')
pyplot.plot(upper_bound,color='red')
pyplot.show()