# import packages
#################################################################
import matplotlib.pyplot as plt
import numpy as np


# import personal files
#################################################################
import plasma_data_and_parameters.q_profile.load_q_min as load_q_min
import load_save_data.load_data as load_data
import signal_processing.signal_processing as sig_proc


def plot_axuv_q_min(shot_number):
    q_data, q_min_errors, q_times = load_q_min.load_q_min_array(shot_number)
    axuv_data = load_data.load_bson_file(f"preprocessed_data/raw_axuv_data/{int(shot_number/1000)*1000}/axuv_rawdata_{shot_number}.bson")
        
    axuv_data[list(axuv_data.keys())[0]] = sig_proc.low_pass(axuv_data[list(axuv_data.keys())[0]], axuv_data['t'][1] - axuv_data['t'][0], 100*10**3)
            
    # Create the plot
    fig, ax1 = plt.subplots(figsize=(16,10))
    fig.set()

    # Plot data on the left y-axis
    ax1.plot(axuv_data['t'], axuv_data[list(axuv_data.keys())[0]], 'b')
    ax1.set_ylabel("Photodiode Current [A]", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xlabel("Time [s]")

    # Create a secondary y-axis on the right
    ax2 = ax1.twinx()
    ax2.plot(q_times, q_data, 'r', marker='o', linestyle='-')
    ax2.set_ylabel('q_min', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title(f"AXUV Signal and q_min Over Time\nShot: {shot_number}")
    
    plt.show()
    
    return

