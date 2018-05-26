from assignment2.io import read_csv_adapted

key = 'F_PU2'

# Read data.
series = read_csv_adapted('data/BATADAL_train_dataset_1.csv')

# Select start and stop indices for a given data range.
# (Set end to 8762 and start to 0 for all).
start = 0
end = 8700