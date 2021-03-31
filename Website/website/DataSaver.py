#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 13:27:14 2021

@author: pedrojose
"""
import matplotlib.pyplot as plt
import os

class DataSaver():
    
    def __init__(self, image_data, text_data):
        self.image_data = image_data
        self.text_data = text_data
        
    def save_data(path, data):
        pass #plt.savefig(args, kwargs)
        
    def save_fig(path, fig_id, tight_layout=True, fig_extension="png", resolution=300):
        """ Saves the figures"""
        path = os.path.join(path, fig_id + "." + fig_extension)
        #print("Saving figure", fig_id)
        if tight_layout:
            plt.tight_layout()
        # save the figure
        plt.savefig(path, format=fig_extension, dpi=resolution)