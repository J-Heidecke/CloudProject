#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 13:19:32 2021

@author: pedrojose
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import sys
sys.path.append('./ColumnSelector.py')
sys.path.append('./EncoderSelector.py')
sys.path.append('./types.py')

import ColumnSelector
import EncoderSelector


    
class PredictorSelector:
    
    """Selects the type of prediction properties to be used in categorical data based on the prediction type, 
    such as classification or regression"""
    def __init__(self, columnSelector: ColumnSelector, encoderSelector: EncoderSelector, predictionType: str):
        self.columnSelector = columnSelector
        self.predictionType = predictionType
        self.encoderSelector = encoderSelector
        
    def predictionType(self):
        return self.predictionType

    
    def X_encoder(self):
        """Returns the encoder to encode X variables"""
        X_enc, _ = self.encoderSelector.encoders()
        return X_enc
    
    def y_encoder(self):
         _, y_enc = self.encoderSelector.encoders()
         return y_enc
    
    def encoders(self):
        """Returns the current encoders, if y is not set None is returned"""
        
        X_encoder, y_encoder = self.encoderSelector.encoders()
        return X_encoder, y_encoder
    
    def select_prediction_encoders(self):
      """selects encoder based on the type of prediction,"""
      # select the predicting column or label and the X
      #self.columnSelector.select_modelling_data(pred_column)
      predictionType = self.predictionType.lower()
      # get the selected
      X, y = self.columnSelector.modelling_data()
     
      #encode only X if it is regression as y is a number
      if predictionType == 'regression':
          self.encoderSelector.select_reg_encoder(X)
          
      #encode X and y if it is classification    
      elif predictionType == 'classification':
          self.encoderSelector.select_cls_encoder(X, y)
      
    
   
      
    

  
          
    
    
