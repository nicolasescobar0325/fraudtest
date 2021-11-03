# Fraud detection ML model pipeline
Machine Learning model to predict fraud on Credit Card transactions dataset. The model was deployed with Flask on Google Cloud Platform as a docker build using the services Cloud Build and Cloud Run.

To call the model, you can send a POST request to the predict endpoint with the input features as a JSON payload.

## API params:
host='https://cont-rappi-1-y3a2lw3urq-uc.a.run.app'
endpoint='predict'

## API call example (Python):
You can make an API request using the following parameters (datailed example at api_call_sample.py).

features = {'ID_USER': 62,
     'genero': 'F',
     'monto': 426.0129785731381,
     'fecha': '2020-01-23',
     'hora': 2,
     'dispositivo': "{'model': 2020, 'device_score': 1, 'os': '%%'}",
     'establecimiento': 'Abarrotes',
     'ciudad': 'Monterrey',
     'tipo_tc': 'Virtual',
     'linea_tc': 84000,
     'interes_tc': 50,
     'status_txn': 'Aceptada',
     'is_prime': False,
     'dcto': 0.0,
     'cashback': 8.520259571462763} 

It should return the following parameters:
'prediction': 0.0207,
'predictionLabel': '0 - NoFraude' 