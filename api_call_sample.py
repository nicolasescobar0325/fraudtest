import requests
import json


local_host='http://127.0.0.1:5000/predict?'
host='https://cont-rappi-1-y3a2lw3urq-uc.a.run.app/predict?'

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

payload = {'features':features}


def api_call(host=host, payload=payload, i=1):
    try:
        req = requests.post(host, json=payload)
        return req.json(), 'Request took {} iterations'.format(i)    

    except:
        i+=1
        api_call(host, payload, i)

api_call(host, payload)