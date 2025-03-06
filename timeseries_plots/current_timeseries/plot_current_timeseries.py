# import libraries
#################################################################
import matplotlib.pyplot as plt
import numpy as np
import os


# import personal files
#################################################################
import load_save_data.load_data as load_data
import load_save_data.save_data as save_data
import printouts.progress_bar as prog_bar
import signal_processing.signal_processing as sig_proc
import plasma_data_and_parameters.q_profile.load_q_min as load_q_min



def plot_current_timeseries(crash_dir, shot_number):
    toroidal_current_data = load_data.load_json_file(f"plasma_data_and_parameters/toroidal_spline_current/toroidal_current_data/current_spline_{shot_number}.json")
    poloidal_current_data = load_data.load_json_file(f"plasma_data_and_parameters/poloidal_current/poloidal_current.json")[str(shot_number)]
    
    poloidal_current_time = np.linspace(1/1000, len(poloidal_current_data['data'])/1000, len(poloidal_current_data['data']))
    
    current_ratios = load_data.load_json_file(f"{crash_dir}/crash_info_with_cur_ratio.json")[str(shot_number)]
    crash_data = load_data.load_json_file(f"{crash_dir}/crash_info_with_hardware_error.json")[str(shot_number)]
    
    # Create the plot
    fig, ax1 = plt.subplots()

    # Plot data on the left y-axis
    ax1.plot(toroidal_current_data['time'], toroidal_current_data['data'])
    ax1.plot(poloidal_current_time, poloidal_current_data['data'])
    ax1.set_ylabel("Current [A]")
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a secondary y-axis on the right
    ax2 = ax1.twinx()
    ax2.plot(crash_data['times'], current_ratios, color='r')
    ax2.set_ylabel('Current Ratios', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title("Plasma Current Timeseries Data")
    plt.xlabel("Time [s]")
    
    plt.show()
    
    return


def plot_current_ratio_axuv_timeseries(shot_number):
    toroidal_current_data = load_data.load_json_file(f"plasma_data_and_parameters/toroidal_current/toroidal_current.json")[str(shot_number)]
    poloidal_current_data = load_data.load_json_file(f"plasma_data_and_parameters/poloidal_current/poloidal_current.json")[str(shot_number)]
    axuv_data = load_data.load_bson_file(f"preprocessed_data/raw_axuv_data/{int(shot_number/1000)*1000}/axuv_rawdata_{shot_number}.bson")
    
    current_times = np.linspace(1/1000, len(poloidal_current_data['data'])/1000, len(poloidal_current_data['data']))
    
    current_ratios = []
    for i in range(len(toroidal_current_data['data'])):
        current_ratios.append(toroidal_current_data['data'][i] / poloidal_current_data['data'][i])
        
    axuv_data[list(axuv_data.keys())[0]] = sig_proc.low_pass(axuv_data[list(axuv_data.keys())[0]], axuv_data['t'][1] - axuv_data['t'][0], 100*10**3)
            
    # Create the plot
    fig, ax1 = plt.subplots()

    # Plot data on the left y-axis
    ax1.plot(axuv_data['t'], axuv_data[list(axuv_data.keys())[0]], 'b')
    ax1.set_ylabel("Photodiode Current [A]", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xlabel("Time [s]")

    # Create a secondary y-axis on the right
    ax2 = ax1.twinx()
    ax2.plot(current_times, current_ratios, 'r')
    ax2.set_ylabel('I_tor/I_pol Reconstruction Outputs', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title(f"AXUV Signal and I_tor/I_pol Reconstruction Outputs Over Time\nShot: {shot_number}")
    
    plt.show()
    
    return

def plot_current_ratio_axuv_timeseries_q(shot_number):
    toroidal_current_data = load_data.load_json_file(f"plasma_data_and_parameters/toroidal_current/toroidal_current.json")[str(shot_number)]
    poloidal_current_data = load_data.load_json_file(f"plasma_data_and_parameters/poloidal_current/poloidal_current.json")[str(shot_number)]
    axuv_data = load_data.load_bson_file(f"preprocessed_data/raw_axuv_data/{int(shot_number/1000)*1000}/axuv_rawdata_{shot_number}.bson")
    
    current_times = np.linspace(1/1000, len(poloidal_current_data['data'])/1000, len(poloidal_current_data['data']))
    
    q_data, q_times = load_q_min.load_q_min_array(shot_number)
    
    current_ratios = []
    for i in range(len(toroidal_current_data['data'])):
        current_ratios.append(toroidal_current_data['data'][i] / poloidal_current_data['data'][i])
        
    axuv_data[list(axuv_data.keys())[0]] = sig_proc.low_pass(axuv_data[list(axuv_data.keys())[0]], axuv_data['t'][1] - axuv_data['t'][0], 100*10**3)
            
    # Create the plot
    fig, ax1 = plt.subplots()

    # Plot data on the left y-axis
    ax1.plot(axuv_data['t'], axuv_data[list(axuv_data.keys())[0]], 'b')
    ax1.set_ylabel("Photodiode Current [A]", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xlabel("Time [s]")

    # Create a secondary y-axis on the right
    ax2 = ax1.twinx()
    ax2.plot(current_times, current_ratios, 'r')
    ax2.plot(q_times, q_data, 'k')
    ax2.set_ylabel('I_tor/I_pol Reconstruction Outputs', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title(f"AXUV Signal and I_tor/I_pol Reconstruction Outputs Over Time\nShot: {shot_number}")
    
    plt.show()
    
    return