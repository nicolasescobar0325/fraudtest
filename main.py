import os
import sys
import json
import pandas as pd
from datetime import datetime as dt

from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

ABS_DIR = os.path.dirname(__file__)
DEPLOYED_DIR = os.path.join(ABS_DIR, 'deployed')
SCRIPTS_DIR = os.path.join(ABS_DIR, 'scripts')

MODEL_CONFIG_FILE = os.path.join(DEPLOYED_DIR, 'config.json')

sys.path.insert(0, DEPLOYED_DIR)
sys.path.insert(0, SCRIPTS_DIR)

from predict_pipeline import online_prediction_pipeline


with open(MODEL_CONFIG_FILE,'r') as f:
    model_config = json.load(f)

app = Flask(__name__)
api = Api(app)

feature = 1

model_features = model_config['modelFeatures']
test_request = model_config['testRequest']['features']

class ModelPrediction(Resource):
    def post(self):
        request_dict = request.get_json(silent=True)   
        req_features = request_dict['features']
        #if request is not None  
        request_df = pd.DataFrame(columns=model_features)
        request_df = request_df.append(req_features, ignore_index=True)
        response = online_prediction_pipeline(request_df)

        return response


api.add_resource(ModelPrediction, '/predict')

if __name__ == '__main__':
    app.run(debug=True)