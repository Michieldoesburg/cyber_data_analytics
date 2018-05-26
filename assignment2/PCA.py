from assignment2.io import read_csv_adapted
import pandas as pd

key = 'F_PU2'

def set_to_zero_mean(df):
    data = []
    index = df.index
    mean = df.mean(axis=0).values
    columns = df.columns
    for row in df.iterrows():
        r = row[1].values - mean
        data.append(r)
    res = pd.DataFrame(index=index, data=data, columns=columns)

# Read data.
series = read_csv_adapted('data/BATADAL_train_dataset_1.csv')

# Select start and stop indices for a given data range.
# (Set end to 8762 and start to 0 for all).
start = 0
end = 8700

set_to_zero_mean(series)