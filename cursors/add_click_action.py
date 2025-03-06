# import packages
#################################################################
import os
import mplcursors
import subprocess
import matplotlib.pyplot as plt

import timeseries_plots.axuv_ts_q_min.plot_axuv_q_min_ts as plot_axuv_q
import timeseries_plots.q_profile.plot_q_profile as plot_q
import timeseries_plots.particle_inventory.axuv_particle_inventory_ts as plot_part_inv
import timeseries_plots.axuv_Te.plot_axuv_Te_ts as plot_axuv_Te


def add_click_action_timeseries_plots(output_dir, scatter, fig, shots_list, click_timeseries_plots_list=[]):
    # Define the click event
    def on_pick(event):
        ind = event.ind[0]
        print(f"Pick Event Initialized for Shot {shots_list[ind]}")
        if click_timeseries_plots_list == [] or "crashes" in click_timeseries_plots_list or "all" in click_timeseries_plots_list:
            file_path = output_dir + "plots/non_normalized/" + str(shots_list[ind]) + ".png"
            print(f"\tOpening file: {file_path}")
            # Ensure the file exists for demonstration purposes
            if not os.path.exists(file_path):
                print("FILE DOES NOT EXIST")

            subprocess.Popen(['start', file_path], shell=True)
            
    # Connect the pick event handler
    print("Picking Enabled")
    fig.canvas.mpl_connect('pick_event', on_pick)

    # Make the scatter plot pickable
    scatter.set_picker(True)
    scatter.set_pickradius(3)
    

    return

def add_click_action_axuv_q_ts(scatter, fig, shots_list):
        # Define the click event
    def on_pick(event):
        ind = event.ind[0]
        plot_axuv_q.plot_axuv_q_min(int(shots_list[ind]))
        plot_q.plot_q_profile(int(shots_list[ind]))
            
            
    # Connect the pick event handler
    fig.canvas.mpl_connect('pick_event', on_pick)

    # Make the scatter plot pickable
    scatter.set_picker(True)
    
    return

def add_click_action_axuv_part_inv_ts(scatter, fig, shots_list):
    # Define the click event
    def on_pick(event):
        ind = event.ind[0]
        plot_part_inv.plot_ts_axuv_part_inv(int(shots_list[ind]))
            
    # Connect the pick event handler
    fig.canvas.mpl_connect('pick_event', on_pick)

    # Make the scatter plot pickable
    scatter.set_picker(True)
    
    return

def add_click_action_axuv_Te(scatter, fig, shots_list):
    # Define the click event
    def on_pick(event):
        ind = event.ind[0]
        plot_axuv_Te.plot_ts_axuv_Te(int(shots_list[ind]))
            
    # Connect the pick event handler
    fig.canvas.mpl_connect('pick_event', on_pick)

    # Make the scatter plot pickable
    scatter.set_picker(True)
    
    
    return