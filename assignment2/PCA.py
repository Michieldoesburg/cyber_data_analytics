from assignment2.io import read_csv_adapted
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize
from matplotlib import pyplot
import numpy as np
from numpy import linalg as LA
from assignment2.residual_error import build_lower_upper_bounds

def set_to_zero_mean(df):
    data = []
    index = df.index
    mean = df.mean(axis=0).values
    columns = df.columns
    for row in df.iterrows():
        r = row[1].values - mean
        data.append(r)
    return pd.DataFrame(index=index, data=data, columns=columns)

def PCA_decompose(df, comps, solver='auto'):
    data = df.values
    index = df.index
    columns = ['Component %i' % x for x in range(1, comps + 1)]
    pca = PCA(n_components=comps, svd_solver=solver)
    new_data = pca.fit_transform(data)
    return pd.DataFrame(index=index, data=new_data, columns=columns), normalize(pca.components_.T, axis=1, norm='l2')

def set_zero_mean_decompose(df, comps, keys_to_drop, solver='auto'):
    new_df = df
    new_df.drop(keys_to_drop, axis=1)
    # new_df = set_to_zero_mean(new_df)
    return PCA_decompose(new_df, comps, solver)

def generate_list_outliers(train_data, test_data, test_data_indices, clf):
    predictions = clf.fit(train_data).predict(test_data)
    outlier_indices = list()
    for i in range(len(predictions)):
        if predictions[i] == -1:
            outlier_indices.append(test_data_indices[i].strftime('%d-%m-%Y %H:00:00'))

    return outlier_indices


# Read data.
test_data = read_csv_adapted('data/BATADAL_test_dataset.csv')

# 30 principal components has been found to give a good signal where anomalies were clear.
principal_comps = 30
decomposed_test_data, comps_test = set_zero_mean_decompose(test_data, principal_comps, [])

P = comps_test
P_P_T = np.dot(P, P.T)
amt = P_P_T.shape[0]
I = np.identity(amt)
C = np.subtract(I, P_P_T)

y = test_data.values.T
Cy = np.dot(C, y)

Cy2 = LA.norm(Cy, axis=0)**2.0

mean = np.mean(Cy2)
std = np.std(Cy2)

upper = mean + 3.0*std
lower = mean - 3.0*std

low, up = build_lower_upper_bounds(lower, upper, test_data.index)
anomalous_indices = list()
for i in range(len(Cy2)):
    val = Cy2[i]
    if val < lower or val > upper:
        anomalous_indices.append(test_data.index[i].strftime('%d-%m-%Y %H:00:00'))

print('%i anomalies detected.' % len(anomalous_indices))
print('These timestamps contain anomalies:')
print(anomalous_indices)

# Plot of PCA residuals of training set.
pyplot.plot(pd.DataFrame(data=Cy2, index=test_data.index))
pyplot.plot(low,color='red')
pyplot.plot(up,color='red')
pyplot.show()