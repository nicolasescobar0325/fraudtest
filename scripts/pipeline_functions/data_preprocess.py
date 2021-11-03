import os
import sys
import json 
import pandas as pd 
import numpy as np
from datetime import datetime as dt

PIPELINE_FUNC_DIR = os.path.dirname(__file__)
SCRIPTS_DIR = os.path.dirname(PIPELINE_FUNC_DIR)
ABS_DIR = os.path.dirname(SCRIPTS_DIR)
DEPLOYED_DIR = os.path.join(ABS_DIR, 'deployed')
UTILS_DIR = os.path.join(SCRIPTS_DIR, 'utils')
TESTING_PATH = os.path.join(UTILS_DIR, 'testing')

sys.path.insert(0, DEPLOYED_DIR)
sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, UTILS_DIR)

FEATURES_CONFIG_FILE = os.path.join(UTILS_DIR, 'features_config.json')

with open(FEATURES_CONFIG_FILE,'r') as f:
    features_config = json.load(f)


def data_preprocessing_pipeline(data, config_file=features_config):
    df_preprocessed = pd.DataFrame()
    
    num_vars = list(config_file['numerical'].keys())
    cat_vars = list(config_file['categorical'].keys())
    bool_vars = list(config_file['boolean'].keys())
    target_var = list(config_file['target'].keys())
    
    num_vars_df = numerical_preprocess(data, num_vars, config_file['numerical'])
    cat_vars_df = categorical_preprocess(data, cat_vars, config_file['categorical'])
    bool_vars_df = boolean_preprocess(data, bool_vars, config_file['boolean'])
    target = boolean_preprocess(data, target_var, config_file['target'])
    
    df_preprocessed = pd.concat([df_preprocessed, num_vars_df, cat_vars_df, bool_vars_df], axis=1)
    return df_preprocessed, target

def numerical_preprocess(df, num_vars, config):
    try:
        df_numerical = pd.DataFrame()
        for num_var in num_vars:
            var_series = df[num_var]
            df_numerical[num_var] = var_series
        return df_numerical
    except:
        return pd.DataFrame()

def categorical_preprocess(data, cat_vars, config):
    try:
        df_categorical = pd.DataFrame()
        for cat_var in cat_vars:
            var_config = config[cat_var]
            var_categories = var_config['categories']
            var_series = data[cat_var]
            df_categorical = pd.concat([df_categorical, pd.get_dummies(data[cat_var].astype(pd.CategoricalDtype(categories=var_categories)) \
                ,drop_first=True)], axis=1)
        return df_categorical
    except:
        return pd.DataFrame()

def boolean_preprocess(data, bool_vars, config):
    try:
        boolean_replace = {True:1, False:0}
        df_boolean = pd.DataFrame()
        for bool_var in bool_vars:
            var_series = data[bool_var]
            df_boolean[bool_var] = var_series.replace(boolean_replace)
        return df_boolean
    except:
        return pd.DataFrame()



if __name__=='__main__':

    kwargs = {'input_filepath':'None'}
    
    input_dict = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])

    kwargs.update(input_dict)

    try:
        input_df = pd.read_csv(kwargs['input_filepath'], encoding='utf-8')
        output_path = os.path.join(TESTING_PATH, 'preprocessed_data_{}.csv'.format(str(dt.now().strftime("%Y%m%d%H%M%S"))))
        transformed_df, _ = data_preprocessing_pipeline(input_df, config_file=features_config)
        transformed_df.to_csv(output_path)
        
    except:
        print('No se pudo procesar el archivo {}'.format(kwargs['input_filepath']))