import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import PIL
import os
import _pickle as pk

class create_vis:
    def __init__(self, job_name, file_system_path):
        self.file_path = os.path.join(file_system_path, 'results/')
        self.data_path = os.path.join(file_system_path, 'data')
        self.job_name = job_name
        self.destination = os.path.join(self.file_path + '/' + self.job_name)

    def load_data(self):
        results = []
        file = os.path.join(self.destination + '/' + self.job_name + 'metrics.ob')
        with open(file, "rb") as input_file:
         	e = pk.load(input_file)
         	results.append(e)
         

        results = results[0]
        for i in results:
            plt.scatter(i.keys(), i.values(), s=300)
            plt.xlabel('Model Name')
            plt.ylabel('Accuracy')
        plot_path = os.path.join(self.destination + '/' + self.job_name + 'metrics_plot')
        print(plot_path)
        plt.savefig(plot_path)
        plt.clf()
        
        csv_file = os.path.join(self.data_path, self.job_name + '.csv')
        df = pd.read_csv(csv_file)
        
        for i in range(1, len(df.columns)): 
            plt.scatter(df.iloc[i-1], df.iloc[i], s=100)
            plt.xlabel(df.columns[i-1])
            plt.ylabel(df.columns[i])
            plot_path = os.path.join(self.destination + '/' + 'plot' + str(i))
            plt.savefig(plot_path)
            plt.clf()