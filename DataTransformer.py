#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 13:16:33 2021

@author: pedrojose
"""
import sys
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
sys.path.append('./ColumnSelector.py')
sys.path.append('./PredictorSelector.py')

import ColumnSelector
import PredictorSelector

class DataTransformer:
    
    def __init__(self, encoder):
        
        self.scaler = StandardScaler()
        self.encoder = encoder

        self.num_pipeline = None
        self.prepared_data = None
        self.full_pipeline = None
    #def encode(self):
        
    def __encode(self, num_cols, cat_cols):
        """Performs the data transformer"""
        
        self.full_pipeline = ColumnTransformer([
            ('num', self.num_pipeline, num_cols),
            ('cat', self.encoder, cat_cols)
            ])
    
    def __scale(self):
        """Scales the data of the columns"""
        self.num_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('std_scaler', self.scaler)
            ])
        
    def process_pipeline(self, X, num_cols, cat_cols):
        
       self.__scale()
       self.__encode(num_cols, cat_cols)
       self.full_pipeline = self.full_pipeline.fit_transform(X)
    
    
    def pipeline(self):
        if self.full_pipeline is not None:
            return self.full_pipeline
        
    def num_pipeline(self):
        if self.num_pipeline is not None:
            return self.num_pipeline
