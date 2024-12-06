### Function to count null values in a df
def find_null_vals(df):
    return df.isnull().sum()

### Function to find shape of a df
def find_shape(df):
    return df.shape 

### Function to find info of a df
def find_info(df):
    return df.info()

### Function to find description of all columns of a df
def find_desc(df):
    if any(df.dtypes == 'object'):
        # Run describe for object columns
        return (df.describe(), df.describe(include='object'))
    else:
        return df.describe()

### Function to count duplicates in a df
def find_dup(df):
    return df.duplicated().sum()

