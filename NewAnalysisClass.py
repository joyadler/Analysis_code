from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


class patch_analysis: 

    def __init__(self, path):
        self.path = path
        self.load_data(path)
        self.edit_data()
        #self.save_name()
        
   #if you want to just run everything 
    def run_all(self):
        self.load_data()
        self.save_name()
        self.edit_data()
        self.plot_sweeps(0,188, 0,100)
        self.avg_baseline()
        self.calc_min_first_peak()
        self.calculate_first_response()
        self.time_correlates()
        df = self.peak_df()

        return df



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
        # Now use variable_name in the code
        return variable_name


#get rid of ititial keys 
    def edit_data(self):
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
        return new_data 
        
#plot all sweeps to look at the data, or just select sweeps at specific time points
    def plot_sweeps(self, start_time, end_time, initial_sweep, final_sweep): 
        
        new_data = self.new_data
        plt.figure(figsize=(10, 6))

        # plot pA data over time for each trial
        for trial_name, pA in list(new_data.items())[initial_sweep:final_sweep]:
            pA = np.array(pA).flatten()  # flatten the array becuase it is 2D
            times = np.linspace(0, len(pA)/10, len(pA))  # create a time array
            plt.plot(times, pA * 1e12)  # multiplying by 1e12 to convert the unit from A to pA

            
        #look only at specific time points for your base amp pre stim
        plt.ylim(-1000, 800) # adjust data range in pA
        plt.xlim(start_time, end_time) # adjust this according to your data range in pA


        plt.xlabel('Time (ms)')  # Add a label to the x-axis
        plt.ylabel('Picoamps (pA)')  # Add a label to the y-axis
        plt.title('Base amp')  # Add a title

        plt.grid(True)  
        return('done')
    
    
    #get baseline values for each sweep
    def calculate_baseline(self, baseline_window_start = 50, baseline_window_end = 100):
        baseline_values = []
        new_data = self.new_data
        count = 0
        for key, value in new_data.items():
            count += 1
            baseline_values.append(value[0][baseline_window_start:baseline_window_end]*(10**12))

        self.baseline_values = baseline_values
        return baseline_values  
    

    def avg_baseline(self):
        self.calculate_baseline()
        baseline_values = self.baseline_values    
        avg_baseline_value = []
        for basline_window in baseline_values:
        
            baseline = sum(basline_window) / len(basline_window)
            avg_baseline_value.append(baseline)
            
        self.avg_baseline_value = avg_baseline_value
        return avg_baseline_value

    
    def calculate_first_window(self,peak_window_start = 100, peak_window_end = 150): 
        all_first_peaks = []
        new_data = self.new_data
        count = 0
        for key, value in new_data.items():
            count += 1
       
            all_first_peaks.append(value[0][peak_window_start:peak_window_end]*(10**12))
        self.all_first_peaks = all_first_peaks
        return all_first_peaks
  
    def calc_min_first_peak(self):
        calculate_first_window = self.calculate_first_window()
        #all_first_peaks = self.all_first_peaks()    

        min_first_peak = []
        for first_peak in calculate_first_window:
        
            first_peak = min(first_peak)
            min_first_peak.append(first_peak)
            
        self.min_first_peak = min_first_peak
        return min_first_peak


    # # calculate the actual response size 
    def calculate_first_response(self):
        calc_min_first_peak = self.calc_min_first_peak()
        avg_baseline = self.avg_baseline()
        avg_baseline_value = self.avg_baseline_value
        min_first_peak = self.min_first_peak
        first_response_pA = []
        for baseline in avg_baseline:
            for value in min_first_peak:
                response = value - baseline
            first_response_pA.append(response)
        
        self.first_response_pA = first_response_pA
        return first_response_pA


        # calculate_baseline = self.calculate_baseline()
        # calculate_first_window = self.calculate_first_window()
        # #self.first_peak()
        # all_first_peaks = self.all_first_peaks()

        # for first_response_pA in all_first_peaks:
        #     print(first_response_pA)


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
        variable_name = self.save_name()
        avg_baseline = self.avg_baseline()
        times = self.time_correlates()
        first_peak_list = self.calc_min_first_peak()
        first_response_pA = self.calculate_first_response()

    
        df = pd.DataFrame(
            {'first_peak': first_peak_list,
             'avg_baseline': avg_baseline,
            'first_response_pA': first_response_pA,
            'time': times
            }
             )
        self.df = df
        df.to_csv('/Users/joyadler/Desktop/patch_df/' + variable_name + ".csv" )

        return df 

        

