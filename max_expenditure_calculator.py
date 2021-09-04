import pandas as pd
import numpy as np

PREDS_PATH = 'prediction_at_all.csv'


def calculate_max_expendature(year, percent):
    try:
        df = pd.read_csv(PREDS_PATH, index_col='Unnamed: 0')
    except:
        print(f'File Not found: {PREDS_PATH}')
        
    res = df.loc[df['year'] == year, 'value'].values
    #print(res)
    return {'actual': res, 'plus_percent': (1 + percent / 100) * res}