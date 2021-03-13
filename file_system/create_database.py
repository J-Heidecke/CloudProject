#!/usr/bin/env python
# coding: utf-8

# In[18]:


import os 


# In[26]:


current_path = os.getcwd() # Should be root
user_database_path = current_path + '/User Database'

def make_database():
    if os.path.isdir(user_database_path) == False:
        os.mkdir(user_database_path)


# In[25]:


# This function should get the following user information, and return it:
# Username
# The user input -> dataset
# The outputs of the analysis 
# 
class get_user_information:
    def __init__(self):
        pass;
    def get_user_name(self):
        pass;
    def get_user_input(self):
        pass;
    def get_analysis_output(self):
        pass;


# In[48]:


class update_user_directory:
    def __init__(self):
        pass;
    
    def make_user_branch(self):
        user_information = get_user_information()
        user_name = user.information.get_user_name()
        user_directory = user_database_path + '/' + user_name
        if os.path.isdir(user_directory) == False:
            os.mkdir(user_directory)
            return user_directory
        else:
            return user_directory
        
    def update_user_branch(self):
        user_directory = self.make_user_branch()
        # Find the number of files in the directory 
        # To label new job file with a number
        # If empty create a new job file
        job_directory_list = os.listdir(user_directory)
        if not job_directory_list:
            first_job = user_directory + '/Job 1'
            os.mkdir(first_job)
            os.mkdir(first_job + '/Input Data')
            os.mkdir(first_job + '/Visualizations')
            os.mkdir(first_job + '/Numerical Outputs')
            return first_job
           
        else:
            job_directory[-1]
            job_name, job_number = job_directory_list[-1].split()
            new_job_number = int(job_number) + 1
            new_job = user_directory + '/Job ' + str(new_job_number)
            os.mkdir(new_job)
            os.mkdir(new_job + '/Input Data')
            os.mkdir(new_job + '/Visualizations')
            os.mkdir(new_job + '/Numerical Outputs')
            return new_job
    
    # This saves the data in the appropriate directories
    def save_data(self):
        data_directory = self.update_user_branch()
        pass;

