import pandas as pd 
import numpy as np
from datetime import datetime as dt

def numerical_cleaning(data, num_vars, config):
    try:
        df_numerical = pd.DataFrame()
        for num_var in num_vars:
            var_series = data[num_var]
            null_replace = config[num_var]['null_replace']
            var_series.replace(np.nan, null_replace, inplace=True)
            df_numerical[num_var] = var_series
        return df_numerical
    except:
        return pd.DataFrame()

def categorical_cleaning(data, cat_vars, config):
    try:
        df_categorical = pd.DataFrame()
        for cat_var in cat_vars:
            var_series = data[cat_var]
            null_replace = config[cat_var]['null_replace']
            var_series.replace(np.nan, null_replace, inplace=True)
            replace_dict = config[cat_var]['replace_dict']
            df_categorical[cat_var] = var_series.replace(replace_dict)
        return df_categorical
    except:
        return pd.DataFrame()

def boolean_cleaning(data, bool_vars, config):
    try:
        df_boolean = pd.DataFrame()
        for bool_var in bool_vars:
            var_series = data[bool_var]
            null_replace = config[bool_var]['null_replace']
            var_series.replace(np.nan, null_replace, inplace=True)
            df_boolean[bool_var] = var_series
        return df_boolean
    except:
        return pd.DataFrame()

if __name__=='__main__':
    pass