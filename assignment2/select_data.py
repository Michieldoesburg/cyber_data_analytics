def select_data(df, keys, start_index, end_index):
    res = df
    res = res[keys]
    res = res[start_index:end_index]
    return res