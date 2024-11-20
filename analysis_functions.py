def find_null_vals(df):
    return df.isnull().sum()

def find_shape(df):
    return df.shape 

def find_info(df):
    return df.info()

def find_desc(df):
    if any(df.dtypes == 'object'):
        # Run describe for object columns
        print(df.describe()) 
        print(df.describe(include='object'))
    else:
        print(df.describe())

def find_dup(df):
    return df.duplicated().sum()

