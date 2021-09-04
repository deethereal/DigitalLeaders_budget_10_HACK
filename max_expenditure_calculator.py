import pandas as pd
import numpy as np

PREDS_PATH = 'prediction_at_all.csv'

def print_big_digit(digit_with_e_and_some_other_shit):
    millions = round(digit_with_e_and_some_other_shit / 1e6, 3)

    millions = str(millions)
    dot_indx = millions.find('.')
    
    return millions[:dot_indx - 3] + ', ' + millions[dot_indx - 3:]


def calculate_max_expendature(year, percent):
    try:
        df = pd.read_csv(PREDS_PATH, index_col='Unnamed: 0')
    except:
        print(f'File Not found: {PREDS_PATH}')
        
    res = df.loc[df['year'] == year, 'value'].values
    print(res)
    return {'actual': print_big_digit(res), 
            'plus_percent': print_big_digit((1 + percent / 100) * res)}