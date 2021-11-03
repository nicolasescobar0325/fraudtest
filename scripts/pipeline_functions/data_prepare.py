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
HISTORICAL_FILE = os.path.join(UTILS_DIR, 'ds_challenge_2021.csv')
historical_df = pd.read_csv(HISTORICAL_FILE, encoding='utf-8')

with open(FEATURES_CONFIG_FILE,'r') as f:
    features_config = json.load(f)

from utils import read_dict_as_col, bin_to_bool
from enrich_utils import time_dep_features
from clean_utils import numerical_cleaning, categorical_cleaning, boolean_cleaning

def data_preparation_pipeline(df, config_file, historical, is_training=True):
    validated_data = data_validate(df)
    historical = data_transform(historical)
    transformed_data = historical if is_training else data_transform(validated_data)
    enriched_data = data_enrich(transformed_data, historical)
    cleaned_data = data_cleaning(enriched_data, config_file)
    return cleaned_data


def data_validate(df):
    return(df)


def data_transform(df):
    df[['disp_model', 'disp_device_score', 'disp_os']] = df['dispositivo'].apply(read_dict_as_col)
    df['minuto'] = df.apply(lambda x: np.random.randint(0, 59+1), axis=1)
    df['segundo'] = df.apply(lambda x: np.random.randint(0, 59+1), axis=1)
    df['timestamp'] = df['fecha'] + ' ' + df['hora'].astype(str).str.pad(width=2, side='left', fillchar='0') \
                            + ':' + df['minuto'].astype(str).str.pad(width=2, side='left', fillchar='0') \
                            + ':' + df['segundo'].astype(str).str.pad(width=2, side='left', fillchar='0')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df[['year','weekofyear','dayofweek']] = df['timestamp'].apply(lambda x: x.isocalendar()).to_list()
    df['valor_riesgo'] = df['monto'] - df['dcto']
    df['tc_fisica'] = bin_to_bool(df['tipo_tc'], classes=['Física', 'Virtual'])
    df['dcto_perc'] = (df['dcto']*100/df['monto']).round(0).astype(int)
    df['cashback_perc'] = (df['cashback']*100/df['monto']).round(1)
    return df


def data_enrich(df, historical):
    df[['num_hist_txn', 'num_hist_txn_fraud', 'avg_amount_txn', 'std_amount_txn', 'same_city_last', 'same_commerce_last', 'same_device_last', \
           'same_type_last', 'last_status_last', 'last_fraud_last', 'amount_diff_last', 'time_since_last']] = df.apply(lambda row: time_dep_features(row, historical), axis=1).to_list()
    return df

def data_cleaning(data, config=features_config):
    df_cleaned = pd.DataFrame()
    
    num_vars = list(config['numerical'].keys())
    cat_vars = list(config['categorical'].keys())
    bool_vars = list(config['boolean'].keys())
    target_var = list(config['target'].keys())
    
    num_vars_df = numerical_cleaning(data, num_vars, config['numerical'])
    cat_vars_df = categorical_cleaning(data, cat_vars, config['categorical'])
    bool_vars_df = boolean_cleaning(data, bool_vars, config['boolean'])
    target = boolean_cleaning(data, target_var, config['target'])
    
    df_cleaned = pd.concat([df_cleaned, num_vars_df, cat_vars_df,bool_vars_df, target], axis=1)
    return df_cleaned


if __name__=='__main__':

    kwargs = {'input_filepath':'None'}
    
    input_dict = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])

    kwargs.update(input_dict)

    try:
        input_df = pd.read_csv(kwargs['input_filepath'], encoding='utf-8')
        output_path = os.path.join(TESTING_PATH, 'transformed_data_{}.csv'.format(str(dt.now().strftime("%Y%m%d%H%M%S"))))
        transformed_df = data_preparation_pipeline(input_df, config_file=features_config, historical=historical_df)
        transformed_df.to_csv(output_path)
    except:
        print('No se pudo procesar el archivo {}'.format(kwargs['input_filepath']))