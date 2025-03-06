# import packages
#################################################################
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.integrate import cumtrapz


# import personal files
#################################################################
import load_save_data.load_data as load
from printouts.progress_bar import progress_bar_pct_only as pb_pct
import cursors.scatter_cursors as cursors
import cursors.add_click_action as click
from axuv_crash_postprocessing.q.crash_q_scatter_helper import *
import plots_github.GF_html_plot_viewer.plot_generation_tools.plotly_scatter as plotly_scatter



# import personal files
#################################################################
def reconstruct_J_change_over_phase_without_last_half_cycle_nums_crashes_sustain_non_sustain(data_dir, num_phase_bins, nums_crashes_array, J_psibar='05', show_plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    if J_psibar == 'min':
        J_dict = load.load_json_file("plasma_data_and_parameters/J_profile/J_min_data.json")
    if J_psibar == 'max':
        J_dict = load.load_json_file("plasma_data_and_parameters/J_profile/J_max_data.json")
    if J_psibar == '05':
        J_dict = load.load_json_file("plasma_data_and_parameters/J_profile/J_05_data.json")
        
    sustainment_dict = load.load_json_file("machine_settings_and_state/sustainment/sustainment.json")
    crash_dict = load.load_json_file("2024-10-10_19718-23016/crash_info_with_hardware_error.json")
    
    # plotting arrays
        # J and phase arrays
    J_array_sustain = []
    J_array_non_sustain = []
    J_phase_array_sustain = []
    J_phase_array_non_sustain = []
        # J and phase slope arrays
    J_slope_array_sustain = []
    J_slope_array_non_sustain = []
    J_phase_slope_array_sustain = []
    J_phase_slope_array_non_sustain = []
        # shot number arrays
    shot_numbers_slope_array_sustain = []
    shot_numbers_slope_array_non_sustain = []
    
    unique_shots = []
    
    # make arrays of thomson temperature data
    fig, ax = plt.subplots(figsize=(16,9))
    cur = 1
    tot = len(J_dict)
    for s in J_dict.keys():
        if s in crash_dict.keys() and s in sustainment_dict:
            if type(sustainment_dict[s]) != type(str()) and type(J_dict[s]) != type(str()) and type(crash_dict[s]) != type(str()) and max(J_dict[s]['data']) < 10**7:
                temp_data = load_data.load_json_file(data_dir + "crash_phase/phase_" + str(s) + ".json")
                if sustainment_dict[s] > 0 and len(crash_dict[s]['times']) in nums_crashes_array:
                    valid_J_points_shot=0
                    for i in range(len(J_dict[s]['data'])):
                        # get phase offset based on how many crashes have occurred
                        j = 0
                        while len(crash_dict[s]['times']) > j:
                            if crash_dict[s]['times'][j] < J_dict[s]['times'][i]:
                                j += 1
                            else:
                                break

                        cur_phase = convert_times_to_phases(temp_data, J_dict[s]['times'][i])
                        if cur_phase > 0.5 and j >= len(crash_dict[s]['times']) and J_dict[s]['times'][i] < 10**7:
                            continue
                        else:
                            J_array_sustain.append(J_dict[s]['data'][i])
                            J_phase_array_sustain.append(cur_phase + j)
                            valid_J_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_J_points_shot - 1):
                        J_slope_array_sustain.append((J_array_sustain[-(i+1)] - J_array_sustain[-i]) / (J_phase_array_sustain[-(i+1)] - J_phase_array_sustain[-i]))
                        J_phase_slope_array_sustain.append((J_phase_array_sustain[-(i+1)] + J_phase_array_sustain[-i]) / 2)
                        shot_numbers_slope_array_sustain.append(s)
                        
                    unique_shots.append(s)
                
                elif len(crash_dict[s]['times']) in nums_crashes_array:
                    valid_J_points_shot=0
                    for i in range(len(J_dict[s]['data'])):
                        # get phase offset based on how many crashes have occurred
                        j = 0
                        while len(crash_dict[s]['times']) > j:
                            if crash_dict[s]['times'][j] < J_dict[s]['times'][i]:
                                j += 1
                            else:
                                break
                        
                        cur_phase = convert_times_to_phases(temp_data, J_dict[s]['times'][i])
                        if cur_phase > 0.5 and j >= len(crash_dict[s]['times']) and J_dict[s]['times'][i] < 10**7:
                            continue
                        else:
                            J_array_non_sustain.append(J_dict[s]['data'][i])
                            J_phase_array_non_sustain.append(cur_phase + j)
                            valid_J_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_J_points_shot - 1):
                        J_slope_array_non_sustain.append((J_array_non_sustain[-(i+1)] - J_array_non_sustain[-i]) / (J_phase_array_non_sustain[-(i+1)] - J_phase_array_non_sustain[-i]))
                        J_phase_slope_array_non_sustain.append((J_phase_array_non_sustain[-(i+1)] + J_phase_array_non_sustain[-i]) / 2)
                        shot_numbers_slope_array_non_sustain.append(s)
                        
                    unique_shots.append(s)


            pb_pct(cur, tot)
            cur += 1

    # reconstruct thomson temp from slope data
        # get indices of sorted arrays
            # sustain
    J_slope_indices_sorted_by_phase_sustain = np.argsort(J_phase_slope_array_sustain)
    J_slope_array_sustain = [J_slope_array_sustain[i] for i in J_slope_indices_sorted_by_phase_sustain]
    J_phase_slope_array_sustain = [J_phase_slope_array_sustain[i] for i in J_slope_indices_sorted_by_phase_sustain]
    shot_numbers_slope_array_sustain = [shot_numbers_slope_array_sustain[i] for i in J_slope_indices_sorted_by_phase_sustain]
            # non sustain
    J_slope_indices_sorted_by_phase_non_sustain = np.argsort(J_phase_slope_array_non_sustain)
    J_slope_array_non_sustain = [J_slope_array_non_sustain[i] for i in J_slope_indices_sorted_by_phase_non_sustain]
    J_phase_slope_array_non_sustain = [J_phase_slope_array_non_sustain[i] for i in J_slope_indices_sorted_by_phase_non_sustain]
    shot_numbers_slope_array_non_sustain = [shot_numbers_slope_array_non_sustain[i] for i in J_slope_indices_sorted_by_phase_non_sustain]
    
        # get boundaries of bins
            # sustain
    bin_edges_phase_sustain = np.linspace(J_phase_slope_array_sustain[0], J_phase_slope_array_sustain[-1], num_phase_bins + 1)
            # non sustain
    bin_edges_phase_non_sustain = np.linspace(J_phase_slope_array_non_sustain[0], J_phase_slope_array_non_sustain[-1], num_phase_bins + 1)
    
    J_slope_means_sustain = []
    J_slope_means_non_sustain = []
    J_slope_phase_means_sustain = []
    J_slope_phase_means_non_sustain = []
    
    for i in range(len(bin_edges_phase_sustain) - 1):
        # sustain
        J_mean_sustain = median_of_bin(J_slope_array_sustain, J_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        J_slope_means_sustain.append(J_mean_sustain) if J_mean_sustain is not None else None
        J_p_mean_sustain = median_of_bin(J_phase_slope_array_sustain, J_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        J_slope_phase_means_sustain.append(J_p_mean_sustain) if J_p_mean_sustain is not None else None
        # non sustain
        J_mean_non_sustain = median_of_bin(J_slope_array_non_sustain, J_phase_slope_array_non_sustain, bin_edges_phase_non_sustain[i], bin_edges_phase_non_sustain[i+1])
        J_slope_means_non_sustain.append(J_mean_non_sustain) if J_mean_non_sustain is not None else None
        J_p_mean_non_sustain = median_of_bin(J_phase_slope_array_non_sustain, J_phase_slope_array_non_sustain, bin_edges_phase_non_sustain[i], bin_edges_phase_non_sustain[i+1])
        J_slope_phase_means_non_sustain.append(J_p_mean_non_sustain) if J_p_mean_non_sustain is not None else None

        
    # integrate
        # sustain
    J_recon_array_sustain = cumtrapz(J_slope_means_sustain, J_slope_phase_means_sustain, initial=0)
    J_phase_recon_array_sustain = J_slope_phase_means_sustain
        # non sustain
    J_recon_array_non_sustain = cumtrapz(J_slope_means_non_sustain, J_slope_phase_means_non_sustain, initial=0)
    J_phase_recon_array_non_sustain = J_slope_phase_means_non_sustain


    # zero out array
        # sustain
    for i in range(len(J_recon_array_sustain)):
        J_recon_array_sustain[i] = J_recon_array_sustain[i] - min(J_recon_array_sustain)
        
        # non sustain
    for i in range(len(J_recon_array_non_sustain)):
        J_recon_array_non_sustain[i] = J_recon_array_non_sustain[i] - min(J_recon_array_non_sustain)


    # offset array by c
        # sustain
    c = np.nanmean(J_array_sustain) - np.nanmean(J_recon_array_sustain)
    for i in range(len(J_recon_array_sustain)):
        J_recon_array_sustain[i] = J_recon_array_sustain[i] + c
        
        # non sustain
    c = np.nanmean(J_array_non_sustain) - np.nanmean(J_recon_array_non_sustain)
    for i in range(len(J_recon_array_non_sustain)):
        J_recon_array_non_sustain[i] = J_recon_array_non_sustain[i] + c
    
    print(len(J_recon_array_sustain))
    print(len(J_phase_recon_array_sustain))
    
    print(J_recon_array_non_sustain)
    print(J_phase_recon_array_non_sustain)
    
    
    plotly_scatter.make_plotly_multi_scatter([J_phase_slope_array_sustain, J_phase_slope_array_non_sustain],
                                             [J_slope_array_sustain, J_slope_array_non_sustain],
                                             ["dJ/dp of Sustain Shots", "dJ/dp of Non-Sustain Shots"],
                                             ["red", "blue"],
                                             [shot_numbers_slope_array_sustain, shot_numbers_slope_array_non_sustain],
                                             [J_slope_phase_means_sustain, J_slope_phase_means_non_sustain],
                                             [J_slope_means_sustain, J_slope_means_non_sustain],
                                             ["Median of Sustain Shots", "Median of Non-Sustain Shots"],
                                             ["red", "blue"],
                                             f"dJ/dp Over Phase at J{J_psibar}<br>{nums_crashes_array} Crashes\n{len(J_phase_slope_array_sustain) + len(J_phase_slope_array_non_sustain)} Points, {len(unique_shots)} Shots",
                                             "Phase",
                                             "dJ/dp",
                                             f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/J/dJ_dp_recon_J{J_psibar}_without_last_half_cycle_{nums_crashes_array[0]}-{nums_crashes_array[-1]}_crashes.html",
                                             show_plot=show_plotly)
    
    plotly_scatter.make_plotly_multi_scatter([],
                                             [],
                                             [],
                                             [],
                                             [],
                                             [J_phase_recon_array_sustain, J_phase_recon_array_non_sustain],
                                             [J_recon_array_sustain, J_recon_array_non_sustain],
                                             ["J of Sustain Shots", "J of Non-Sustain Shots"],
                                             ["red", "blue"],
                                             f"J{J_psibar} Value Over Phase<br>Comparing Sustain and Non-Sustain for {nums_crashes_array} Crashes\n{len(J_phase_array_sustain) + len(J_phase_array_non_sustain)} Points, {len(unique_shots)} Shots",
                                             "Phase",
                                             "J [A/m^2]",
                                             f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/J/J_phase_recon_J{J_psibar}_without_last_half_cycle_{nums_crashes_array[0]}-{nums_crashes_array[-1]}_crashes.html",
                                             show_plot=show_plotly)
        
    return


