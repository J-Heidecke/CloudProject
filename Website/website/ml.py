#!/usr/bin/env python
# coding: utf-8

# In[124]:


import numpy as np
import pandas as pd
import sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron
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

# In[125]:


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
    def __init__(self, data_frame, file_name, ml_type, target, results_path):
        self.data_frame = data_frame
        self.ml_type = ml_type
        self.target = target
        self.file_name = file_name
        self.results_path = results_path

    def data_wrangler(self):
        if self.ml_type == 'classification':
            result = []

            for x in self.data_frame.columns:
                if x != self.target:
                    result.append(x)
                
            X = self.data_frame[result].values
            y = self.data_frame[self.target].values
            del self.data_frame
            del self.ml_type
            return X, y
    
        elif self.my_type == 'regression':
            del self.data_frame
            del self.ml_type

    def analysis(self):
        X, y = self.data_wrangler()
        output = []
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

    def save_data(self):
        output = self.analysis()
        f_name = self.file_name + 'metrics.ob'
        output_path = os.path.join( self.results_path, f_name)
        with open(output_path, 'wb') as fp:
            pk.dump(output, fp)


#df = pd.read_csv("../../Data/heart.csv", na_values=['NA', '?'])
#df = df.reindex(np.random.permutation(df.index))
#data_handler = handler(df, 'pic', 'classification', 'target')
#outcome = data_handler.analysis()
#print(outcome)