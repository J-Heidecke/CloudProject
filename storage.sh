#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 20:26:18 2021
@author: pedrojose
"""

# sets the cucket name to store the data 

# create the bucket 
export BUCKET_NAME= YOUR BUCKET NAME
gsutil mb -c STANDARD -l europe-west2 gs://${BUCKET_NAME}






#create location folder for results
export COMMON_PATH=./website/static/file_system/

# storing to google cloud
gsutil cp -r ${COMMON_PATH} gs://${BUCKET_NAME}
