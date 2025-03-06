# import libraries
#################################################################
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.integrate import cumtrapz
import numpy as np
import mpld3
import os
import matplotlib.colors as mcolors


# import personal files
#################################################################
import load_save_data.load_data as load_data
import cursors.scatter_cursors as cursor
import cursors.add_click_action as click
import printouts.progress_bar as prog_bar
from axuv_crash_postprocessing.particle_inventory.crash_particle_inventory_scatter_helper import *


def plot_ts_axuv_part_inv(shot):
    axuv_data_directory = f"preprocessed_data/axuv_timeseries_plotting/{int(shot/1000)*1000}/{shot}_ts.bson"
    axuv_data = load_data.load_bson_file(axuv_data_directory)
    
    particle_inventory_dict = load_data.load_json_file("plasma_data_and_parameters/particle_inventory/particle_inventory.json")
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    part_inventory_time = np.linspace(1/1000, len(particle_inventory_dict[str(shot)]['data'])/1000, len(particle_inventory_dict[str(shot)]['data']))
    
    if type(str()) in [type(particle_inventory_dict[str(shot)]), type(lifetimes_dict[str(shot)])]:
        print(f"DATA INVALID FOR SHOT {shot}")
        return

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
    ax2.plot(part_inventory_time, particle_inventory_dict[str(shot)]['data'], 'r')
    ax2.set_ylabel('Particle Inventory', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    plt.title(f"AXUV Signal and Particle Inventory Reconstruction Outputs Over Time\nShot: {shot}")    
    
    plt.show()
    
    return