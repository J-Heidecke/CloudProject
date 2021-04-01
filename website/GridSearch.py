#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 11:43:30 2021

@author: pedrojose
"""
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from abc import ABC, abstractmethod


class AbstractGridSearch:
    """Abstract class that selects the type of gridsearch to use based on the length of the dataset,
    The select method must be implemented by subclasses and selects the type of gridsearch"""
    def __init__(self, X, y, scoring, n_jobs, verbose):
        self.X = X 
        self.y = y
        self.n_jobs = n_jobs
        self.scoring = scoring
        self.verbose = verbose
   
    def select(self):
        if self.size():
            return GridSearchCV(self.estimator, self.parameters,
                                          self.scoring, verbose=self.verbose, n_jobs=self.n_jobs)
        else:
            
           return RandomizedSearchCV(self.estimator, self.parameters, 
                                                 self.scoring, verbose=self.verbose, n_iter=self.n_ter, n_jobs=self.n_jobs)    
   
    def size(self):
        
        if (self.X.shape[0] and self.y.shape[0]) <= 10000:
            return  True
        else:
            return False
             
class GridSearchSelector(AbstractGridSearch):
    """Selects the type of gridsearch"""
    def __init__(self, X, y, estimator, parameters, n_iter=10, scoring=None, n_jobs=-1, verbose=2):
        super(GridSearchSelector, self).__init__(X, y, scoring, n_jobs, verbose)
        self.estimator = estimator
        self.parameters = parameters
        self.n_ter = n_iter
        
        
    def select(self):
        if self.size():
            return GridSearchCV(self.estimator, self.parameters,
                                          self.scoring, verbose=self.verbose, n_jobs=self.n_jobs)
        else:
            
           return RandomizedSearchCV(estimator=self.estimator, param_distributions=self.parameters, 
                                                 self.scoring, verbose=self.verbose, n_iter=self.n_ter, n_jobs=self.n_jobs)
         
  
   
    def parameters(self):
       return self.parameters
   
 
  