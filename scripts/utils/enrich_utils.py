import pandas as pd 
import numpy as np
from datetime import datetime as dt

def last_trx_comparison(actual_trx, last_trx):
    same_city = actual_trx['ciudad'] == last_trx['ciudad']
    same_commerce = actual_trx['establecimiento'] == last_trx['establecimiento']
    same_device = actual_trx['disp_os'] == last_trx['disp_os']
    same_type = actual_trx['tipo_tc'] == last_trx['tipo_tc']
    last_status = last_trx['status_txn']
    last_fraud = last_trx['fraude']
    amount_diff = actual_trx['monto'] - last_trx['monto']
    time_since = (actual_trx['timestamp'] - last_trx['timestamp']).total_seconds()
    return same_city, same_commerce, same_device, same_type, last_status, last_fraud, amount_diff, time_since

def price_behavior(hist, num_txn):
    avg_amount = round(hist['monto'].mean(),2) if num_txn > 0 else 0
    std_amount = round(hist['monto'].std(),2) if num_txn > 1 else 0
    return avg_amount, std_amount

def time_dep_features(row, hist_data):
    historical_trx = hist_data[(hist_data['timestamp'] < row['timestamp']) & (hist_data['ID_USER'] == row['ID_USER'])]
    num_hist_txn = historical_trx.shape[0]
    num_hist_txn_fraud = historical_trx[historical_trx['fraude']==True].shape[0]
    avg_amount_txn, std_amount_txn = price_behavior(historical_trx, num_hist_txn)
    same_city_last, same_commerce_last, same_device_last, same_type_last, last_status_last, last_fraud_last, amount_diff_last, time_since_last = \
                last_trx_comparison(row, historical_trx.sort_values(by='timestamp', ascending=False).iloc[0]) if num_hist_txn > 0 else (np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan)
    return num_hist_txn, num_hist_txn_fraud, avg_amount_txn, std_amount_txn, same_city_last, same_commerce_last, same_device_last, same_type_last, last_status_last, last_fraud_last, amount_diff_last, time_since_last

if __name__=='__main__':
    pass
