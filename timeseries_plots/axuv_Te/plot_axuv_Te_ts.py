# import libraries
#################################################################
import matplotlib.pyplot as plt
import os
import scipy.signal as sig




# import personal files
#################################################################
import load_save_data.load_data as load_data
from axuv_crash_postprocessing.particle_inventory.crash_particle_inventory_scatter_helper import *
import signal_processing.signal_processing as sig_proc



def plot_ts_axuv_Te(shot):
    axuv_data_directory = f"preprocessed_data/axuv_timeseries_plotting/{int(shot/1000)*1000}/{shot}_ts.bson"
    axuv_data = load_data.load_bson_file(axuv_data_directory)
    
    axuv_Te_data_directory = os.environ['AURORA_REPOS'] + "/BH_axuv_Te/axuv_Te_data/" + str(int(int(shot) / 1000)*1000) + "/" + "axuv_Te_data_" + str(shot) + ".bson"
    if os.path.isfile(axuv_Te_data_directory):
        axuv_Te_data = load_data.load_bson_file(axuv_Te_data_directory)
        # dt = (axuv_Te_data['axuv_Te_time (ms)'][1] - axuv_Te_data['axuv_Te_time (ms)'][0])
        # for k in axuv_Te_data.keys():
        #     if k[:5] == "Mylar":
        #         axuv_Te_data[k] = sig_proc.low_pass(axuv_Te_data[k], dt, 100*10**3)
        #         axuv_Te_data[k] = sig.savgol_filter(axuv_Te_data[k], int(1/dt), 3)
    else:
        print(f"DATA INVALID FOR SHOT {shot}")
        
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")

    # Create the plot
    fig, ax1 = plt.subplots()

    # Plot data on the left y-axis
    ax1.plot(axuv_data['t'], axuv_data[list(axuv_data.keys())[0]], 'b')
    ax1.set_ylabel("Photodiode Current [A]", color='blue')
    ax1.set_ylim(bottom=min(axuv_data[list(axuv_data.keys())[0]][:int(0.9*find_closest_index(axuv_data['t'], lifetimes_dict[str(shot)]))])-0.1*max(axuv_data[list(axuv_data.keys())[0]][:int(0.9*find_closest_index(axuv_data['t'], lifetimes_dict[str(shot)]))]) , top=1.1*max(axuv_data[list(axuv_data.keys())[0]][:int(0.9*find_closest_index(axuv_data['t'], lifetimes_dict[str(shot)]))]))
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xlabel("Time [s]")

    # Create a secondary y-axis on the right
    ax2 = ax1.twinx()
    for k in axuv_Te_data.keys():
        if 'Mylar' in k:
            ax2.plot([t / 1000 for t in axuv_Te_data['axuv_Te_time (ms)']], axuv_Te_data[k], label=k, alpha=0.5)
    ax2.set_ylim(-100, 1000)
    ax2.set_ylabel('AXUV Te [eV]')
    ax2.tick_params(axis='y')

    plt.title(f"AXUV Signal and Particle Inventory Reconstruction Outputs Over Time\nShot: {shot}")    
    plt.legend()
    
    plt.show()
    
    return