from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

class patch_analysis: 
#initialize class
    def __init__(self, path):
        self.path = path
        self.load_data(path)
        self.edit_data()
        
   #if you want to just run everything 
    def run_all(self):
        self.path = path
        self.load_data(path)
        self.edit_data()
        self.save_name()
        self.plot_sweeps()
        self.first_peak()
        self.time_correlates()
        self.peak_df()
        self.





#load in new file(s)
    def load_data(self, path):
        path = self.path
        data = loadmat(path)
        self.data = data
        print("total sweeps: " + str(len(data)))
        return data


#save file name as the file date and cell number
    def save_name(self):
        path = self.path 
        filename = os.path.basename(path)  # This will get '20221017_005.mat'
        variable_name = os.path.splitext(filename)[0]  #remove the extension, giving you file name/date ex: '20221017_005' 

        self.variable_name = variable_name
        print(variable_name)
        # Now you can use variable_name in your code
        return variable_name


#get rid of ititial keys 
    def edit_data(self):
        # data = self.load_data()
        #give access to variable names inside functions 
        data = self.data
        
        new_data = data.copy()  # Create a copy of the original dictionary

        for i in range(4):  # Remove the first three keys from the copy
            first_sweep_key = list(new_data.keys())[0]
            new_data.pop(first_sweep_key)

        for i in range(len(new_data.keys())):  
            first_sweep_key = list(new_data.keys())[i]
            first_value = new_data[first_sweep_key]

        self.new_data = new_data
        print('done1')
        return new_data 
        

    def plot_sweeps(self, start_time, end_time, initial_sweep, final_sweep): 
        
        new_data = self.new_data
        plt.figure(figsize=(10, 6))

        # Plot pA data over time for each trial
        for trial_name, pA in list(new_data.items())[initial_sweep:final_sweep]:
            pA = np.array(pA).flatten()  # flatten the array becuase it is 2D
            times = np.linspace(0, len(pA)/10, len(pA))  # create a time array
            plt.plot(times, pA * 1e12)  # multiplying by 1e12 to convert the unit from A to pA
            #break  # Break the loop after the first iteration
            
        #look only at specific time points for your base amp pre stim
        plt.ylim(-1000, 800) # adjust data range in pA
        plt.xlim(start_time, end_time) # adjust this according to your data range in pA


        plt.xlabel('Time (ms)')  # Add a label to the x-axis
        plt.ylabel('Picoamps (pA)')  # Add a label to the y-axis
        plt.title('Base amp')  # Add a title

        plt.grid(True)  
        return()

    def calculate_first_window(self,peak_window_start = 100, peak_window_end = 150): 
        all_first_peaks = []
        new_data = self.new_data
        count = 0
        for key, value in new_data.items():
            count += 1
       
            all_first_peaks.append(value[0][peak_window_start:peak_window_end]*(10**12))

        self.all_first_peaks = all_first_peaks
        return all_first_peaks
    
  
  
    def first_peak(self):
        self.calculate_first_window()
        all_first_peaks = self.all_first_peaks
        

        first_peak_list = []
        count = 0 
        for first_peak in all_first_peaks:

            first_peak = min(all_first_peaks[count])
            count += 1
            first_peak_list.append(first_peak)

        self.first_peak = first_peak
        return first_peak_list

    def time_correlates(self):
        new_data = self.new_data

        count = 0
        times = []
        for time in new_data:

            times.append(count)
            count += 0.333
        
        self.times = times
        return times

    def peak_df(self):
        variable_name = self.variable_name
        times = self.time_correlates()
        first_peak_list = self.first_peak()
        # times = self.times
        # first_peak_list = self.first_peak_list

        df = pd.DataFrame(
            {'first_peak': first_peak_list,
            'time': times}
             )

        df.to_csv('/Users/joyadler/Desktop/patch_df/' + variable_name + ".csv" )



    

