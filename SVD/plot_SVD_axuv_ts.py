# import packages
#################################################################
import matplotlib.pyplot as plt
import numpy as np


# import personal files
#################################################################
import plasma_data_and_parameters.q_profile.load_q_min as load_q_min
import load_save_data.load_data as load_data
import signal_processing.signal_processing as sig_proc







def plot_axuv_SVD(shot_number, SVD_dir):
    # reformat SVD directory
    if SVD_dir[-1] != "/":
        SVD_dir += "/"
        
    SVD_pol_data = load_data.load_json_file(f"{SVD_dir}SVD_info_poloidal.json")
    SVD_tor_data = load_data.load_json_file(f"{SVD_dir}SVD_info_toroidal.json")
    axuv_data = load_data.load_bson_file(f"preprocessed_data/raw_axuv_data/{int(shot_number/1000)*1000}/axuv_rawdata_{shot_number}.bson")
        
    axuv_data[list(axuv_data.keys())[0]] = sig_proc.low_pass(axuv_data[list(axuv_data.keys())[0]], axuv_data['t'][1] - axuv_data['t'][0], 100*10**3)
    
    SVD_data_pol_plot = []
    SVD_data_tor_plot = []
    t = []

    for i in range(len(SVD_pol_data[str(shot_number)]["t"])):
        # different ratio options in here
        # SVD_data_pol_plot.append(SVD_pol_data[str(shot_number)]['n0'][i] / ((SVD_pol_data[str(shot_number)]['n1'][i] + SVD_pol_data[str(shot_number)]['n2'][i]) / 2))
        # SVD_data_tor_plot.append(SVD_tor_data[str(shot_number)]['n0'][i] / ((SVD_tor_data[str(shot_number)]['n1'][i] + SVD_tor_data[str(shot_number)]['n2'][i]) / 2))
        # SVD_data_pol_plot.append(SVD_pol_data[str(shot_number)]['n1'][i] / SVD_pol_data[str(shot_number)]['n2'][i])
        # SVD_data_tor_plot.append(SVD_tor_data[str(shot_number)]['n1'][i] / SVD_tor_data[str(shot_number)]['n2'][i])
        SVD_data_pol_plot.append(SVD_pol_data[str(shot_number)]['n2'][i] / SVD_pol_data[str(shot_number)]['n1'][i])
        SVD_data_tor_plot.append(SVD_tor_data[str(shot_number)]['n2'][i] / SVD_tor_data[str(shot_number)]['n1'][i])
        t.append(SVD_pol_data[str(shot_number)]['t'][i])
    
    # Create the plot
    fig, ax1 = plt.subplots(figsize=(8,5))
    fig.set()
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Plot data on the left y-axis
    ax1.plot(axuv_data['t'], axuv_data[list(axuv_data.keys())[0]], color=default_colors[0], label="AXUV Signal")
    ax1.set_ylabel("Photodiode Current [A]")
    ax1.tick_params(axis='y')
    ax1.set_xlabel("Time [s]")

    # Create a secondary y-axis on the right
    ax2 = ax1.twinx()
    ax2.plot(t, SVD_data_pol_plot, color=default_colors[1], marker='o', linestyle='-', label="Poloidal Mode Ratio")
    ax2.plot(t, SVD_data_tor_plot, color=default_colors[2], marker='o', linestyle='-', label="Toroidal Mode Ratio")

    ax2.set_ylabel('Mode Ratio')
    ax2.tick_params(axis='y')

    plt.title(f"AXUV Signal and SVD Decomposed Mode Ratios Over Time\nShot: {shot_number}")
    plt.legend()
    
    plt.show()
    
    return