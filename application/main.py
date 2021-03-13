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

import Analysis as an
import Visualiser as vs

# Load the file
# This loading into a file should be the input data of the
# user from the website
airbnb_file_path = os.path.join('.', 'AB_NYC_2019.csv')

# Load data into dataframe
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
fig = visualiser.plot_boxplot(kind='box')

fig = visualiser.plot_histogram(figsize=(20, 15))