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
import _pickle as pk
from PIL import Image


import website.Analysis as an
import website.Visualiser as vs
import website.ColumnSelector as cs
import website.PredictorSelector as ps
import website.EncoderSelector as es
import website.DataTransformer as dt
import website.CrossValidator as cv
import website.models as m


class handler:
    def __init__(self, user_path, data_frame, file_name, ml_type, target):
        self.data_frame = data_frame
        self.ml_type = ml_type
        self.target = target
        self.file_name = file_name
        self.user_path = user_path
        self.results_path = os.path.join(user_path + '/results')
        f_name, f_ext = os.path.splitext(self.file_name) 
        self.query_path = os.path.join(self.results_path + '/'+ f_name)
        
    def analysis(self):
        if os.path.isdir(self.query_path) == False:
            os.mkdir(self.query_path)

        output = []
        output_metrics = []

        # create data wrangler object 
        data_wrangler = an.DataWrangler(self.data_frame, ['id', 'host_id'])

        null_ratio = data_wrangler.find_missing_ratio()
    
        # clean
        data_wrangler.remove_unnecesary_rows()
        data_wrangler.remove_missing(null_ratio, 20)
        data_wrangler.remove_outliers(1.7)

        # create visualiser object
        cleaned_data = data_wrangler.dataset()
        visualiser = vs.Visualiser(cleaned_data, self.query_path)

        #plot graphs
        fig_box = visualiser.plot_boxplot(kind='box')
        fig_hist = visualiser.plot_histogram(figsize=(20, 15))
        corr = data_wrangler.find_correlation()
        mask = corr > 0.20
        corr = corr[corr > 0.20]

        #create heatmap plot
        #sns_plot = visualiser.plot_heatmap(corr, annot=True)

        #set prediction type
        predictorType = self.ml_type #'classification' #self.ml_type 
        y_col = self.target #'room_type' #self.target

        columnSelector = cs.ColumnSelector(cleaned_data)

        columnSelector.select_processing_data(y_col)

        # select X and y columns but the X set has not been encoded or scaled
        X, y = columnSelector.modelling_data()

        #print(y.dtypes)
        # select the numeric and the categorical columns to use 
        num_cols, cat_cols = columnSelector.modelling_columns(y_col)

        # set encoder and predictor
        encoderSelector = es.EncoderSelector()
        predictorSelector = ps.PredictorSelector(columnSelector, encoderSelector, predictorType)

        predictorSelector.select_prediction_encoders()

        columnSelector.select_modelling_data(y_col)
        X, y = columnSelector.modelling_data()
        #y = y.values.reshape(-1, 1)

        if predictorType == 'regression':
            #regression
            X_encoder  = predictorSelector.X_encoder()
            #dataTransformer = dt.DataTransformer(X_encoder)
            data_transformer = dt.RegressorDataTransformer(X, X_encoder)
            data_transformer.process_pipeline(num_cols, cat_cols)
    
            X = data_transformer.X_pipeline()
            X = pd.DataFrame(X.toarray())
            cross_validator = cv.RegressionCrossValidator(X, y)
    
        elif predictorType == 'classification':
            X_encoder, y_encoder = predictorSelector.encoders()
            data_transformer = dt.ClassifierDataTransformer(X, y, X_encoder, y_encoder)
            data_transformer.process_pipeline(num_cols, cat_cols)
    
    
            X = data_transformer.X_pipeline()
            X = pd.DataFrame(X.toarray())
    
            y = data_transformer.y_pipeline()

            y = pd.Series(y)
            #print(y.shape)
            cross_validator = cv.ClassificationCrossValidator(X, y)


        X_train, X_test, y_train, y_test = cross_validator.cross_validate(cross_validator) 


        if predictorType == 'regression':
            # Linear Regression 
            lin_reg = m.LinearRegressionModel(X, y, n_iter=100)
    
            lin_reg.fit(X_train, y_train)
    
            y_pred_lin = lin_reg.predict(X_test)
    
            mae_lin, mse_lin, rmse_lin, r2_lin = lin_reg.evaluate(y_test, y_pred_lin)
            
            regression_dict = {'Mean Absolute Error': mae_lin,
                               'Mean Squared Error' : mse_lin,
                               'Mean Square Error' : rmse_lin,
                               'R2' : r2_lin
                               }
            
            output_metrics.append(regression_dict)
            output.append({'Linear Regression': y_pred_lin})
            
            # Ridge Regression
            ridge_reg = m.RidgeRegressionModel(X, y, n_iter=100)
    
            ridge_reg.fit(X_train, y_train)
    
            y_pred_ridge = ridge_reg.predict(X_test)
    
            mae_ridge, mse_ridge, rmse_ridge, r2_ridge = ridge_reg.evaluate(y_test, y_pred_ridge)
            
            regression_dict = {'Mean Absolute Error': mae_ridge,
                               'Mean Squared Error' : mse_ridge,
                               'Mean Square Error' : rmse_ridge,
                               'R2' : r2_ridge
                               }
            
            output_metrics.append(regression_dict)
            output.append({'Ridge Regression' : y_pred_ridge})
    
            # Support Vector Regressor
            #svr commented out as takes long 
            #svr = m.SVRModel(X, y, n_iter=20)

            #svr.fit(X_train, y_train)

            #y_pred_svr = svr.predict(X_test)
    
            #mae_svr, mse_svr, rmse_svr, r2_svr = svr.evaluate(y_test, y_pred_svr)
    
            bagging_svr = m.BaggingSVRModel(X, y, n_estimators=5, n_iter=20)
    
            bagging_svr.fit(X_train, y_train)
    
            y_pred_svr = bagging_svr.predict(X_test)
    
            mae_bag_svr, mse_bag_svr, rmse_bag_svr, r2_bag_svr = bagging_svr.evaluate(y_test, y_pred_svr)
            
            
            regression_dict = {'Mean Absolute Error': mae_bag_svr,
                               'Mean Squared Error' : mse_bag_svr,
                               'Mean Square Error' : rmse_bag_svr,
                               'R2' : r2_bag_svr
                               }
            
            output_metrics.append(regression_dict)
            output.append({'Bagging SVR' : y_pred_svr})
    
        elif predictorType == 'classification':
   
            #Logistic Regression
            log_reg = m.LogisticRegressionModel(X, y, n_iter=10)

            log_reg.fit(X_train, y_train)
    
            y_pred_logit = log_reg.predict(X_test)
    
            cm_logit, accuracy_logit, recall_logit, precision_logit, f1_logit = log_reg.evaluate(y_test, y_pred_logit)
            
            classification_dict = {'Confusion Matrix': cm_logit,
                               'Accuracy' : accuracy_logit,
                               'Recall' : recall_logit,
                               'Precission' : precision_logit,
                               'F1' : f1_logit 
                               }
            
            
            output_metrics.append(classification_dict)
            output.append({'Logistic Regression' : y_pred_logit})
            #svc commented out as takes long 
            #svc = m.SVCModel(X, y, n_iter=5)

            #svc.fit(X_train, y_train)
    
            #y_pred_svc = svc.predict(X_test)
    
            #cm_svc, accuracy_svc, recall_svc, precision_svc, f1_svc = svc.evaluate(y_test, y_pred_svc)
    
            #bagging svc commented out as takes long, but much less than using svc
            #bagging_svc = m.BaggingSVCModel(X, y, n_estimators=1, n_iter=10)
    
            #bagging_svc.fit(X_train, y_train)
    
            #y_pred_bag_svc = bagging_svc.predict(X_test)
    
            #cm_bag_svc, accuracy_bag_svc, recall_bag_svc, precision_bag_svc, f1_bag_svc = bagging_svc.evaluate(y_test, y_pred_bag_svc)
            
        return output, output_metrics

    def save_data(self):
        output, output_metrics = self.analysis()

        output_path = os.path.join(self.query_path + '/' + 'metrics.ob')
        with open(output_path, 'wb') as fp:
            pk.dump(output_metrics, fp)
