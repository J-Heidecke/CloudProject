#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 17:36:53 2021

@author: pedrojose
"""

#importing functions
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
import Visualiser as vs
import ColumnSelector as cs
import PredictorSelector as ps
import EncoderSelector as es
import DataTransformer as dt
from enum import Enum

## Load the file
airbnb_file_path = os.path.join('.', 'AB_NYC_2019.csv')

df = pd.read_csv(airbnb_file_path)

# create data wrangler object 
data_wrangler = an.DataWrangler(df, ['id', 'host_id'])


#find info about columns
data_wrangler.info()

data_description = data_wrangler.describe()
print(data_description)


data_types = data_wrangler.dtypes()
print(data_types)

#get null ratio of data
null_ratio = data_wrangler.find_missing_ratio()

print(null_ratio)    

# clean
data_wrangler.remove_unnecesary_rows()
data_wrangler.remove_missing(null_ratio, 20)
data_wrangler.remove_outliers(1.7)

#check there are no nulls 
count_nulls = data_wrangler.null_values_count()
print(count_nulls)

# create visualiser object
cleaned_data = data_wrangler.dataset()
visualiser = vs.Visualiser(cleaned_data)


#plot graphs
fig_box = visualiser.plot_boxplot(kind='box')

fig_hist = visualiser.plot_histogram(figsize=(20, 15))

corr = data_wrangler.find_correlation()
mask = corr > 0.20
corr = corr[corr > 0.20]

#create heatmap plot
sns_plot = visualiser.plot_heatmap(corr, annot=True)



#set prediction type
predictorType =  'regression' #'classification'#
y_col = 'price'

columnSelector = cs.ColumnSelector(cleaned_data)
#columnSelector.find_columns()
columnSelector.select_modelling_data(y_col)

# select X and y columns but the X set has not been encoded or scaled
X, y = columnSelector.modelling_data()

# select the numeric and the categorical columns to use 
num_cols, cat_cols = columnSelector.modelling_columns(y_col)

print(X.head(), y.head())
print(num_cols)
print(cat_cols)
print(X.columns.values)
print(y.head())
# set encoder and predictor
encoderSelector = es.EncoderSelector()


predictorSelector = ps.PredictorSelector(columnSelector, encoderSelector, predictorType)


print(X.shape, y.shape)

predictorSelector.select_prediction_encoders()

X_encoder  = predictorSelector.X_encoder()


dataTransformer = dt.DataTransformer(X_encoder)

dataTransformer.process_pipeline(X, num_cols, cat_cols)

X = dataTransformer.pipeline()
X = pd.DataFrame(X.toarray())
#X = X.todense()
from sklearn.linear_model import LinearRegression

#lin_reg = LinearRegression()
#lin_reg.fit(data_prepared, y)
