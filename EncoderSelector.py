#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 22:52:13 2021

@author: pedrojose
"""

from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder

import sys

  
class EncoderSelector:
    
    """Selects the encoder used to encode categorical features"""
    def __init__(self):
        self.X_encoder = None
        self.y_encoder = None
        
    
    def select_reg_encoder(self, X):
        
        """Sets the encoding algorithm for X for regression tasks, 
        y encoder is OHE to do cross-validation. y must be a number to use this function"""
        self.X_encoder = OneHotEncoder()

    def select_cls_encoder(self, X, y):
        """Sets the encoding algorithm for X and y for classification tasks, 
        y encoder is ordinal to do cross-validation"""
        self.X_encoder = OneHotEncoder()
        self.y_encoder = OrdinalEncoder()
        
    def encoders(self):
        """Returns the current encoders, if y is not set None is returned"""
       
        return self.X_encoder, self.y_encoder

    