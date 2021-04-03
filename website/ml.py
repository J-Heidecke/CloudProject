#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import os
import _pickle as pk

# Statistics for Analysis

# Confusion Matrix
def confusionMatrix(pred, test):
    mat = sklearn.metrics.confusion_matrix(pred, test)
    sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False)
    plt.xlabel('true label')
    plt.ylabel('predicted label');

# Accuracy
def accuracy(pred, test):
    return sklearn.metrics.accuracy_score(test, pred)

# Mean of test set
def mean(test):
    return np.mean(test)

# Mean Root Squared
def mrs(pred, test):
    return np.sqrt(metrics.mean_squared_error(test, pred))

# Accuracy + Confusion Matrix + Mean + MRS
def combined(pred, test):
    accuracy(pred,test)
    confusionMatrix(pred, test)
    mrs(pred, test) 

# Kfold training + results 
class crossValidation:

    def __init__(self, algorithm, X, y):

        self.algorithm = algorithm
        self.X = X 
        self.y = y

    # Splits and trains the dataset
    def train(self, k):
        self.k = k

        #Scale data - normalize data
        sc = StandardScaler()
        # Decides number of splits according to specified number by user
        kf = KFold(self.k)
        output = []

        for train_index, validate_index in kf.split(self.X, self.y):
            # Training data
            Xt = self.X[train_index]
            sc.fit(Xt)
            X_train_std = sc.transform(Xt)
            X_test_std = sc.transform(self.X[validate_index])
            # Fit model to data
            self.algorithm.fit(X_train_std, self.y[train_index])
            # Get validation labels
            y_test = (self.y[validate_index])
            # Get predicted labels
            y_pred = (self.algorithm.predict(X_test_std))
            # Creating a list of predictions and validation labels for later use
            output.append(y_pred)
            output.append(y_test)

        return output

    #Performs statistics on the model
    def stats(self, k):
        pred = self.train(k)
        # See 'combined' function
        return combined(pred[0], pred[1])

    #Evalates the effect of different fold sizes and gives the mean of all folds.
    def evaluateK(self, k):
        result = []
        # Runs from 2 (minimum available amount) to a specified number (fold sizes) by user
        for i in range(2, k):
            #Calls train method
            pred = self.train(i)
            result.append(accuracy_score(pred[0], pred[1]))

        return result

class handler:
    def __init__(self, data_frame, file_name, ml_type, target, user_path):
        self.data_frame = data_frame
        self.ml_type = ml_type
        self.target = target
        self.file_name = file_name
        self.user_path = user_path

    def data_wrangler(self):

        #if self.ml_type == 'classification':
            result = []

            for x in self.data_frame.columns:
                if x != self.target:
                    result.append(x)

            X = self.data_frame[result].values
            y = self.data_frame[self.target].values
            del self.data_frame
            return X, y

    def analysis(self):
        X, y = self.data_wrangler()
        output = []

        if self.ml_type == 'classification':
            model_list = [DecisionTreeClassifier(criterion = 'entropy'),KNeighborsClassifier(),
                        RandomForestClassifier(n_estimators=10,criterion="entropy")]
            for model in model_list:

                name = str(model).split('(')
                name_dict = {}
                model_output = []
                results = crossValidation(model, X, y)
                np.max(results.evaluateK(20))
                name_dict[name[0]] = np.max(results.evaluateK(20))
                output.append(name_dict)

            return output

        elif self.ml_type == 'regression':
            model_list = [
                ('Linear Regression', LinearRegression()),
                ('Lasso', Lasso()),
                ('Ridge', Ridge()),
                ('DecisionTreeRegressor', DecisionTreeRegressor())]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)

            for model_name, model in model_list:

                name_dict = {}
                model.fit(X_train, y_train)
                name_dict[model_name] = model.score(X_test, y_test)
                output.append(name_dict)

            return output

    def save_data(self):
        output = self.analysis()
        results_path = os.path.join(self.user_path, 'results')
        if os.path.isdir(results_path) == False:
            os.mkdir(results_path)
        query_path = os.path.join(results_path, self.file_name)
        if os.path.isdir(query_path) == False:
            os.mkdir(query_path)
        f_name = self.file_name + 'metrics.ob'
        output_path = os.path.join(query_path, f_name)
        with open(output_path, 'wb') as fp:
            pk.dump(output, fp)