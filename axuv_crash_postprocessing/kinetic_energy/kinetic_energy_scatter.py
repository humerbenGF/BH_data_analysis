# import libraries
#################################################################
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.integrate import cumtrapz
import numpy as np
import mpld3
import os
import matplotlib.colors as mcolors
from matplotlib.colors import Normalize
import plotly.graph_objects as go



# import personal files
#################################################################
import load_save_data.load_data as load_data
import cursors.scatter_cursors as cursor
import cursors.add_click_action as click
import printouts.progress_bar as prog_bar
from axuv_crash_postprocessing.kinetic_energy.kinetic_energy_scatter_helper import *
from axuv_crash_postprocessing.thomson.crash_thomson_load_data import load_thomson_phase_data_by_shot


def reconstruct_plasma_kinetic_energy_over_phase_single_num_crashes(data_dir, thomson_position, num_phase_bins, num_crashes=0, matplotlib=True, plotly=False, show_plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    
    ######################################################################################################################################################################################
    ######################################################################################################################################################################################
    # PARTICLE INVENTORY
    ######################################################################################################################################################################################
    ######################################################################################################################################################################################
    
    # load in data
    crash_dict = load_data.load_json_file("2024-10-10_19718-23016/crash_info.json")
    particle_inventory_dict = load_data.load_json_file("plasma_data_and_parameters/particle_inventory/particle_inventory.json")
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    # plotting arrays
    part_invent_array = []
    part_invent_phase_array = []
    part_invent_time_array = []
    
    part_invent_slope_array = []
    part_invent_phase_slope_array = []

    part_invent_recon_array = []
    part_invent_phase_recon_array = []
    
    # make arrays of thomson Particle Inventory data
    tot = len(crash_dict)
    cur = 1
    for s in crash_dict.keys():
        if s in lifetimes_dict.keys() and s in particle_inventory_dict.keys():
            if type(lifetimes_dict[s]) != type(str()) and type(particle_inventory_dict[s]) != type(str()) and type(crash_dict[s]) != type(str()):
                if len(particle_inventory_dict[s]['data']) >= 1 and len(crash_dict[s]['times']) == num_crashes:
                    # make array of all temps
                    phase = load_data.load_json_file(data_dir + "crash_phase/phase_" + str(s) + ".json")
                    for i in range(len(particle_inventory_dict[s]['data'])):
                        part_invent_array.append(particle_inventory_dict[s]['data'][i])
                        part_invent_time_array.append((i+1)/1000)
                        # get phase offset based on how many crashes have occurred
                        j = 0
                        while len(crash_dict[s]['times']) > j:
                            if crash_dict[s]['times'][j] < (i+1)/1000:
                                j += 1
                            else:
                                break
                        
                        part_invent_phase_array.append(phase['phase'][find_closest_index(phase['time'], part_invent_time_array[-1])] + j)
                        
                    # make array of all slopes
                    for i in range(len(particle_inventory_dict[s]['data']) - 1):
                        part_invent_slope_array.append((part_invent_array[-(i+1)] - part_invent_array[-i]) / (part_invent_phase_array[-(i+1)] - part_invent_phase_array[-i]))
                        part_invent_phase_slope_array.append((part_invent_phase_array[-(i+1)] + part_invent_phase_array[-i]) / 2)
        
        prog_bar.progress_bar_pct_only(cur, tot)
        cur += 1
                    
    # reconstruct thomson temp from slope data
        # get indices of sorted arrays
    thomson_slope_indices_sorted_by_phase = np.argsort(part_invent_phase_slope_array)
    part_invent_slope_array = [part_invent_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    part_invent_phase_slope_array = [part_invent_phase_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
            
    
    ######################################################################################################################################################################################
    ######################################################################################################################################################################################
    # THOMSON TEMPERATURE
    ######################################################################################################################################################################################
    ######################################################################################################################################################################################
    
    # load in data
    data_dict_by_shot = load_thomson_phase_data_by_shot(data_dir, True, True, True, True)
    
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    # plotting arrays
    thomson_temp_array = []
    thomson_phase_array = []
    thomson_time_array = []
    
    thomson_temp_slope_array = []
    thomson_phase_slope_array = []
    
    thomson_temp_slope_array_time = []
    thomson_time_slope_array = []

    thomson_temp_recon_array = []
    thomson_phase_recon_array = []
    thomson_time_recon_array = []
    
    # make arrays of thomson temperature data
    for s in data_dict_by_shot.keys():
        if s in lifetimes_dict.keys():
            if type(lifetimes_dict[s]) != type(str()):
                sorted_by_time = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_times"])
                
                if len(sorted_by_time) >= 1 and len(data_dict_by_shot[s]["crash_info"]['times']) == num_crashes:
                    # make array of all temps
                    for i in range(len(sorted_by_time)):
                        thomson_temp_array.append(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i]])
                        thomson_time_array.append(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[i]])
                        # get phase offset based on how many crashes have occurred
                        j = 0
                        while len(data_dict_by_shot[s]["crash_info"]['times']) > j:
                            if data_dict_by_shot[s]["crash_info"]['times'][j] < data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[i]]:
                                j += 1
                            else:
                                break
                        
                        thomson_phase_array.append(data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[i]] + j)
                        
                    # make array of all slopes
                    for i in range(len(sorted_by_time) - 1):
                        thomson_temp_slope_array.append((thomson_temp_array[-(i+1)] - thomson_temp_array[-i]) / (thomson_phase_array[-(i+1)] - thomson_phase_array[-i]))
                        thomson_phase_slope_array.append((thomson_phase_array[-(i+1)] + thomson_phase_array[-i]) / 2)
                    
    # reconstruct thomson temp from slope data
        # get indices of sorted arrays
    thomson_slope_indices_sorted_by_phase = np.argsort(thomson_phase_slope_array)
    thomson_temp_slope_array = [thomson_temp_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    thomson_phase_slope_array = [thomson_phase_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    
    
    ######################################################################################################################################################################################
    ######################################################################################################################################################################################
    # INTEGRATION OF BOTH QUANTITIES
    ######################################################################################################################################################################################
    ######################################################################################################################################################################################

        
    # get boundaries of bins
    bin_edges_phase = np.linspace(min(part_invent_phase_slope_array[0],thomson_phase_slope_array[0]), max(part_invent_phase_slope_array[-1], thomson_phase_slope_array[-1]), num_phase_bins + 1)
    bin_edges_phase_pi = np.linspace(part_invent_phase_slope_array[0], part_invent_phase_slope_array[-1], num_phase_bins + 1)
    bin_edges_phase_temp = np.linspace(thomson_phase_slope_array[0], thomson_phase_slope_array[-1], num_phase_bins + 1)
    
        # part inv
    pi_slope_means = []
    pi_slope_phase_means = []
        # thomson
    thomson_slope_temp_means = []
    thomson_slope_phase_means = []
    
    for i in range(len(bin_edges_phase) - 1):
        # part inv
        pi_mean = median_of_bin(part_invent_slope_array, part_invent_phase_slope_array, bin_edges_phase_pi[i], bin_edges_phase_pi[i+1])
        pi_slope_means.append(pi_mean) if pi_mean is not None else None
        pi_phase_mean = median_of_bin(part_invent_phase_slope_array, part_invent_phase_slope_array, bin_edges_phase_pi[i], bin_edges_phase_pi[i+1])
        pi_slope_phase_means.append(pi_phase_mean) if pi_phase_mean is not None else None
        # thomson
        t_s_t_mean = median_of_bin(thomson_temp_slope_array, thomson_phase_slope_array, bin_edges_phase_temp[i], bin_edges_phase_temp[i+1])
        thomson_slope_temp_means.append(t_s_t_mean) if t_s_t_mean is not None else None
        t_s_p_mean = median_of_bin(thomson_phase_slope_array, thomson_phase_slope_array, bin_edges_phase_temp[i], bin_edges_phase_temp[i+1])
        thomson_slope_phase_means.append(t_s_p_mean) if t_s_p_mean is not None else None
        
    # integrate part inv
    part_invent_recon_array = cumtrapz(pi_slope_means, pi_slope_phase_means, initial=0)
    part_invent_phase_recon_array = pi_slope_phase_means
    # integrate thomson
    thomson_temp_recon_array = cumtrapz(thomson_slope_temp_means, thomson_slope_phase_means, initial=0)
    thomson_phase_recon_array = thomson_slope_phase_means
    


    # zero out arrays
        # pi
    for i in range(len(part_invent_recon_array)):
        part_invent_recon_array[i] = part_invent_recon_array[i] - min(part_invent_recon_array)
        
        # thomson
    for i in range(len(thomson_temp_recon_array)):
        thomson_temp_recon_array[i] = thomson_temp_recon_array[i] - min(thomson_temp_recon_array)
        


    # offset pi array by c
    c = np.mean(part_invent_array) - np.nanmean(part_invent_recon_array)
    for i in range(len(part_invent_recon_array)):
        part_invent_recon_array[i] = part_invent_recon_array[i] + c

    # offset thomson array by c
    c = np.mean(thomson_temp_array) - np.nanmean(thomson_temp_recon_array)
    for i in range(len(thomson_temp_recon_array)):
        thomson_temp_recon_array[i] = thomson_temp_recon_array[i] + c
        
    
    # combine into energy
    kinetic_energy_recon_array = []
    kinetic_energy_phase_recon_array = []
    for i in range(len(bin_edges_phase)-1):
        kinetic_energy_recon_array.append(get_interp_value(thomson_phase_recon_array, thomson_temp_recon_array, (bin_edges_phase[i] + bin_edges_phase[i+1]) / 2) * get_interp_value(part_invent_phase_recon_array, part_invent_recon_array, (bin_edges_phase[i] + bin_edges_phase[i+1]) / 2) * 1.602*10**(-19))
        kinetic_energy_phase_recon_array.append((bin_edges_phase[i] + bin_edges_phase[i+1]) / 2)

        


    if matplotlib:
        # Plots of Kinetic Energy over Phase
        #######################################################################################################
        
        # scatter of the reconstructed thomson slope over phase data
        fig, ax = plt.subplots(figsize=(16,9))
        # plt.scatter(part_invent_phase_array, thomson_temp_array, color='k', marker='.')
        plt.plot(kinetic_energy_phase_recon_array, kinetic_energy_recon_array, color='r')
        plt.title(f"Kinetic Energy Over Phase at TS{thomson_position}\n{num_crashes} Crashes")
        plt.xlabel("Phase")
        plt.ylabel("Kinetic Energy [J]")
        plt.grid(True)
        plt.show()
        
    
    if plotly:
        # Scatter of the reconstructed Thomson slope over phase data
        recon_line_phase = go.Scatter(x=kinetic_energy_phase_recon_array, 
                                    y=kinetic_energy_recon_array, 
                                    mode='lines', 
                                    line=dict(color='red'),
                                    name='Reconstructed')

        # Create layout for the phase recon plot
        layout_recon_phase = go.Layout(title=f"Kinetic Energy Over Phase at TS{thomson_position}\n{num_crashes} Crashes",
                                    xaxis=dict(title='Phase',
                                        showgrid=True,  # Enable grid lines for the x-axis
                                        gridcolor="lightgray",  # Color of the grid lines
                                        gridwidth=1  # Thickness of the grid lines
                                    ),
                                    yaxis=dict(title='Kinetic Energy [J]',
                                        showgrid=True,  # Enable grid lines for the x-axis
                                        gridcolor="lightgray",  # Color of the grid lines
                                        gridwidth=1  # Thickness of the grid lines
                                    ),
                                    showlegend=True,
                                    template='plotly_white')

        # Create the figure and plot the phase recon data
        fig_recon_phase = go.Figure(data=[recon_line_phase], layout=layout_recon_phase)
        fig_recon_phase.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/recon_kinetic_energy/kinetic_energy_over_phase_ts{thomson_position}_{num_crashes}crash.html")
        if show_plotly:
            fig_recon_phase.show()

    
    return