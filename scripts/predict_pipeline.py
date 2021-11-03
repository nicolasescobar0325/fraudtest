import os
import sys
import json 
import time 
import pandas as pd 
import numpy as np
import pickle as pkl
from datetime import datetime as dt


SCRIPTS_DIR = os.path.dirname(__file__)
PIPELINE_FUNC_DIR = os.path.join(SCRIPTS_DIR, 'pipeline_functions')
ABS_DIR = os.path.dirname(SCRIPTS_DIR)
DEPLOYED_DIR = os.path.join(ABS_DIR, 'deployed')
UTILS_DIR = os.path.join(SCRIPTS_DIR, 'utils')
TESTING_PATH = os.path.join(UTILS_DIR, 'testing')

sys.path.insert(0, DEPLOYED_DIR)
sys.path.insert(0, PIPELINE_FUNC_DIR)
sys.path.insert(0, UTILS_DIR)

from data_prepare import data_preparation_pipeline
from data_preprocess import data_preprocessing_pipeline

FEATURES_CONFIG_FILE = os.path.join(UTILS_DIR, 'features_config.json')
HISTORICAL_FILE = os.path.join(UTILS_DIR, 'ds_challenge_2021.csv')
DEPLOYED_MODEL = os.path.join(DEPLOYED_DIR, 'model.pkl')
historical_df = pd.read_csv(HISTORICAL_FILE, encoding='utf-8')

with open(DEPLOYED_MODEL,'rb') as f:
    deployed_model = pkl.load(f)

with open(FEATURES_CONFIG_FILE,'r') as f:
    features_config = json.load(f)


def online_prediction_pipeline(req_json, config_file=features_config, historical=historical_df, model=deployed_model):
    exec_time = dt.now().strftime("%m/%d/%Y %H:%M:%S")
    start_time = time.time()
    req_df = pd.DataFrame()
    req_df = req_df.append(req_json, ignore_index=True) if type(req_json) == dict else req_json
    data_prepared = data_preparation_pipeline(req_df, config_file, historical, is_training=False)
    data_preprocessed, _ = data_preprocessing_pipeline(data_prepared, config_file)
    prediction, prediction_label = model_predict(model, data_preprocessed, labels = {0:'0 - NoFraude', 1:'1 - Fraude'}, th=0.1)
    return {'prediction':prediction, 'predictionLabel':prediction_label, 'modelType': 'gb', 'predictionTime':round(time.time()-start_time,2), 'execTimestamp':exec_time}

def model_predict(model, to_predict_data, labels, th=0.5):
    prediction = round((model.predict_proba(to_predict_data)).squeeze()[1],4)
    prediction_label = labels[1 if prediction > th else 0]
    return prediction, prediction_label


if __name__=='__main__':

    kwargs = {'input_filepath':'None'}
    
    input_dict = dict([arg.split('=', maxsplit=1) for arg in sys.argv[1:]])

    kwargs.update(input_dict)

    try:
        with open(kwargs['input_filepath'], 'r') as f:
            input_json = json.load(f)
            
        output_path = os.path.join(TESTING_PATH, 'online_prediction_{}.json'.format(str(dt.now().strftime("%Y%m%d%H%M%S"))))
        prediction = online_prediction_pipeline(input_json)

        with open(output_path, 'w') as f:
            json.dump(prediction, f)
        
    except:
        print('No se pudo procesar el archivo {}'.format(kwargs['input_filepath']))