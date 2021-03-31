#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 20:06:39 2021

@author: pedrojose
"""
from abc import ABC, abstractmethod

from sklearn.model_selection import StratifiedKFold, KFold
import pandas as pd
import sys
#sys.path.append('./CrossValidator.py')
#import website.CrossValidator as CrossValidator


class CrossValidator(ABC):
    
    def __init__(self, X, y):
        self.X = X
        self.y = y
        
    @abstractmethod 
    def cross_validate(self, cv: CrossValidator): 
        pass
    
            
    
    def size(self):
        
        if (self.X.shape[0] and self.y.shape[0]) <= 10000:
            return  5
        else:
            return 10
    
    @abstractmethod
    def get_data(self):
            pass
        
class ClassificationCrossValidator(CrossValidator):
    
    def __init__(self, X, y):
        super(ClassificationCrossValidator, self).__init__(X, y)
        
        self.kfolds = self.size()
        self.kf = StratifiedKFold(n_splits=self.kfolds, shuffle=True, random_state=42)
        
    def cross_validate(self, cv: CrossValidator):
        if isinstance(cv, ClassificationCrossValidator):
            for train_index, test_index in self.kf.split(self.X, self.y):
                X_train, X_test = self.X.iloc[train_index], self.X.iloc[test_index] 
                y_train, y_test = self.y.iloc[train_index], self.y.iloc[test_index]
                
                
            return X_train, X_test, y_train, y_test
        else:
            return None
    
    def get_data(self):
        return self.X, self.y
    
class RegressionCrossValidator(CrossValidator):
    
    def __init__(self, X, y):
        super(RegressionCrossValidator, self).__init__(X, y)
        self.kfolds = super(RegressionCrossValidator, self).size()
        self.kf = KFold(n_splits=self.kfolds, shuffle=True, random_state=42)
        
    def cross_validate(self, cv:CrossValidator):
        if isinstance(cv, RegressionCrossValidator):
            for train_index, test_index in self.kf.split(self.X, self.y):
                X_train, X_test = self.X.iloc[train_index], self.X.iloc[test_index] 
                y_train, y_test = self.y.iloc[train_index], self.y.iloc[test_index]          
            
            
            return X_train, X_test, y_train, y_test
        
        else:
            return None
    
    def get_data(self):
        return self.X, self.y