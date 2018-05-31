from assignment2.io import read_csv_adapted
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from matplotlib import pyplot

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

def set_zero_mean_decompose(df, comps, keys_to_drop, solver='auto'):
    new_df = df
    new_df.drop(keys_to_drop, axis=1)
    new_df = set_to_zero_mean(new_df)
    return PCA_decompose(new_df, comps, solver)

def generate_list_outliers(train_data, test_data, test_data_indices, clf):
    predictions = clf.fit(train_data).predict(test_data)
    outlier_indices = list()
    for i in range(len(predictions)):
        if predictions[i] == -1:
            outlier_indices.append(test_data_indices[i])

    return outlier_indices


# Read data.
train_data = read_csv_adapted('data/BATADAL_train_dataset_1.csv')
test_data = read_csv_adapted('data/BATADAL_test_dataset.csv')

# Eight principal components has been found to not detect too much anomalies for the isolation forest while still detecting some.
principal_comps = 8

decomposed_train_data = set_zero_mean_decompose(train_data, principal_comps, 'ATT_FLAG')
decomposed_test_data = set_zero_mean_decompose(test_data, principal_comps, [])

# Plot of PCA residuals of training set.
pyplot.plot(decomposed_train_data[decomposed_train_data.columns][0:1000])
pyplot.show()

print('Generating outliers with the isolation forest model.')
# Notes regarding parameters:
#   - Contamination set to 0, as training data does not contain any attacks.
#   - max_samples set to all samples, as that provided more accurate results.
outlier_indices = generate_list_outliers(decomposed_train_data.values, decomposed_test_data.values, decomposed_test_data.index, IsolationForest(contamination=0, max_samples=8761))
print('Amount of outliers found: %i' % len(outlier_indices))
print('List of outliers:')
print(outlier_indices)
print('Generating outliers with the one-class SVM model.')
# Notes regarding parameters:
#   - Kernel set to sigmoid, seems to be the best option from several that we tried.
outlier_indices = generate_list_outliers(decomposed_train_data.values, decomposed_test_data.values, decomposed_test_data.index, OneClassSVM(kernel='sigmoid'))
print('Amount of outliers found: %i' % len(outlier_indices))
print('List of outliers:')
print(outlier_indices)

# pyplot.plot(decomposed_train_data[decomposed_train_data.columns][0:1000])
# pyplot.show()