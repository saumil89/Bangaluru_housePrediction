from flask import Flask
import json
import pickle
import sklearn
import numpy as np
import pandas as pd

__locations = None
__col_data = None
__model = None

def get_locations():
    global __locations
    global __col_data

    with open('columns.json','r') as f:
        __col_data = json.load(f)['column']
        __locations = __col_data[3:]
    
    return __locations

def get_estimated_price(location,sqft,bhk,bath):
    global __model
    
    sqft = float(sqft)
    bhk = float(bhk)
    bath = float(bath)

    data = json.load(open('other.json'))
    
    sqft_mean = data['size'][0]
    sqft_std = data['size'][1]

    bed_mean = data['bed'][0]
    bed_std = data['bed'][1]

    bath_mean = data['bath'][0]
    bath_std = data['bath'][1]

    sqft = (sqft-sqft_mean)/sqft_std
    bhk = (bhk-bath_mean)/bath_std
    bath = (bath-bath_mean)/bath_std 

    if __model == None:
        with open('model','rb') as f:
            __model = pickle.load(f)
    try:
        loc_index = __col_data.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__col_data))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)*100000

if __name__ == '__main':
    get_locations()