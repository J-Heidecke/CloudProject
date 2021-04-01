# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 18:29:07 2021

@author: heide
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

import sys
sys.path.append('./Analysis.py')
sys.path.append('./Visualiser.py')
sys.path.append('./ColumnSelector.py')
sys.path.append('./PredictorSelector.py')
sys.path.append('./EncoderSelector.py')
sys.path.append('./DataTransformer.py')

import Analysis as an

## Load the file
airbnb_file_path = os.path.join('.', 'AB_NYC_2019.csv')

df = pd.read_csv(airbnb_file_path)

# create data wrangler object 
data_wrangler = an.DataWrangler(df, ['id', 'host_id'])

#find info about columns
data_wrangler.info()

data_description = data_wrangler.describe()

data_types = data_wrangler.dtypes()

#get null ratio of data
null_ratio = data_wrangler.find_missing_ratio()

  

# clean
data_wrangler.remove_unnecesary_rows()
data_wrangler.remove_missing(null_ratio, 20)
data_wrangler.remove_outliers(1.7)

cleaned_data = data_wrangler.dataset()

columns = cleaned_data.columns
geographical_data = {}

for i in range(len(columns)):
    if 'name' in columns[i]:
        del cleaned_data[columns[i]]
        columns.drop(columns[i])
    elif 'longitude' in columns[i]  or 'long' in columns[i]:
        geographical_data['longitude'] = cleaned_data[columns[i]]
        columns.drop(columns[i])
    elif 'latitude' in columns[i] or 'lat' in columns[i]:
        geographical_data['latitude'] = cleaned_data[columns[i]]
        columns.drop(columns[i])

print(cleaned_data)

plt.hist(cleaned_data[columns[3]], bars=100)