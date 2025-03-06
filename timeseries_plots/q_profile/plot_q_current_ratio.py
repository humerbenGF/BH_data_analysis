# import packages
#################################################################
import matplotlib.pyplot as plt
import numpy as np

# import personal files
#################################################################
import plasma_data_and_parameters.q_profile.load_q_min as load_q_min
import load_save_data.load_data as load_data
import signal_processing.signal_processing as sig_proc


def plot_q_min_current(shot_number):
    toroidal_current_data = load_data.load_json_file(f"plasma_data_and_parameters/toroidal_current/toroidal_current.json")[str(shot_number)]
    poloidal_current_data = load_data.load_json_file(f"plasma_data_and_parameters/poloidal_current/poloidal_current.json")[str(shot_number)]
    axuv_data = load_data.load_bson_file(f"preprocessed_data/raw_axuv_data/{int(shot_number/1000)*1000}/axuv_rawdata_{shot_number}.bson")
    
    current_times = np.linspace(1/1000, len(poloidal_current_data['data'])/1000, len(poloidal_current_data['data']))
    
    q_data, q_times = load_q_min.load_q_min_array(shot_number)
    
    current_ratios = []
    for i in range(len(toroidal_current_data['data'])):
        current_ratios.append(toroidal_current_data['data'][i] / poloidal_current_data['data'][i])
        
    axuv_data[list(axuv_data.keys())[0]] = sig_proc.low_pass(axuv_data[list(axuv_data.keys())[0]], axuv_data['t'][1] - axuv_data['t'][0], 100*10**3)
    
    
    plt.scatter(q_data, current_ratios)
    plt.xlabel('q')
    plt.ylabel('cr')
    
    plt.show()
    
    
    return