#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 22:48:03 2021

@author: pedrojose
"""
from enum import Enum


import os


class ColumnSelector:
    
    """Selects the columns that are numeric and categorical"""
    def __init__(self, data):
        self.data = data
        self.X = None
        self.y = None
        self.cat_cols = self.__find_categorical_columns()
        self.num_cols = self.__find_numerical_columns()
        
        
    def __find_categorical_columns(self):
      """Finds the numerical columns of the data"""  
      #find columns that are objects, that do have strings in it.
      
      str_cols = self.data.select_dtypes(include=['object']).columns.tolist()
      
      # create categorical columns array
      cat_cols = []
    
      # for every column that contains string values
      for col in str_cols:
        # select the colums where the length of unique elements are less than 30, more that should be just text, but not categorical or ordinal
        mask = len(self.data[col].unique()) <= 100

        if mask:
          cat_cols.append(col)
    
      return cat_cols
     
    
    def __find_numerical_columns(self):
        """Finds the numerical columns of the data"""
        num_cols = self.data.select_dtypes(include=['number']).columns.to_list()
        return num_cols
        
    def data(self):
        """Returns the data"""
        return self.data
        

    def select_modelling_data(self, pred_column):
        """Selects X and y"""
        #check if pred column is in the columns value
        
        
        if pred_column in self.data.columns.values:
            self.data.reset_index(drop=True, inplace=True)
            self.y = self.data[[pred_column]]
            
            self.X = self.data.drop([pred_column], axis=1)
        
    
    def modelling_columns(self, pred_column):
        """Return a list of categorical columns and numeric columns excluding y variable"""
        if pred_column in self.cat_cols:
            
            cat_cols = self.cat_cols(pred_column)
            num_cols = self.num_cols
          
        if pred_column in self.num_cols:
            num_cols = self.num_cols.remove(pred_column)
            cat_cols = self.cat_cols
        
        return self.num_cols , self.cat_cols 
        
    def modelling_data(self):
        """Returns the data to be used for predictions"""
        
        return self.X, self.y 
    