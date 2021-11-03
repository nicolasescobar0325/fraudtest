import ast
import pandas as pd

def read_dict_as_col(var_series):
    col_dict = ast.literal_eval(var_series)
    col_dict_keys = list(col_dict.keys())
    #var_series_separated = pd.Series()
    return pd.Series([col_dict[i] for i in col_dict_keys])

def bin_to_bool(var_series, classes):
    replace_dict = {classes[0]:True, classes[1]:False}
    return var_series.replace(replace_dict)

def acc(true_pos, true_neg, total_obs):
    try:
        return round((true_pos+true_neg)*100/total_obs,2)
    except:
        return 0

def recall(true_pos, false_neg):
    try:
        return round(true_pos*100/(true_pos+false_neg),2)
    except:
        return 0

def precision(true_pos, false_pos):
    try:
        return round(true_pos*100/(true_pos+false_pos),2)
    except:
        return 0
    
def fbeta_score(recall, precision, beta=1):
    try:
        return round((1+beta**2)*((precision*recall)/((precision*(beta**2))+recall)),2)
    except:
        return 0

if __name__=='__main__':
    pass