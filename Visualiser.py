#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 17:53:27 2021

@author: pedrojose
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

class Visualiser:
    
    def __init__(self, data):
        self.data = data


    def plot_boxplot(self, kind='box', rot=90, title='Boxplot', figsize=None, figsave=False, savepath=None):
        """Plots a boxplot graph of the data"""

        fig = plt.figure()        
        if figsize:
            fig = self.data.plot(kind=kind, rot=rot, title=title, figsize=figsize)
            
        else:
            
            fig = self.data.plot(kind=kind, rot=rot, title=title)
        
        if figsave:
            if savepath is not None:
                self.save_fig(path=savepath, fig_id=kind)
        plt.show()
        return fig

    
    def plot_histogram(self, bins=50, figsize=None, figsave=False, savepath=None):
        """Plots a histogram graph of the data"""
        fig = plt.figure()
        
        if figsize:
            
            fig = self.data.hist(bins=bins, figsize=figsize)
        else:
            
            fig = self.data.hist(bins=bins)
        
        if figsave:
            if savepath is not None:
                self.save_fig(path=savepath, fig_id='hist')
            
        plt.show()
        return fig

    
    def plot_heatmap(self, data, annot=True):
        return sns.heatmap(data, annot=True, cmap=plt.cm.OrRd)
        
        
    def save_fig(path, fig_id, tight_layout=True, fig_extension="png", resolution=300):
        """ Saves the figures"""
        path = os.path.join(path, fig_id + "." + fig_extension)
        print("Saving figure", fig_id)
        if tight_layout:
            plt.tight_layout()
        # save the figure
        plt.savefig(path, format=fig_extension, dpi=resolution)