def select_data(df, keys, start_index, end_index):
    print(df)
    res = df
    res = res[keys]
    print(res)
    res = res[start_index:end_index]
    return res