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
#sys.path.append('./ColumnSelector.py')
#sys.path.append('./PredictorSelector.py')
from abc import ABC, abstractmethod
import website.ColumnSelector as ColumnSelector
import website.PredictorSelector as PredictorSelector


class DataTransformer(ABC):
   
    def __init__(self, X,  X_encoder, y_encoder=None):
        
        self.X = X
        self.scaler = StandardScaler()
        self.X_encoder = X_encoder
        self.y_encoder = y_encoder
        self.num_pipeline = None
        self.prepared_data = None
        self.full_pipeline = None
        
    #def encode(self):
    
    @abstractmethod    
    def encode(self, num_cols, cat_cols): pass
        
    
    @abstractmethod
    def scale(self): pass
        
    @abstractmethod    
    def process_pipeline(self, num_cols, cat_cols): pass
    
    
    def X_pipeline(self):
        if self.full_pipeline is not None:
            return self.full_pipeline
        
    def num_pipeline(self):
        if self.num_pipeline is not None:
            return self.num_pipeline
       
    
class RegressorDataTransformer(DataTransformer):
    
    def __init__(self, X, X_encoder):
        super(RegressorDataTransformer, self).__init__(X, X_encoder)
        
    def encode(self, num_cols, cat_cols):
        """Performs the data transformer"""
        
        self.full_pipeline = ColumnTransformer([
            ('num', self.num_pipeline, num_cols),
            ('cat', self.X_encoder, cat_cols)
            ])
    
    
    def scale(self):
        """Scales the data of the columns"""
        self.num_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('std_scaler', self.scaler)
            ])
    
    def process_pipeline(self, num_cols, cat_cols):
       
       self.scale()
       self.encode(num_cols, cat_cols)
       self.full_pipeline = self.full_pipeline.fit_transform(self.X)
       
class ClassifierDataTransformer(DataTransformer):

    def __init__(self, X, y, X_encoder, y_encoder):
        super(ClassifierDataTransformer, self).__init__(X, X_encoder, y_encoder)
        #self.y_encoder = y_encoder
        
        self.y = y
        self.label_pipeline = None
        
    def encode(self, num_cols, cat_cols):
        """Performs the data transformer"""
        
        self.label_pipeline = self.y_encoder
        
        self.full_pipeline = ColumnTransformer([
            ('num', self.num_pipeline, num_cols),
            ('cat', self.X_encoder, cat_cols)
            ])
    
        
        
    #def encode(self):
    #    self.label_pipeline = ColumnTransformer([
    #        ('label', self.y_encoder, y)
    #       ])

    def scale(self):
        """Scales the data of the columns"""
        self.num_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('std_scaler', self.scaler)
            ])
        
    def process_pipeline(self, num_cols, cat_cols):
       
       self.scale()
       self.encode(num_cols, cat_cols)
       self.full_pipeline = self.full_pipeline.fit_transform(self.X)    
       self.label_pipeline = self.label_pipeline.fit_transform(self.y)
       
    #def process_y_pipeline(self, y):
    #    self.encode_y(y)
    #    self.label_pipeline = self.label_pipeline.fit_transform(y=y)
        
    def y_pipeline(self):
        if self.label_pipeline is not None:
            return self.label_pipeline
        
    def categories(self):
        return self.y_encoder.classes_