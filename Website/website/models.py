#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 13:48:28 2021

@author: pedrojose
"""
from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression
from sklearn.svm import SVC, SVR
from sklearn.ensemble import BaggingClassifier, BaggingRegressor
from sklearn.multiclass import OneVsRestClassifier

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, confusion_matrix, accuracy_score, f1_score, recall_score, precision_score, roc_auc_score
from scipy.stats import uniform, loguniform, expon

import sys

from abc import ABC, abstractmethod

class Model:
    
    
    def __init__(self, X, y, n_iter, random_state, scoring):
        self.X = X 
        self.y = y
        self.n_jobs = -1
        self.scoring = scoring
        self.verbose = 2
        self.grid_search = None
        self.parameters = self.choose_parameters()
        self.n_iter = n_iter
        self.random_state = random_state
        
    def select(self):
        if self.size():
            self.grid_search = GridSearchCV(self.estimator, self.parameters,
                                          self.scoring, verbose=self.verbose, n_jobs=self.n_jobs)
        else:
            
           self.grid_search = RandomizedSearchCV(estimator=self.estimator, param_distributions=self.parameters, scoring=self.scoring,
                                                 verbose=self.verbose, n_iter=self.n_iter, random_state=self.random_state ,n_jobs=self.n_jobs)    
           
    def size(self):
        
        if (self.X.shape[0] and self.y.shape[0]) <= 10000:
            return  True
        else:
            return False
    
    @abstractmethod    
    def evaluate(self, y_true, y_pred): pass

    @abstractmethod
    def choose_parameters(self): pass

class RegressionModel(Model):
    
    def __init__(self, X, y, estimator, n_iter, random_state, scoring):
        
        super().__init__(X, y, n_iter, random_state, scoring)
        self.estimator = estimator
        
        
        super(RegressionModel, self).select()
       
        
        
    def evaluate(self, y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = mean_squared_error(y_true, y_pred, squared=False)
        r2 = r2_score(y_true, y_pred)
        
        return mae, mse, rmse, r2
    


        
    def best_score(self):
        return self.grid_search.best_score_
    
    def best_estimator(self):
        return self.grid_search.best_estimator_
    
    def fit(self, X, y):
        return self.grid_search.fit(X, y)
    
    def predict(self, X):
        predicted = self.grid_search.predict(X)
        return predicted
    
 
    @abstractmethod
    def choose_parameters(self): pass
        
            
           
## Regression models                

class LinearRegressionModel(RegressionModel):
    
    def __init__(self, X, y, n_iter=10, random_state=42, scoring=None):
        #self.parameters = self.choose_parameters()
        super(LinearRegressionModel, self).__init__(X, y, LinearRegression() , n_iter, random_state, scoring)
        
     

    def parameters(self):
        return self.parameters     

    def best_params(self):
        return self.grid_search.best_params_

    
    def gridsearch(self):
        return self.grid_search
   
    
    def choose_parameters(self):
       
        if self.size():
            params  = {'fit_intercept':[True,False], 'normalize':[True,False], 'copy_X':[True, False]}
           
        else:
            
            params = {'fit_intercept':[True,False], 'normalize':[True,False], 'copy_X':[True, False]}
    
        return params
    
class RidgeRegressionModel(RegressionModel):
    
    def __init__(self, X, y, n_iter=10, random_state=42, scoring=None):
        super(RidgeRegressionModel, self).__init__(X, y, Ridge(), n_iter, random_state, scoring)
        
        
    
   
    def parameters(self):
        return self.parameters
    
    def best_params(self):
        return self.grid_search.best_params_
    
    #def best_score(self):
    #    return self.grid_search.best_score_
    
    def gridsearch(self):
        return self.grid_search
    
    def choose_parameters(self):
       
        if self.size():
            params  = {'alpha':[1,0.1,0.01,0.001,0.0001,0], 'normalize':[True,False]}
           
        else:
            
            params = {'alpha':loguniform(1e-4, 1e0) , 'normalize':[True,False]}
    
        return params
 
class SVRModel(RegressionModel):
    
    def __init__(self, X, y, n_iter=10, random_state=42, scoring=None):
        super(SVRModel, self).__init__(X, y, SVR(), n_iter, random_state, scoring)
        

    
   
    def parameters(self):
        return self.parameters
    
    def best_params(self):
        return self.grid_search.best_params_
    
    #def best_score(self):
    #    return self.grid_search.best_score_
    
    def gridsearch(self):
        return self.grid_search
    
    def choose_parameters(self):
       
        if self.size():
            params  = {'C': [1, 10, 100, 1000],
                       'gamma': [0.0001, 0.001, 0.01, 0.1],
                       'kernel': ['rbf', 'linear', 'poly', 'sigmoid'], 'epsilon': [0.1,0.2,0.5,0.3]}

        else:
        
            params = {'C': loguniform(1e0, 1e3),
                      'gamma': loguniform(1e-4, 1e-1),
                      'kernel': ['rbf', 'linear', 'poly', 'sigmoid'], 'epsilon': uniform(0.1, 0.5) }
            
        return params
    
class BaggingSVRModel(RegressionModel):
    
    def __init__(self, X, y, n_estimators=10, n_iter=10, random_state=42, scoring=None):
        self.n_estimators = n_estimators
        super(BaggingSVRModel, self).__init__(X, y, BaggingRegressor(base_estimator=SVR(), n_estimators=self.n_estimators), n_iter, random_state, scoring)
       
        
    
   
    def parameters(self):
        return self.parameters
    
    def best_params(self):
        return self.grid_search.best_params_
    
   
    
    def gridsearch(self):
        return self.grid_search
    
    def choose_parameters(self):
       
        if self.size():
            params  = {'base_estimator__C': [1, 10, 100, 1000],
                       'base_estimator__gamma': [0.0001, 0.001, 0.01, 0.1],
                       'base_estimator__kernel': ['rbf', 'linear', 'poly', 'sigmoid'], 
                       'base_estimator__epsilon': [0.1,0.2,0.5,0.3]}

        else:
        
            params = {'base_estimator__C': loguniform(1e0, 1e3),
                      'base_estimator__gamma': loguniform(1e-4, 1e-1),
                      'base_estimator__kernel': ['rbf', 'linear', 'poly', 'sigmoid'], 
                      'base_estimator__epsilon': uniform(0.1, 0.5) }
            

            
        return params

## Classification models    
class ClassificationModel(Model):
    
    def __init__(self, X, y, estimator, n_iter, random_state, scoring):
        
        super().__init__(X, y, n_iter, random_state, scoring)
        self.estimator = estimator
        
        
        #model_LR= LinearRegression()
        super(ClassificationModel, self).select()

        
    
    def evaluate(self, y_true, y_pred):
        cm = confusion_matrix(y_true, y_pred)
        accuracy = accuracy_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred, average='weighted')
        precision = precision_score(y_true, y_pred, average='weighted')
        
        f1 = f1_score(y_true, y_pred, average='weighted')
        return cm, accuracy, recall, precision, f1
    

    
     
    def best_score(self):
        return self.grid_search.best_score_
    
    def best_estimator(self):
        return self.grid_search.best_estimator_
    
    def fit(self, X, y):
        return self.grid_search.fit(X, y)
    
    def predict(self, X):
        predicted = self.grid_search.predict(X)
        return predicted
    
    def predict_proba(self, X):
        predicted = self.grid_search.predict_proba(X)
        return predicted
 
    @abstractmethod
    def choose_parameters(self): pass



class SVCModel(ClassificationModel):
    
    def __init__(self, X, y, n_iter=10, random_state=42, scoring=None):
        super(SVCModel, self).__init__(X, y, OneVsRestClassifier(SVC()), n_iter, random_state, scoring)
        


   
    def parameters(self):
        return self.parameters
    
    def best_params(self):
        return self.grid_search.best_params_
    
    #def best_score(self):
    #    return self.grid_search.best_score_
    
    def gridsearch(self):
        return self.grid_search
    
    def choose_parameters(self):
        
        if self.size():
            params  = {'estimator__C': [1, 10, 100, 1000],
                       'estimator__gamma': [0.0001, 0.001, 0.01, 0.1],
                       'estimator__kernel': ['rbf', 'linear', 'poly', 'sigmoid']}

        else:
        
            params = {'estimator__C': loguniform(1e0, 1e3),
                      'estimator__gamma': loguniform(1e-4, 1e-1),
                      'estimator__kernel': ['rbf', 'linear', 'poly', 'sigmoid']}
             
        return params
    
class BaggingSVCModel(ClassificationModel):
    
    def __init__(self, X, y, n_estimators=10,n_iter=10, random_state=42, scoring=None):
        self.n_estimators = n_estimators
        super(BaggingSVCModel, self).__init__(X, y, BaggingClassifier(base_estimator=SVC(), n_estimators=self.n_estimators), n_iter, random_state, scoring)
        


   
    def parameters(self):
        return self.parameters
    
    def best_params(self):
        return self.grid_search.best_params_
    
    #def best_score(self):
    #    return self.grid_search.best_score_
    
    def gridsearch(self):
        return self.grid_search
    
    def choose_parameters(self):
        
        if self.size():
            params  = {'base_estimator__C': [1, 10, 100, 1000],
                       'base_estimator__gamma': [0.0001, 0.001, 0.01, 0.1],
                       'base_estimator__kernel': ['rbf', 'linear', 'poly', 'sigmoid']}

        else:
        
            params = {'base_estimator__C': loguniform(1e0, 1e3),
                      'base_estimator__gamma': loguniform(1e-4, 1e-1),
                      'base_estimator__kernel': ['rbf', 'linear', 'poly', 'sigmoid']}
             
        return params

class LogisticRegressionModel(ClassificationModel):
    
    def __init__(self, X, y, n_iter=10, random_state=42, scoring=None):
        super(LogisticRegressionModel, self).__init__(X, y, LogisticRegression(), n_iter, random_state, scoring)
       
   
    def parameters(self):
        return self.parameters
    
    def best_params(self):
        return self.grid_search.best_params_
    
    #def best_score(self):
    #    return self.grid_search.best_score_
    
    def gridsearch(self):
        return self.grid_search
    
    def choose_parameters(self):
        
        if self.size():
            params  = {'C': [1, 10, 100, 1000],
                       'penalty': ['l1', 'l2'],
                       'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']}

        else:
        
            params = {'C': loguniform(1e0, 1e3),
                      'penalty': ['l1', 'l2'],
                      'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']}
             
        return params