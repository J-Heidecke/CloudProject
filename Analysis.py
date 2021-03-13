#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 17:11:22 2021

@author: pedrojose
"""


#importing functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns


airbnb_file_path = os.path.join('.', 'AB_NYC_2019.csv')

df = pd.read_csv(airbnb_file_path)

class DataWrangler:
    
    def __init__(self, data, unnecesary_cols):
        self.data = data.copy()
        self.unnecesary_cols = unnecesary_cols

    def info(self):
        """Shows the info of the data"""
        self.data.info()
    
    def describe(self):
        """Decribes the statistics of the data"""
        return self.data.describe()
    
    def find_missing_ratio(self):
        """Finds the ratio of missing values for each column"""
        nullRatios = {}
        #for every value in the columns
        for val in list(self.data.columns.values):
            #find the sum of null values and the length of the column
            nullValuesCol = self.data[val].isnull().sum()
            totalCol = len(self.data[val])
    
            #find ratio of nulls compared to total column
            ratio = (nullValuesCol / totalCol) * 100
    
            #if there are nulls, add to nullRatios
            if ratio > 0:
                nullRatios[val] = ratio
    
        # print values to test
        for k, v in nullRatios.items():
            print('Column {key} has a ratio of {value}'.format(key = k, value = v))
            print(k)
    
        return nullRatios 

    def remove_missing(self, nullRatios, drop_col_ratio):
        # find mean of column skipping na
        meanv = self.data.mean(axis=1, skipna=True)
        col_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64', 'object']
        df_col_types = dict(self.data.dtypes)
        #percentage to fill or drop, if bigger the column is dropped
        minPercent = drop_col_ratio
    
        # for every key value pair 
        for k, v in nullRatios.items():
    
            print(k)
            # if the value of the ratio is larger than the min percentage drop the column
            if v > minPercent:
                self.data.drop(str(k), axis=1, inplace=True)
                #self.data.reset_index(drop=True, inplace=True)
                #print(df.columns.values)
                
            #if the type is np.object or string remove row missing
            elif df_col_types[str(k)] == np.object:
                self.data.dropna(how='any', axis=0, inplace=True)
                #self.data.reset_index(drop=True, inplace=True)
            #else fill na
            else:
                
                df.fillna(value={k: meanv}, axis=0, inplace=True)
     
    def remove_outliers(self, sd):
        """Removes the outliers above a given standard deviation"""
        #get the name of the columns
        col_names = self.data.columns.values
        #get the types of the columns
        df_col_types = dict(self.data.dtypes)
        
        #for every name and type, 
        for name, t in df_col_types.items():
            if t != np.object:
                name = str(name)
                #drop rows that values are sd times bigger than std
                drop_rows = self.data.index[(np.abs(self.data[name] - self.data[name].mean())
                              >= (sd * self.data[name].std()))]
                self.data.drop(drop_rows, axis=0, inplace=True)

    def remove_unnecesary_rows(self):
      """Removes unnecesary columns specified by """
    
      #for every column check if there are some of the most used by dataset, such as id
      self.data.drop(self.unnecesary_cols, axis=1, inplace=True)
      #self.data.reset_index(drop=True, inplace=True)
    def find_correlation(self, method='pearson'):
        return self.data.corr(method=method)
    
    def dtypes(self):
       return  self.data.dtypes
   
    def null_values_count(self):
        return self.data.isnull().sum()
    
    def dataset(self):
        return self.data