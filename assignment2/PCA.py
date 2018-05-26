from assignment2.io import read_csv_adapted
import pandas as pd
from sklearn.decomposition import PCA

key = 'F_PU2'

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
    return pd.DataFrame(index=index, data=new_data, columns=columns)

# Read data.
series = read_csv_adapted('data/BATADAL_train_dataset_1.csv')

# Select start and stop indices for a given data range.
# (Set end to 8762 and start to 0 for all).
start = 0
end = 8700

new_series = set_to_zero_mean(series)
new_series.drop('ATT_FLAG', axis=1, inplace=True)

decomposed_data = PCA_decompose(new_series, 2)
