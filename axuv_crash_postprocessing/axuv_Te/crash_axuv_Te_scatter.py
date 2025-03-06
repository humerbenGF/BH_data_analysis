# import libraries
#################################################################
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.integrate import cumtrapz
import numpy as np
import os
import matplotlib.colors as mcolors
from matplotlib.colors import Normalize
import plotly.graph_objects as go
import scipy.signal as sig



# import personal files
#################################################################
import load_save_data.load_data as load_data
import load_save_data.save_data as save_data
import cursors.scatter_cursors as cursor
import cursors.add_click_action as click
import printouts.progress_bar as prog_bar
from axuv_crash_postprocessing.axuv_Te.crash_axuv_Te_scatter_helper import *
import signal_processing.signal_processing as sig_proc


def dT_crash_amp_over_crashes(crash_info_dir, min_number_crashes, matplotlib=True, plotly=False):
    # check the formatting of the crash info dir string
    if crash_info_dir[-1] != "/":
        crash_info_dir += "/"
    
    # load in crash dict
    crash_dict = load_data.load_json_file(f"{crash_info_dir}crash_info_with_hardware_error.json")
    
    # load in shots since lithium
    ss_li_dict = load_data.load_json_file("machine_settings_and_state/shots_since_li/shots_since_li.json")
    
    crash_dt_dict_filename = 'axuv_crash_postprocessing/axuv_Te/crash_dt_Te_info.json'
    if os.path.isfile(crash_dt_dict_filename):
        crash_dt_dict = load_data.load_json_file(crash_dt_dict_filename)
    else:
        crash_dt_dict = {}
    
    crash_amplitudes_list = []
    dT_list = []
    shots_list = []
    ss_li_list = []
    cursor_labels = []
    
    cur = 1
    n = len(crash_dict)
    for s in crash_dict.keys():
        filename = os.environ['AURORA_REPOS'] + "/BH_axuv_Te/axuv_Te_data/" + str(int(int(s) / 1000)*1000) + "/" + "axuv_Te_data_" + str(s) + ".bson"
        if os.path.isfile(filename) and type(crash_dict[s]) != type(str()) and type(ss_li_dict[s]) != type(str()):
            if len(crash_dict[s]['times']) >= min_number_crashes:
                if s not in crash_dt_dict.keys():
                    crash_dt_dict[s] = {"pair1": [], "pair2": [], "pair3": []}
                    # retrieve Te data
                    axuv_Te_data = load_data.load_bson_file(filename)
                    # dt = (axuv_Te_data['axuv_Te_time (ms)'][1] - axuv_Te_data['axuv_Te_time (ms)'][0])
                    # for k in axuv_Te_data.keys():
                    #     if k[:5] == "Mylar":
                    #         axuv_Te_data[k] = sig_proc.low_pass(axuv_Te_data[k], dt, 100*10**3)
                    #         axuv_Te_data[k] = sig.savgol_filter(axuv_Te_data[k], int(1/dt), 3)
                    for i in range(len(crash_dict[s]['times'])):
                        # get indices before and after the crash
                        idx_lhs = find_closest_index(axuv_Te_data['axuv_Te_time (ms)'], crash_dict[s]['pre_crash_times'][i])
                        idx_rhs = find_closest_index(axuv_Te_data['axuv_Te_time (ms)'], crash_dict[s]['post_crash_times'][i])
                        d_index = 20 # int(crash_dict[s]['durations'][i]/dt)
                        
                        # get temp and amplitude change data
                        dT = 0
                        pair_n = 1
                        for k in axuv_Te_data.keys():
                            if k[:5] == "Mylar":
                                if abs(np.mean(axuv_Te_data[k][(idx_lhs-d_index):idx_lhs])) > 500 or abs(np.mean(axuv_Te_data[k][idx_rhs:(idx_rhs+d_index)])) > 500:
                                    dT_temp = np.NaN
                                else:
                                    dT_temp = np.mean(axuv_Te_data[k][(idx_lhs-d_index):idx_lhs]) - np.mean(axuv_Te_data[k][idx_rhs:(idx_rhs+d_index)])
                                
                                if dT_temp > dT:
                                    dT = dT_temp
                            
                                crash_dt_dict[s][f"pair{pair_n}"].append(dT_temp)
                                pair_n += 1
                        
                        amp = crash_dict[s]['amps'][i]
                        
                        crash_amplitudes_list.append(amp)
                        dT_list.append(dT)
                        shots_list.append(s)
                        ss_li_list.append(ss_li_dict[s])
                        cursor_labels.append(f"{s}, {crash_dict[s]['times'][i]}")


                    save_data.save_json(crash_dt_dict_filename, crash_dt_dict)
                
                else:
                    for i in range(len(crash_dict[s]['times'])):
                        dT = crash_dt_dict[s]['pair1'][i]
                        amp = crash_dict[s]['rel_amps'][i]
                        
                        crash_amplitudes_list.append(amp)
                        dT_list.append(dT)
                        shots_list.append(s)
                        ss_li_list.append(ss_li_dict[s])
                        cursor_labels.append(f"{s} {str(crash_dict[s]['times'][i]*1000)[:4]}ms")


        prog_bar.progress_bar_pct_only(cur, n)
        cur += 1
        
    # plot
    if matplotlib:
        # Define a colormap and create a mapping for discrete values
        cmap = plt.cm.jet

        print(dT_list)

        # plot the data
        norm = Normalize(vmin=min(ss_li_list), vmax=max(ss_li_list))
        fig, ax = plt.subplots(figsize=(16,9))
        scatter = plt.scatter(crash_amplitudes_list, dT_list, c=ss_li_list, marker='.', cmap=cmap, norm=norm)
        plt.title(f"Change in Temperature Over Crash Amplitude (Shots with at least {min_number_crashes} Crashes)")
        plt.xlabel("Crash Amplitude")
        plt.ylabel("Change in Te [eV]")
        # plt.ylim(-100, 1000)
        cbar = plt.colorbar(scatter)
        cbar.set_label("Shots Since Lithium Coat")
        plt.grid(True)
                
        cursor.add_cursors_to_scatter(scatter, cursor_labels)
        click.add_click_action_axuv_Te(scatter, fig, shots_list)

        plt.show()
                  
    return
            