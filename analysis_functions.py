def find_null_vals(df):
    return df.isnull().sum()