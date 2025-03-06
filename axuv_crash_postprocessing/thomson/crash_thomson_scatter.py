# import libraries
#################################################################
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.integrate import cumtrapz
import numpy as np
import mpld3
import plotly.graph_objects as go


# import personal files
#################################################################
import load_save_data.load_data as load_data
import cursors.scatter_cursors as cursor
import cursors.add_click_action as click
import printouts.progress_bar as prog_bar
from axuv_crash_postprocessing.thomson.crash_thomson_scatter_helpers import *
from axuv_crash_postprocessing.thomson.crash_thomson_load_data import *
import axuv_crash_postprocessing.thomson.crash_thomson_data_filters as filter


def reconstruct_temp_change_over_phase_crash_range_sustain_non_sustain(data_dir, thomson_position, num_phase_bins, min_crashes=0, max_crashes=100, matplotlib=True, plotly=False, scatter_plotly=False, max_thomson_temp=700):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict_by_shot = load_thomson_phase_data_by_shot(data_dir, True, True, True, True)
        
    sustainment_dict = load_data.load_json_file("machine_settings_and_state/sustainment/sustainment.json")
    
    
    # plotting arrays
    thomson_temp_array_sustain = []
    thomson_temp_array_non_sustain = []
    thomson_phase_array_sustain = []
    thomson_phase_array_non_sustain = []
    shots_list_sustain = []
    shots_list_non_sustain = []
    
    thomson_temp_slope_array_sustain = []
    thomson_temp_slope_array_non_sustain = []
    thomson_phase_slope_array_sustain = []
    thomson_phase_slope_array_non_sustain = []
    shots_list_slope_sustain = []
    shots_list_slope_non_sustain = []
    
    unique_shots = []
    
    # make arrays of thomson temperature data
    fig, ax = plt.subplots(figsize=(16,9))
    for s in data_dict_by_shot.keys():
        if type(sustainment_dict[s]) != type(str()):
            if sustainment_dict[s] > 0:
                sorted_by_time = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_times"])
                
                if len(sorted_by_time) >= 1 and len(data_dict_by_shot[s]["crash_info"]['times']) >= min_crashes and len(data_dict_by_shot[s]["crash_info"]['times']) <= max_crashes:
                    # make array of all temps
                    valid_thomson_points_shot=0
                    for i in range(len(sorted_by_time)):
                        if data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i]] < max_thomson_temp and data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i]] > 0:
                            thomson_temp_array_sustain.append(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i]])
                            shots_list_sustain.append(s)
                            # get phase offset based on how many crashes have occurred
                            j = 0
                            while len(data_dict_by_shot[s]["crash_info"]['times']) > j:
                                if data_dict_by_shot[s]["crash_info"]['times'][j] < data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[i]]:
                                    j += 1
                                else:
                                    break
                            
                            thomson_phase_array_sustain.append(data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[i]] + j)
                            valid_thomson_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_thomson_points_shot - 1):
                        thomson_temp_slope_array_sustain.append((thomson_temp_array_sustain[-(i+1)] - thomson_temp_array_sustain[-i]) / (thomson_phase_array_sustain[-(i+1)] - thomson_phase_array_sustain[-i]))
                        thomson_phase_slope_array_sustain.append((thomson_phase_array_sustain[-(i+1)] + thomson_phase_array_sustain[-i]) / 2)
                        shots_list_slope_sustain.append(s)
                        
                    unique_shots.append(s)
            
            else:
                sorted_by_time = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_times"])
                
                if len(sorted_by_time) >= 1 and len(data_dict_by_shot[s]["crash_info"]['times']) >= min_crashes and len(data_dict_by_shot[s]["crash_info"]['times']) <= max_crashes:
                    # make array of all temps
                    valid_thomson_points_shot = 0
                    for i in range(len(sorted_by_time)):
                        if data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i]] < max_thomson_temp and data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i]] > 0:
                            thomson_temp_array_non_sustain.append(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i]])
                            shots_list_non_sustain.append(s)
                            # get phase offset based on how many crashes have occurred
                            j = 0
                            while len(data_dict_by_shot[s]["crash_info"]['times']) > j:
                                if data_dict_by_shot[s]["crash_info"]['times'][j] < data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[i]]:
                                    j += 1
                                else:
                                    break
                            
                            thomson_phase_array_non_sustain.append(data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[i]] + j)
                            valid_thomson_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_thomson_points_shot - 1):
                        thomson_temp_slope_array_non_sustain.append((thomson_temp_array_non_sustain[-(i+1)] - thomson_temp_array_non_sustain[-i]) / (thomson_phase_array_non_sustain[-(i+1)] - thomson_phase_array_non_sustain[-i]))
                        thomson_phase_slope_array_non_sustain.append((thomson_phase_array_non_sustain[-(i+1)] + thomson_phase_array_non_sustain[-i]) / 2)
                        shots_list_slope_non_sustain.append(s)
                        
                    unique_shots.append(s)
                        
    # reconstruct thomson temp from slope data
        # get indices of sorted arrays
            # sustain
    thomson_slope_indices_sorted_by_phase_sustain = np.argsort(thomson_phase_slope_array_sustain)
    thomson_temp_slope_array_sustain = [thomson_temp_slope_array_sustain[i] for i in thomson_slope_indices_sorted_by_phase_sustain]
    thomson_phase_slope_array_sustain = [thomson_phase_slope_array_sustain[i] for i in thomson_slope_indices_sorted_by_phase_sustain]
    shots_list_slope_sustain = [shots_list_slope_sustain[i] for i in thomson_slope_indices_sorted_by_phase_sustain]

            # non sustain
    thomson_slope_indices_sorted_by_phase_non_sustain = np.argsort(thomson_phase_slope_array_non_sustain)
    thomson_temp_slope_array_non_sustain = [thomson_temp_slope_array_non_sustain[i] for i in thomson_slope_indices_sorted_by_phase_non_sustain]
    thomson_phase_slope_array_non_sustain = [thomson_phase_slope_array_non_sustain[i] for i in thomson_slope_indices_sorted_by_phase_non_sustain]
    shots_list_slope_non_sustain = [shots_list_slope_non_sustain[i] for i in thomson_slope_indices_sorted_by_phase_sustain]

    
    
        # get boundaries of bins
            # sustain
    bin_edges_phase_sustain = np.linspace(thomson_phase_slope_array_sustain[0], thomson_phase_slope_array_sustain[-1], num_phase_bins + 1)
            # non sustain
    bin_edges_phase_non_sustain = np.linspace(thomson_phase_slope_array_non_sustain[0], thomson_phase_slope_array_non_sustain[-1], num_phase_bins + 1)
    
    thomson_slope_temp_means_sustain = []
    thomson_slope_temp_means_non_sustain = []
    thomson_slope_phase_means_sustain = []
    thomson_slope_phase_means_non_sustain = []
    
    for i in range(len(bin_edges_phase_sustain) - 1):
        # sustain
        t_s_t_mean_sustain = median_of_bin(thomson_temp_slope_array_sustain, thomson_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        thomson_slope_temp_means_sustain.append(t_s_t_mean_sustain) if t_s_t_mean_sustain is not None else None
        t_s_p_mean_sustain = median_of_bin(thomson_phase_slope_array_sustain, thomson_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        thomson_slope_phase_means_sustain.append(t_s_p_mean_sustain) if t_s_p_mean_sustain is not None else None
        # non sustain
        t_s_t_mean_non_sustain = median_of_bin(thomson_temp_slope_array_non_sustain, thomson_phase_slope_array_non_sustain, bin_edges_phase_non_sustain[i], bin_edges_phase_non_sustain[i+1])
        thomson_slope_temp_means_non_sustain.append(t_s_t_mean_non_sustain) if t_s_t_mean_non_sustain is not None else None
        t_s_p_mean = median_of_bin(thomson_phase_slope_array_non_sustain, thomson_phase_slope_array_non_sustain, bin_edges_phase_non_sustain[i], bin_edges_phase_non_sustain[i+1])
        thomson_slope_phase_means_non_sustain.append(t_s_p_mean) if t_s_p_mean is not None else None
        
    # integrate
        # sustain
    thomson_temp_recon_array_sustain = cumtrapz(thomson_slope_temp_means_sustain, thomson_slope_phase_means_sustain, initial=0)
    thomson_phase_recon_array_sustain = thomson_slope_phase_means_sustain
        # non sustain
    thomson_temp_recon_array_non_sustain = cumtrapz(thomson_slope_temp_means_non_sustain, thomson_slope_phase_means_non_sustain, initial=0)
    thomson_phase_recon_array_non_sustain = thomson_slope_phase_means_non_sustain

    # zero out array
        # sustain
    for i in range(len(thomson_temp_recon_array_sustain)):
        thomson_temp_recon_array_sustain[i] = thomson_temp_recon_array_sustain[i] - min(thomson_temp_recon_array_sustain)
        
        # non sustain
    for i in range(len(thomson_temp_recon_array_non_sustain)):
        thomson_temp_recon_array_non_sustain[i] = thomson_temp_recon_array_non_sustain[i] - min(thomson_temp_recon_array_non_sustain)

    # offset array by c
        # sustain
    c = np.mean(thomson_temp_array_sustain) - np.mean(thomson_temp_recon_array_sustain)
    for i in range(len(thomson_temp_recon_array_sustain)):
        thomson_temp_recon_array_sustain[i] = thomson_temp_recon_array_sustain[i] + c
        
        # non sustain
    c = np.mean(thomson_temp_array_non_sustain) - np.mean(thomson_temp_recon_array_non_sustain)
    for i in range(len(thomson_temp_recon_array_non_sustain)):
        thomson_temp_recon_array_non_sustain[i] = thomson_temp_recon_array_non_sustain[i] + c


    if matplotlib:
        # Plots of Temperature over Phase
        #######################################################################################################

        # scatter of the thomson slope over phase data
            # scatter
        plt.scatter(thomson_phase_slope_array_sustain, thomson_temp_slope_array_sustain, color='r', marker='.', alpha=0.3, label=r"\frac{dT}{dp} of Sustain Shots")
        plt.scatter(thomson_phase_slope_array_non_sustain, thomson_temp_slope_array_non_sustain, color='b', marker='.', alpha=0.3, label=r"\frac{dT}{dp} of Non-Sustain Shots")
            # lines
        plt.plot(thomson_slope_phase_means_sustain, thomson_slope_temp_means_sustain, color='r', label='Median of Sustain Shots')
        plt.plot(thomson_slope_phase_means_non_sustain, thomson_slope_temp_means_non_sustain, color='b', label='Median of Non-Sustain Shots')
        plt.title(r"$\frac{dT}{dp}$ Over Phase" + f" TS{thomson_position}\n{min_crashes}-{max_crashes} Crashes // {len(thomson_phase_slope_array_sustain)+len(thomson_phase_slope_array_non_sustain)} Points")
        plt.xlabel("Phase")
        plt.ylabel(r"$\frac{dT}{dp}$")
        plt.grid(True)
        plt.legend()
        plt.show()
        
        # scatter of the reconstructed thomson slope over phase data
        plt.plot(thomson_phase_recon_array_sustain, thomson_temp_recon_array_sustain, color='r', label='Sustain')
        plt.plot(thomson_phase_recon_array_non_sustain, thomson_temp_recon_array_non_sustain, color='b', label='Non-Sustain')
        plt.title(f"Temperature Over Phase TS{thomson_position}\nComparing Sustain and Non-Sustain for {min_crashes}-{max_crashes} Crashes")
        plt.xlabel("Phase")
        plt.ylabel("Temperature")
        plt.grid(True)
        plt.legend()
        plt.show()
    
    if plotly:
        # Scatter of the Thomson slope over phase data
        fig1 = go.Figure()

        # Add sustain scatter points
        fig1.add_trace(go.Scatter(
            x=thomson_phase_slope_array_sustain,
            y=thomson_temp_slope_array_sustain,
            mode='markers',
            marker=dict(color='red', opacity=0.3),
            name="Sustain Shots",
            text=shots_list_slope_sustain
        ))

        # Add non-sustain scatter points
        fig1.add_trace(go.Scatter(
            x=thomson_phase_slope_array_non_sustain,
            y=thomson_temp_slope_array_non_sustain,
            mode='markers',
            marker=dict(color='blue', opacity=0.3),
            name="Non-Sustain Shots",
            text=shots_list_slope_non_sustain
        ))

        # Add sustain median line
        fig1.add_trace(go.Scatter(
            x=thomson_slope_phase_means_sustain,
            y=thomson_slope_temp_means_sustain,
            mode='lines',
            line=dict(color='red'),
            name="Median of Sustain Shots"
        ))

        # Add non-sustain median line
        fig1.add_trace(go.Scatter(
            x=thomson_slope_phase_means_non_sustain,
            y=thomson_slope_temp_means_non_sustain,
            mode='lines',
            line=dict(color='blue'),
            name="Median of Non-Sustain Shots"
        ))

        # Layout settings for the first plot
        fig1.update_layout(
            title=f"dT/dp Over Phase TS{thomson_position}<br>{min_crashes}-{max_crashes} Crashes\n{len(unique_shots)} Shots",
            xaxis=dict(
                title="Phase",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(
                title="dT/dp",
                showgrid=True,  # Enable grid lines for the y-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            legend=dict(title="Legend"),
            template="simple_white"
            )

        # Show the first plot
        fig1.show()
        fig1.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/recon_thomson/dTdP_over_phase_ts{thomson_position}_sustain_non_sustain.html")

        # Scatter of the reconstructed Thomson slope over phase data
        fig2 = go.Figure()

        if scatter_plotly:
            # Add sustain scatter
            fig2.add_trace(go.Scatter(
                x=thomson_phase_array_sustain,
                y=thomson_temp_array_sustain,
                mode='markers',
                marker=dict(color='red', opacity=0.3),
                name="Sustain",
                text=shots_list_sustain
            ))

            # Add non-sustain scatter
            fig2.add_trace(go.Scatter(
                x=thomson_phase_array_non_sustain,
                y=thomson_temp_array_non_sustain,
                mode='markers',
                marker=dict(color='blue', opacity=0.3),
                name="Non-Sustain",
                text=shots_list_non_sustain
            ))

        # Add sustain line
        fig2.add_trace(go.Scatter(
            x=thomson_phase_recon_array_sustain,
            y=thomson_temp_recon_array_sustain,
            mode='lines',
            line=dict(color='red'),
            name="Sustain"
        ))

        # Add non-sustain line
        fig2.add_trace(go.Scatter(
            x=thomson_phase_recon_array_non_sustain,
            y=thomson_temp_recon_array_non_sustain,
            mode='lines',
            line=dict(color='blue'),
            name="Non-Sustain"
        ))

        # Layout settings for the second plot
        fig2.update_layout(
            title=f"Temperature Over Phase TS{thomson_position}<br>Comparing Sustain and Non-Sustain for {min_crashes}-{max_crashes} Crashes\n{len(unique_shots)} Shots",
                        xaxis=dict(
                title="Phase",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(
                title="Temperature",
                showgrid=True,  # Enable grid lines for the y-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            legend=dict(title="Legend"),
            template="simple_white"
            )

        # Show the second plot
        fig2.show()
        fig2.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/recon_thomson/T_over_phase_ts{thomson_position}_sustain_non_sustain.html")

    
    return




def reconstruct_temp_change_over_phase_single_num_crashes(data_dir, thomson_position, num_phase_bins, num_time_bins, num_crashes=0, matplotlib=True, plotly=False, show_plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict_by_shot = load_thomson_phase_data_by_shot(data_dir, True, True, True, True)
    
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    # plotting arrays
    thomson_temp_array = []
    thomson_phase_array = []
    thomson_time_array = []
    shot_labels_array = []
    
    thomson_temp_slope_array = []
    thomson_phase_slope_array = []
    shot_labels_slopes_array = []

    thomson_temp_recon_array = []
    thomson_phase_recon_array = []
    
    unique_shots = []
    
    # make arrays of thomson temperature data
    fig, ax = plt.subplots(figsize=(16,9))
    for s in data_dict_by_shot.keys():
        if s in lifetimes_dict.keys():
            if type(lifetimes_dict[s]) != type(str()):
                sorted_by_time = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_times"])
                
                if len(sorted_by_time) >= 1 and len(data_dict_by_shot[s]["crash_info"]['times']) == num_crashes:
                    # make array of all temps
                    for i in range(len(sorted_by_time)):
                        thomson_temp_array.append(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i]])
                        thomson_time_array.append(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[i]])
                        shot_labels_array.append(s)
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
                        shot_labels_slopes_array.append(s)
                        
                unique_shots.append(s)
                
    # reconstruct thomson temp from slope data
        # get indices of sorted arrays
    thomson_slope_indices_sorted_by_phase = np.argsort(thomson_phase_slope_array)
    thomson_temp_slope_array = [thomson_temp_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    thomson_phase_slope_array = [thomson_phase_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    shot_labels_slopes_array = [shot_labels_slopes_array[i] for i in thomson_slope_indices_sorted_by_phase]
    
        # get boundaries of bins
    bin_edges_phase = np.linspace(thomson_phase_slope_array[0], thomson_phase_slope_array[-1], num_phase_bins + 1)
    
    thomson_slope_temp_means = []
    thomson_slope_phase_means = []
    
    
    for i in range(len(bin_edges_phase) - 1):
        # handle phase
        t_s_t_mean = median_of_bin(thomson_temp_slope_array, thomson_phase_slope_array, bin_edges_phase[i], bin_edges_phase[i+1])
        thomson_slope_temp_means.append(t_s_t_mean) if t_s_t_mean is not None else None
        t_s_p_mean = median_of_bin(thomson_phase_slope_array, thomson_phase_slope_array, bin_edges_phase[i], bin_edges_phase[i+1])
        thomson_slope_phase_means.append(t_s_p_mean) if t_s_p_mean is not None else None
        
    # integrate
    thomson_temp_recon_array = cumtrapz(thomson_slope_temp_means, thomson_slope_phase_means, initial=0)
    thomson_phase_recon_array = thomson_slope_phase_means

    # zero out array
    for i in range(len(thomson_temp_recon_array)):
        thomson_temp_recon_array[i] = thomson_temp_recon_array[i] - min(thomson_temp_recon_array)

    # offset array by c
    c = np.mean(thomson_temp_array) - np.mean(thomson_temp_recon_array)
    for i in range(len(thomson_temp_recon_array)):
        thomson_temp_recon_array[i] = thomson_temp_recon_array[i] + c


    if matplotlib:
        # Plots of Temperature over Phase
        #######################################################################################################

        # scatter of the thomson slope over phase data
        plt.scatter(thomson_phase_slope_array, thomson_temp_slope_array, color='k', marker='.')
        plt.plot(thomson_slope_phase_means, thomson_slope_temp_means, color='r')
        plt.title(r"$\frac{dT}{dp}$ Over Phase" + f" TS{thomson_position}\n{num_crashes} Crashes // {len(thomson_phase_slope_array)} Shots")
        plt.xlabel("Phase")
        plt.ylabel(r"$\frac{dT}{dp}$")
        plt.grid(True)
        plt.show()
        
        # scatter of the reconstructed thomson slope over phase data
        # plt.scatter(thomson_phase_array, thomson_temp_array, color='k', marker='.')
        plt.plot(thomson_phase_recon_array, thomson_temp_recon_array, color='r')
        plt.title(f"Temperature Over Phase TS{thomson_position}\n{num_crashes} Crashes")
        plt.xlabel("Phase")
        plt.ylabel("Temperature")
        plt.grid(True)
        plt.show()
        
    
    if plotly:
        # Plots of Temperature over Phase
        #######################################################################################################

        # Scatter of the Thomson slope over phase data
        scatter_phase_slope = go.Scatter(x=thomson_phase_slope_array, 
                                        y=thomson_temp_slope_array, 
                                        mode='markers', 
                                        marker=dict(color='black'),
                                        name='Slope Data',
                                        text=shot_labels_slopes_array)

        # Line of the mean values for the Thomson slope
        line_slope_phase = go.Scatter(x=thomson_slope_phase_means, 
                                    y=thomson_slope_temp_means, 
                                    mode='lines', 
                                    line=dict(color='red'),
                                    name='Mean Slope')

        # Create layout for the phase plot
        layout_phase = go.Layout(title=r"dT/dp Over Phase" + f" {num_crashes} Crashes\nTS{thomson_position} // {len(thomson_phase_slope_array)} Points, {len(unique_shots)} Shots",
                                xaxis=dict(title='Phase'),
                                yaxis=dict(title="dt/dp"),
                                showlegend=True,
                                template='plotly_white')

        # Create the figure and plot the phase data
        fig_phase = go.Figure(data=[scatter_phase_slope, line_slope_phase], layout=layout_phase)
        fig_phase.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/recon_thomson/dtdP_over_phase_ts{thomson_position}_{num_crashes}crash.html")
        if show_plotly:
            fig_phase.show()

        # scatter of raw thomson temperature
        scatter_phase = go.Scatter(x=thomson_phase_array, 
                                        y=thomson_temp_array, 
                                        mode='markers', 
                                        marker=dict(color='black'),
                                        name='Temperature Data',
                                        text=shot_labels_array)

        # Scatter of the reconstructed Thomson slope over phase data
        recon_line_phase = go.Scatter(x=thomson_phase_recon_array, 
                                    y=thomson_temp_recon_array, 
                                    mode='lines', 
                                    line=dict(color='red'),
                                    name='Reconstructed')

        # Create layout for the phase recon plot
        layout_recon_phase = go.Layout(title=f"Temperature Over Phase {num_crashes} Crashes\nTS{thomson_position} // {len(thomson_phase_array)} Points, {len(unique_shots)} Shots",
                                    xaxis=dict(title='Phase'),
                                    yaxis=dict(title='Temperature'),
                                    showlegend=True,
                                    template='plotly_white')

        # Create the figure and plot the phase recon data
        fig_recon_phase = go.Figure(data=[scatter_phase, recon_line_phase], layout=layout_recon_phase)
        fig_recon_phase.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/recon_thomson/T_over_phase_ts{thomson_position}_{num_crashes}crash.html")
        if show_plotly:
            fig_recon_phase.show()

    
    return



def reconstruct_temp_change_over_phase(data_dir, thomson_position, num_phase_bins, num_time_bins, min_num_crashes=0, matplotlib=True, plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict_by_shot = load_thomson_phase_data_by_shot(data_dir, True, True, True, True)
    
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    # plotting arrays
    thomson_temp_array = []
    thomson_phase_array = []
    thomson_time_array = []
    shot_labels_array = []
    
    thomson_temp_slope_array = []
    thomson_phase_slope_array = []
    shot_labels_slope_array = []
    
    thomson_temp_slope_array_time = []
    thomson_time_slope_array = []

    thomson_temp_recon_array = []
    thomson_phase_recon_array = []
    thomson_time_recon_array = []
    
    unique_shots = []
    
    # make arrays of thomson temperature data
    fig, ax = plt.subplots(figsize=(16,9))
    for s in data_dict_by_shot.keys():
        if s in lifetimes_dict.keys():
            if type(lifetimes_dict[s]) != type(str()):
                sorted_by_time = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_times"])
                
                if len(sorted_by_time) >= 1 and len(data_dict_by_shot[s]["crash_info"]['times']) >= min_num_crashes:
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
                        shot_labels_array.append(s)
                        
                    # make array of all slopes
                    for i in range(len(sorted_by_time) - 1):
                        thomson_temp_slope_array.append((thomson_temp_array[-(i+1)] - thomson_temp_array[-i]) / (thomson_phase_array[-(i+1)] - thomson_phase_array[-i]))
                        thomson_phase_slope_array.append((thomson_phase_array[-(i+1)] + thomson_phase_array[-i]) / 2)
                        thomson_temp_slope_array_time.append((thomson_temp_array[-(i+1)] - thomson_temp_array[-i]) / (thomson_time_array[-(i+1)] - thomson_time_array[-i]))
                        thomson_time_slope_array.append((thomson_time_array[-(i+1)] + thomson_time_array[-i]) / 2)
                        shot_labels_slope_array.append(s)
                        
                    unique_shots.append(s)
                    
    # reconstruct thomson temp from slope data
        # get indices of sorted arrays
    thomson_slope_indices_sorted_by_phase = np.argsort(thomson_phase_slope_array)
    thomson_temp_slope_array = [thomson_temp_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    thomson_phase_slope_array = [thomson_phase_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    shot_labels_slope_array = [shot_labels_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    
    thomson_slope_indices_sorted_by_time = np.argsort(thomson_time_slope_array)
    thomson_temp_slope_array_time = [thomson_temp_slope_array_time[i] for i in thomson_slope_indices_sorted_by_time]
    thomson_time_slope_array = [thomson_time_slope_array[i] for i in thomson_slope_indices_sorted_by_time]
    shot_labels_slope_array = [shot_labels_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    
        # get boundaries of bins
    bin_edges_phase = np.linspace(thomson_phase_slope_array[0], thomson_phase_slope_array[-1], num_phase_bins + 1)
    bin_edges_times = np.linspace(0.9*thomson_time_slope_array[0], thomson_time_slope_array[-1]*1.1, num_time_bins + 1)
    
    thomson_slope_temp_means = []
    thomson_slope_phase_means = []
    
    thomson_slope_temp_means_ts = []
    thomson_slope_time_means = []
    
    for i in range(len(bin_edges_phase) - 1):
        # handle phase
        t_s_t_mean = median_of_bin(thomson_temp_slope_array, thomson_phase_slope_array, bin_edges_phase[i], bin_edges_phase[i+1])
        thomson_slope_temp_means.append(t_s_t_mean) if t_s_t_mean is not None else None
        t_s_p_mean = median_of_bin(thomson_phase_slope_array, thomson_phase_slope_array, bin_edges_phase[i], bin_edges_phase[i+1])
        thomson_slope_phase_means.append(t_s_p_mean) if t_s_p_mean is not None else None

    for i in range(len(bin_edges_times) - 1):
        # handle time
        t_s_t_mean = median_of_bin(thomson_temp_slope_array_time, thomson_time_slope_array, bin_edges_times[i], bin_edges_times[i+1])
        thomson_slope_temp_means_ts.append(t_s_t_mean) if t_s_t_mean is not None else None
        t_s_tm_mean = median_of_bin(thomson_time_slope_array, thomson_time_slope_array, bin_edges_times[i], bin_edges_times[i+1])
        thomson_slope_time_means.append(t_s_tm_mean) if t_s_tm_mean is not None else None
        
    # integrate
    thomson_temp_recon_array = cumtrapz(thomson_slope_temp_means, thomson_slope_phase_means, initial=0)
    thomson_phase_recon_array = thomson_slope_phase_means
    thomson_temp_recon_array_ts = cumtrapz(thomson_slope_temp_means_ts, thomson_slope_time_means, initial=0)
    thomson_time_recon_array = thomson_slope_time_means

    # zero out temperatures
    for i in range(len(thomson_temp_recon_array)):
        thomson_temp_recon_array[i] = thomson_temp_recon_array[i] - min(thomson_temp_recon_array)

    # offset array by c
    c = np.mean(thomson_temp_array) - np.mean(thomson_temp_recon_array)
    for i in range(len(thomson_temp_recon_array)):
        thomson_temp_recon_array[i] = thomson_temp_recon_array[i] + c
        
    
    for i in range(len(thomson_temp_recon_array_ts)):
        thomson_temp_recon_array_ts[i] = thomson_temp_recon_array_ts[i] - min(thomson_temp_recon_array_ts)


    if matplotlib:
        # Plots of Temperature over Phase
        #######################################################################################################

        # scatter of the thomson slope over phase data
        plt.scatter(thomson_phase_slope_array, thomson_temp_slope_array, color='k', marker='.')
        plt.plot(thomson_slope_phase_means, thomson_slope_temp_means, color='r')
        plt.title(r"$\frac{dT}{dp}$ Over Phase" + f" TS{thomson_position} // {len(thomson_phase_slope_array)} Points")
        plt.xlabel("Phase")
        plt.ylabel(r"$\frac{dT}{dp}$")
        plt.grid(True)
        plt.show()
        
        # scatter of the reconstructed thomson slope over phase data
        # plt.scatter(thomson_phase_array, thomson_temp_array, color='k', marker='.')
        plt.plot(thomson_phase_recon_array, thomson_temp_recon_array, color='r')
        plt.title(f"Temperature Over Phase TS{thomson_position}")
        plt.xlabel("Phase")
        plt.ylabel("Temperature")
        plt.grid(True)
        plt.show()
        
        
        # Plots of Temperature over Time
        #######################################################################################################

        # scatter of the thomson slope over phase data
        plt.scatter(thomson_time_slope_array, thomson_temp_slope_array_time, color='k', marker='.')
        plt.plot(thomson_slope_time_means, thomson_slope_temp_means_ts, color='r')
        plt.title(r"$\frac{dT}{dt}$ Over Time" + f" TS{thomson_position}")
        plt.xlabel("Time")
        plt.ylabel(r"$\frac{dT}{dt}$")
        plt.grid(True)
        plt.show()
        
        # scatter of the reconstructed thomson slope over phase data
        # plt.scatter(thomson_phase_array, thomson_temp_array, color='k', marker='.')
        plt.plot(thomson_time_recon_array, thomson_temp_recon_array_ts, color='r')
        plt.title("Temperature Over Time" + f" TS{thomson_position}")
        plt.xlabel("Time")
        plt.ylabel("Temperature")
        plt.grid(True)
        plt.show()
    
    if plotly:
        # Plots of Temperature over Phase
        #######################################################################################################

        # Scatter of the Thomson slope over phase data
        scatter_phase_slope = go.Scatter(x=thomson_phase_slope_array, 
                                        y=thomson_temp_slope_array, 
                                        mode='markers', 
                                        marker=dict(color='black'),
                                        name='Slope Data',
                                        text=shot_labels_slope_array)

        # Line of the mean values for the Thomson slope
        line_slope_phase = go.Scatter(x=thomson_slope_phase_means, 
                                    y=thomson_slope_temp_means, 
                                    mode='lines', 
                                    line=dict(color='red'),
                                    name='Mean Slope')

        # Create layout for the phase plot
        layout_phase = go.Layout(title=r"dT/dp Over Phase" + f"\nTS{thomson_position} // {len(thomson_slope_phase_means)} Points, {len(unique_shots)} Shots",
                                xaxis=dict(title='Phase'),
                                yaxis=dict(title="dt/dp"),
                                showlegend=True,
                                template='plotly_white')

        # Create the figure and plot the phase data
        fig_phase = go.Figure(data=[scatter_phase_slope, line_slope_phase], layout=layout_phase)
        fig_phase.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/recon_thomson/dtdP_over_phase_ts{thomson_position}.html")
        fig_phase.show()

        # scatter of 
        scatter_phase= go.Scatter(x=thomson_phase_array, 
                                        y=thomson_temp_array, 
                                        mode='markers', 
                                        marker=dict(color='black'),
                                        name='Temperature Data',
                                        text=shot_labels_array)

        # Scatter of the reconstructed Thomson slope over phase data
        recon_line_phase = go.Scatter(x=thomson_phase_recon_array, 
                                    y=thomson_temp_recon_array, 
                                    mode='lines', 
                                    line=dict(color='red'),
                                    name='Reconstructed')

        # Create layout for the phase recon plot
        layout_recon_phase = go.Layout(title=f"Temperature Over Phase\nTS{thomson_position} // {len(thomson_phase_recon_array)} Points, {len(unique_shots)} Shots",
                                    xaxis=dict(title='Phase'),
                                    yaxis=dict(title='Temperature'),
                                    showlegend=True,
                                    template='plotly_white')

        # Create the figure and plot the phase recon data
        fig_recon_phase = go.Figure(data=[scatter_phase, recon_line_phase], layout=layout_recon_phase)
        fig_recon_phase.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/recon_thomson/T_over_phase_ts{thomson_position}.html")
        fig_recon_phase.show()

    return


def plot_temp_phase_for_shotlist_going_over_crashes(data_dir, thomson_position, Tmin=200, multitime_only=False, showplots=True):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict_by_shot = load_thomson_phase_data_by_shot(data_dir, True, True, True, True)
    
    temp_phase_slope_dict = filter.get_slope_at_phase_by_shot(data_dict_by_shot, thomson_position, 0.4, False)
    
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    crash_phase_array = []
    thomson_psibar_array = []
    thomson_temp_array = []
    shot_labels = []
    shot_ints = []
    unique_included_shots = []
    
    fig, ax = plt.subplots(figsize=(16,9))
    for s in temp_phase_slope_dict.keys():
        if s in lifetimes_dict.keys():
            if type(lifetimes_dict[s]) != type(str()):
                sorted_by_time = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_times"])
                # initialize starting values
                phs_next = data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[0]]
                temp_next = data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[0]]
                sht_next_data = (f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][0]}s")
                t_next = data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[0]]
                # initialize arrays that will be appended to the scatter plot arrays
                phs = [phs_next]
                pbs = [get_thomson_psibar_value(t_next, data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"])]
                tmps = [temp_next]
                shts = [sht_next_data]
                sht_ints = [int(s)]
                
                # only include shots that pass over a crash
                if len(data_dict_by_shot[s]["crash_info"]['times']) > 0:
                    if max(data_dict_by_shot[s][f"thomson_{thomson_position}_times"]) < min(data_dict_by_shot[s]["crash_info"]['times']):
                        continue
                else:
                    continue
                
                # only include shots with multitime thomson
                if multitime_only:
                    if len(data_dict_by_shot[s][f"thomson_{thomson_position}_times"]) < 2:
                        continue
                
                for i in range(len(sorted_by_time) - 1):
                    if int(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i+1]*1000) > (len(data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"])-1) or Tmin > max(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"]):
                        continue
                    else:
                        # print(f"Thomson Time: {data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i]*1000}ms // Available Recon Data {len(data_dict_by_shot[s][f'thomson_{thomson_position}_psibars'])}ms")
                        t_cur = t_next
                        t_next = data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[i+1]]
                        crash_in_between = False
                        for t in data_dict_by_shot[s]["crash_info"]['times']:
                            if t_cur < t and t < t_next:
                                crash_in_between=True
                        
                        # initialize plotting values
                        phs_cur = phs_next
                        temp_cur = temp_next
                        temp_next = data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i+1]]
                        sht_next_data = (f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i+1]}s")

                                                
                        if crash_in_between:
                            phs_next = data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[i+1]] + (int(phs_cur) + 1)
                            plt.plot([phs_cur, phs_next], [temp_cur, temp_next], linewidth=0.5, color='r')
                        
                        else:
                            phs_next = data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[i+1]] + int(phs_cur)
                            plt.plot([phs_cur, phs_next], [temp_cur, temp_next], linewidth=0.25, color='b')
                        
                        phs.append(phs_next)
                        pbs.append(get_thomson_psibar_value(t_next, data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]))
                        tmps.append(temp_next)
                        shts.append(sht_next_data)
                        sht_ints.append(int(s))
                        if s not in unique_included_shots:
                            unique_included_shots.append(s)
                            
                # append minor arrays to scatter plot arrays
                crash_phase_array += phs
                thomson_psibar_array += pbs
                thomson_temp_array += tmps
                shot_labels += shts
                shot_ints += sht_ints


    print("crash_phase_array:", len(crash_phase_array))
    print("thomson_temp_array:", len(thomson_temp_array))
    print("thomson_psibar_array:", len(thomson_psibar_array))
    
    scatter = plt.scatter(crash_phase_array, thomson_temp_array, c=thomson_psibar_array, cmap='jet_r', marker='.', picker=True, )
    plt.colorbar(label="Normalized Psi")
    cursor.add_cursors_to_scatter(scatter, shot_labels)
    plt.title(f"Temperature over Phase Coloured by Normalized Psi\nTS{thomson_position}, {len(unique_included_shots)} Unique Shots")
    plt.ylabel("Thomson Temperature [eV]")
    plt.xlabel("Phase")
    click.add_click_action_timeseries_plots(data_dir, scatter, fig, shot_ints)
    
    plt.show()
    
    return


import plotly.graph_objects as go
import numpy as np

def plot_temp_phase_for_shotlist_going_over_crashes_plotly(data_dir, thomson_position, Tmin=200, multitime_only=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict_by_shot = load_thomson_phase_data_by_shot(data_dir, True, True, True, True)
    
    temp_phase_slope_dict = filter.get_slope_at_phase_by_shot(data_dict_by_shot, thomson_position, 0.4, False)
    
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    crash_phase_array = []
    thomson_psibar_array = []
    thomson_temp_array = []
    shot_labels = []
    shot_ints = []
    unique_included_shots = []
    lines = []

    for s in temp_phase_slope_dict.keys():
        if s in lifetimes_dict.keys():
            if type(lifetimes_dict[s]) != type(str()):
                sorted_by_time = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_times"])
                # initialize starting values
                phs_next = data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[0]]
                temp_next = data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[0]]
                sht_next_data = (f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][0]}s")
                t_next = data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[0]]
                # initialize arrays that will be appended to the scatter plot arrays
                phs = [phs_next]
                pbs = [get_thomson_psibar_value(t_next, data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"])]
                tmps = [temp_next]
                shts = [sht_next_data]
                sht_ints = [int(s)]
                
                # only include shots that pass over a crash
                if len(data_dict_by_shot[s]["crash_info"]['times']) > 0:
                    if max(data_dict_by_shot[s][f"thomson_{thomson_position}_times"]) < min(data_dict_by_shot[s]["crash_info"]['times']):
                        continue
                else:
                    continue
                
                # only include shots with multitime thomson
                if multitime_only:
                    if len(data_dict_by_shot[s][f"thomson_{thomson_position}_times"]) < 2:
                        continue
                
                for i in range(len(sorted_by_time) - 1):
                    if int(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i+1]*1000) > (len(data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"])-1) or Tmin > max(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"]):
                        continue
                    else:
                        # print(f"Thomson Time: {data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i]*1000}ms // Available Recon Data {len(data_dict_by_shot[s][f'thomson_{thomson_position}_psibars'])}ms")
                        t_cur = t_next
                        t_next = data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[i+1]]
                        crash_in_between = False
                        for t in data_dict_by_shot[s]["crash_info"]['times']:
                            if t_cur < t and t < t_next:
                                crash_in_between=True
                        
                        # initialize plotting values
                        phs_cur = phs_next
                        temp_cur = temp_next
                        temp_next = data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i+1]]
                        sht_next_data = (f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i+1]}s")

                                                  
                        if crash_in_between:
                            phs_next = data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[i+1]] + (int(phs_cur) + 1)
                            lines.append(go.Scatter(
                                x=[phs_cur, phs_next],
                                y=[temp_cur, temp_next],
                                mode='lines',
                                line=dict(color='red', width=0.5),
                                showlegend=False
                            ))
                        
                        else:
                            phs_next = data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[i+1]] + int(phs_cur)
                            lines.append(go.Scatter(
                                x=[phs_cur, phs_next],
                                y=[temp_cur, temp_next],
                                mode='lines',
                                line=dict(color='blue', width=0.5),
                                showlegend=False
                            ))

                        phs.append(phs_next)
                        pbs.append(get_thomson_psibar_value(t_next, data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]))
                        tmps.append(temp_next)
                        shts.append(sht_next_data)
                        sht_ints.append(int(s))
                        if s not in unique_included_shots:
                            unique_included_shots.append(s)
    
                # append minor arrays to scatter plot arrays
                crash_phase_array += phs
                thomson_psibar_array += pbs
                thomson_temp_array += tmps
                shot_labels += shts
                shot_ints += sht_ints
    
    # scatter plot
    scatter = go.Scatter(
        x=crash_phase_array,
        y=thomson_temp_array,
        mode='markers',
        marker=dict(color=thomson_psibar_array, colorscale='Jet', colorbar=dict(title='Normalized Psi')),
        text=shot_labels,
        hoverinfo='text',
        name='Crash Events'
    )

    # Add the scatter and line plots to the figure
    fig = go.Figure(data=[scatter] + lines)
    
    # Add title and labels
    fig.update_layout(
        title=f"Temperature over Phase Colored by Normalized Psi\nTS{thomson_position} // {len(crash_phase_array)} Points, {len(unique_included_shots)} Shots",
        xaxis=dict(
            title="Phase",
            showgrid=True,  # Enable grid lines for the x-axis
            gridcolor="lightgray",  # Color of the grid lines
            gridwidth=1  # Thickness of the grid lines
        ),
        yaxis=dict(
            title="Thomson Temperature [eV]",
            showgrid=True,  # Enable grid lines for the y-axis
            gridcolor="lightgray",  # Color of the grid lines
            gridwidth=1  # Thickness of the grid lines
        ),
        showlegend=False
    )
    
    # Save the figure to an HTML file
    fig.write_html(f'plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/thomson/temperature_phase_scatter_going_over_crashes_ts{thomson_position}.html')
    fig.show()
    
    return



def plot_temp_phase_for_shotlist_spanning_crashes(data_dir, thomson_position):
    # fig, ax = plt.subplots()
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict_by_shot = load_thomson_phase_data_by_shot(data_dir, True, True, True, True)
    
    temp_phase_slope_dict = filter.get_slope_at_phase_by_shot(data_dict_by_shot, thomson_position, 0.4, True)
    
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    crash_phase_array = []
    thomson_psibar_array = []
    thomson_temp_array = []
    shot_labels = []
    shot_ints = []
    
    fig, ax = plt.subplots()
    for s in temp_phase_slope_dict.keys():
        if s in lifetimes_dict.keys():
            if type(lifetimes_dict[s]) != type(str()):
                sorted_by_time = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_times"])
                for i in range(len(sorted_by_time) - 1):
                    if int(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i]*1000) > len(data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]):
                        continue
                    
                    else:
                        t_cur = data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[i]]
                        t_next = data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[i+1]]
                        crash_in_between = False
                        for t in data_dict_by_shot[s]["crash_info"]['times']:
                            if t_cur < t and t < t_next:
                                crash_in_between=True
                        
                        if crash_in_between:
                            phs_cur = data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[i]]
                            phs_next = data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[i+1]] + 1
                            temp_cur = data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i]]
                            temp_next = data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i+1]]
                            sht_cur_data = (f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i]}s")
                            sht_next_data = (f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i+1]}s")
                            
                            phs = [phs_cur, phs_next]
                            pbs = [get_thomson_psibar_value(t_cur, data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]), get_thomson_psibar_value(t_next, data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"])]
                            tmps = [temp_cur, temp_next]
                            shts = [sht_cur_data, sht_next_data]
                            sht_ints = [int(s), int(s)]
                            
                            if temp_cur < temp_next:
                                plt.plot(phs, tmps, linewidth=0.5, color='r')
                            else:
                                plt.plot(phs, tmps, linewidth=0.25, color='b')
                                
                            # append minor arrays to scatter plot arrays
                            crash_phase_array += phs
                            thomson_psibar_array += pbs
                            thomson_temp_array += tmps
                            shot_labels += shts
                            shot_ints += sht_ints

    
    scatter = plt.scatter(crash_phase_array, thomson_temp_array, c=thomson_psibar_array, cmap='jet_r', marker='.', picker=True)
    plt.colorbar(label="Normalized Psi")
    cursor.add_cursors_to_scatter(scatter, shot_labels)
    plt.title(f"Temperature over Phase Coloured by Normalized Psi\nTS{thomson_position}")
    plt.ylabel("Thomson Temperature [eV]")
    plt.xlabel("Phase")
    click.add_click_action_timeseries_plots(data_dir, scatter, fig, shot_ints)
    # def on_pick(event):
    #     print("Pick event detected!")
    
    # fig.canvas.mpl_connect('pick_event', on_pick)
    plt.show()
    
    return



def plot_temp_phase_for_shotlist_spanning_crashes_plotly(data_dir, thomson_position):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict_by_shot = load_thomson_phase_data_by_shot(data_dir, True, True, True, True)
    
    temp_phase_slope_dict = filter.get_slope_at_phase_by_shot(data_dict_by_shot, thomson_position, 0.4, False)
    
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    crash_phase_array = []
    thomson_psibar_array = []
    thomson_temp_array = []
    shot_labels = []
    shot_ints = []
    lines = []
    
    unique_shots = []

    for s in temp_phase_slope_dict.keys():
        if s in lifetimes_dict.keys():
            if type(lifetimes_dict[s]) != type(str()):
                sorted_by_time = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_times"])
                for i in range(len(sorted_by_time) - 1):
                    if int(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i]*1000) > len(data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]):
                        continue
                    
                    else:
                        t_cur = data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[i]]
                        t_next = data_dict_by_shot[s][f"thomson_{thomson_position}_times"][sorted_by_time[i+1]]
                        crash_in_between = False
                        for t in data_dict_by_shot[s]["crash_info"]['times']:
                            if t_cur < t and t < t_next:
                                crash_in_between=True
                        
                        if crash_in_between:
                            phs_cur = data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[i]]
                            phs_next = data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][sorted_by_time[i+1]] + 1
                            temp_cur = data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i]]
                            temp_next = data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][sorted_by_time[i+1]]
                            sht_cur_data = (f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i]}s")
                            sht_next_data = (f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i+1]}s")
                            
                            phs = [phs_cur, phs_next]
                            pbs = [get_thomson_psibar_value(t_cur, data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]), get_thomson_psibar_value(t_next, data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"])]
                            tmps = [temp_cur, temp_next]
                            shts = [sht_cur_data, sht_next_data]
                            sht_ints = [int(s), int(s)]
                            
                            lines.append(go.Scatter(
                                x=phs,
                                y=tmps,
                                mode='lines',
                                line=dict(color='red' if temp_cur < temp_next else 'blue', width=0.5),
                                name=f"Shot {s}"
                            ))

                            # append minor arrays to scatter plot arrays
                            crash_phase_array += phs
                            thomson_psibar_array += pbs
                            thomson_temp_array += tmps
                            shot_labels += shts
                            shot_ints += sht_ints
            unique_shots.append(s)
            
            
    # scatter plot
    scatter = go.Scatter(
        x=crash_phase_array,
        y=thomson_temp_array,
        mode='markers',
        marker=dict(color=thomson_psibar_array, colorscale='Jet', colorbar=dict(title='Normalized Psi')),
        text=shot_labels,
        hoverinfo='text',
        name='Crash Events'
    )
    
    # Add the scatter and line plots to the figure
    fig = go.Figure(data=[scatter] + lines)
    
    # Add title and labels
    fig.update_layout(
        title=f"Temperature over Phase Colored by Normalized Psi\nTS{thomson_position} // {len(crash_phase_array)} Points, {len(unique_shots)} Shots",
        xaxis=dict(
            title="Phase",
            showgrid=True,  # Enable grid lines for the x-axis
            gridcolor="lightgray",  # Color of the grid lines
            gridwidth=1  # Thickness of the grid lines
        ),
        yaxis=dict(
            title="Thomson Temperature [eV]",
            showgrid=True,  # Enable grid lines for the y-axis
            gridcolor="lightgray",  # Color of the grid lines
            gridwidth=1  # Thickness of the grid lines
        ),
        showlegend=False
    )
    
    fig.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/thomson/temperature_phase_scatter_spanning_crashes_ts{thomson_position}.html")
    fig.show()
    
    return




def plot_temp_phase_for_shotlist_cut_between_crashes(data_dir, thomson_position):
    fig, ax = plt.subplots()
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict_by_shot = load_thomson_phase_data_by_shot(data_dir, True, True, True, True)
    
    temp_phase_slope_dict = filter.get_slope_at_phase_by_shot(data_dict_by_shot, thomson_position, 0.4, True)
    
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    crash_phase_array = []
    thomson_psibar_array = []
    thomson_temp_array = []
    shot_labels = []
    shot_ints = []
    
    for s in temp_phase_slope_dict.keys():
        if s in lifetimes_dict.keys():
            if type(lifetimes_dict[s]) != type(str()):
                sorted_by_time = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_times"])
                tms = []
                phs = []
                tmps = []
                shts = []
                pbs = []
                sht_ints = []
                for i in sorted_by_time:
                    if int(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i]*1000) > len(data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]):
                        continue
                    elif len(tmps) == 0:
                        tms.append(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i])
                        phs.append(data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][i])
                        tmps.append(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][i])
                        shts.append(f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i]}s")
                        pbs.append(get_thomson_psibar_value(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i], data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]))
                        sht_ints.append(int(s))
                        crash_in_between = False
                    else:
                        for t in data_dict_by_shot[s]["crash_info"]['times']:
                            if tms[-1] < t and t < data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i]:
                                crash_in_between=True
                        if crash_in_between:
                            if len(tms) > 1:
                                if tmps[0] < tmps[-1]:
                                    plt.plot(phs, tmps, linewidth=0.5, color='r')
                                else:
                                    plt.plot(phs, tmps, linewidth=0.25, color='b')
                                
                                # append minor arrays to scatter plot arrays
                                crash_phase_array += phs
                                thomson_psibar_array += pbs
                                thomson_temp_array += tmps
                                shot_labels += shts
                                shot_ints += sht_ints
                                
                            # reset minor arrays
                            tms = []
                            phs = []
                            tmps = []
                            shts = []
                            pbs = []
                            sht_ints = []

                        else:
                            tms.append(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i])
                            phs.append(data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][i])
                            tmps.append(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][i])
                            shts.append(f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i]}s")
                            pbs.append(get_thomson_psibar_value(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i], data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]))
                            sht_ints.append(int(s))
                            
                            
    scatter = plt.scatter(crash_phase_array, thomson_temp_array, c=thomson_psibar_array, cmap='jet_r', marker='.')
    plt.colorbar(label="Normalized Psi")
    cursor.add_cursors_to_scatter(scatter, shot_labels)
    plt.title(f"Temperature over Phase Coloured by Normalized Psi\nTS{thomson_position}")
    plt.ylabel("Thomson Temperature [eV]")
    plt.xlabel("Phase")
    click.add_click_action_timeseries_plots(data_dir, scatter, fig, shot_ints)
    plt.show()
    
    
    return


def plot_temp_phase_for_shotlist_cut_between_crashes_plotly(data_dir, thomson_position):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict_by_shot = load_thomson_phase_data_by_shot(data_dir, True, True, True, True)
    
    temp_phase_slope_dict = filter.get_slope_at_phase_by_shot(data_dict_by_shot, thomson_position, 0.4, False)
    
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    crash_phase_array = []
    thomson_psibar_array = []
    thomson_temp_array = []
    shot_labels = []
    shot_ints = []
    lines = []

    unique_shots = []

    for s in temp_phase_slope_dict.keys():
        if s in lifetimes_dict.keys():
            if type(lifetimes_dict[s]) != type(str()):
                sorted_by_time = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_times"])
                tms = []
                phs = []
                tmps = []
                shts = []
                pbs = []
                sht_ints = []
                for i in sorted_by_time:
                    if int(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i]*1000) > len(data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]):
                        continue
                    elif len(tmps) == 0:
                        tms.append(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i])
                        phs.append(data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][i])
                        tmps.append(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][i])
                        shts.append(f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i]}s")
                        pbs.append(get_thomson_psibar_value(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i], data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]))
                        sht_ints.append(int(s))
                        crash_in_between = False
                    else:
                        for t in data_dict_by_shot[s]["crash_info"]['times']:
                            if tms[-1] < t and t < data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i]:
                                crash_in_between=True
                        if crash_in_between:
                            if len(tms) > 1:
                                lines.append(go.Scatter(
                                    x=phs,
                                    y=tmps,
                                    mode='lines',
                                    line=dict(color='red' if tmps[0] < tmps[-1] else 'blue', width=0.5),
                                    name=f"Shot {s}"
                                ))

                                # append minor arrays to scatter plot arrays
                                crash_phase_array += phs
                                thomson_psibar_array += pbs
                                thomson_temp_array += tmps
                                shot_labels += shts
                                shot_ints += sht_ints
                                
                            # reset minor arrays
                            tms = []
                            phs = []
                            tmps = []
                            shts = []
                            pbs = []
                            sht_ints = []

                        else:
                            tms.append(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i])
                            phs.append(data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][i])
                            tmps.append(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][i])
                            shts.append(f"Shot {s}: t={data_dict_by_shot[s][f'thomson_{thomson_position}_times'][i]}s")
                            pbs.append(get_thomson_psibar_value(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i], data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]))
                            sht_ints.append(int(s))
                            
                unique_shots.append(s)
    
    # scatter plot
    scatter = go.Scatter(
        x=crash_phase_array,
        y=thomson_temp_array,
        mode='markers',
        marker=dict(color=thomson_psibar_array, colorscale='Jet', colorbar=dict(title='Normalized Psi')),
        text=shot_labels,
        hoverinfo='text',
        name='Crash Events'
    )

    # Add the scatter and line plots to the figure
    fig = go.Figure(data=[scatter] + lines)
    
    # Add title and labels
    fig.update_layout(
        title=f"Temperature over Phase Colored by Normalized Psi\nTS{thomson_position} // {len(crash_phase_array)} Points, {len(unique_shots)} Shots",
        xaxis=dict(
            title="Phase",
            showgrid=True,  # Enable grid lines for the x-axis
            gridcolor="lightgray",  # Color of the grid lines
            gridwidth=1  # Thickness of the grid lines
        ),
        yaxis=dict(
            title="Thomson Temperature [eV]",
            showgrid=True,  # Enable grid lines for the y-axis
            gridcolor="lightgray",  # Color of the grid lines
            gridwidth=1  # Thickness of the grid lines
        ),
        showlegend=False
    )
    
    # Save the figure to an HTML file
    fig.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/thomson/temperature_phase_scatter_cut_between_crashes_ts{thomson_position}.html")
    fig.show()

    return



def plot_temp_phase_for_shotlist(data_dir, thomson_position, connect_each_shot_temperature):
    fig, ax = plt.subplots()
    
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict_by_shot = load_thomson_phase_data_by_shot(data_dir, True, True, True, True)
    
    temp_phase_slope_dict = filter.get_slope_at_phase_by_shot(data_dict_by_shot, thomson_position, 0.4, True)
    
    crash_phase_array = []
    thomson_psibar_array = []
    thomson_temp_array = []
    shot_labels = []
    for s in temp_phase_slope_dict.keys():
        if temp_phase_slope_dict[s] < 0:
            sorted_by_phase = np.argsort(data_dict_by_shot[s][f"thomson_{thomson_position}_phases"])
            phs = []
            tmps = []
            for i in sorted_by_phase:
                crash_phase_array.append(data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][i])
                thomson_temp_array.append(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][i])
                thomson_psibar_array.append(get_thomson_psibar_value(data_dict_by_shot[s][f"thomson_{thomson_position}_times"][i], data_dict_by_shot[s][f"thomson_{thomson_position}_psibars"]))
                shot_labels.append(s)
                phs.append(data_dict_by_shot[s][f"thomson_{thomson_position}_phases"][i])
                tmps.append(data_dict_by_shot[s][f"thomson_{thomson_position}_temps"][i])
            if connect_each_shot_temperature:
                if max(tmps) > 300:
                    plt.plot(phs, tmps, linewidth=0.5, color='r')
                else:
                    plt.plot(phs, tmps, linewidth=0.25, color='k')
                
        
    scatter = plt.scatter(crash_phase_array, thomson_temp_array, c=thomson_psibar_array, cmap='jet_r', marker='.')
    plt.colorbar(label="Normalized Psi")
    cursor.add_cursors_to_scatter(scatter, shot_labels)
    plt.title(f"Temperature over Phase Coloured by Normalized Psi\nTS{thomson_position}")
    plt.ylabel("Thomson Temperature [eV]")
    plt.xlabel("Phase")
    click.add_click_action_timeseries_plots(data_dir, scatter, fig, shot_labels)
    plt.show()
    

    plot_stdev_bins = False
    if plot_stdev_bins:
        bin_centers, binned_temp_medians, binned_stdevs = bin_by_phase(phase_array=crash_phase_array, value_array=thomson_psibar_array, n_bins=20, percentiles_list=[0.16, 0.5, 0.84])
        plot_stdev_of_bins(bin_centers, binned_stdevs)
        plt.show()

    return




def plot_psi_phase(data_dir, thomson_position, connect_each_shot_psibar, connect_each_shot_temperature):
    fig, ax = plt.subplots()
    
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict = load_thomson_phase_data_plottable(data_dir, True, True, True)
    
    # unpack data
    crash_info = data_dict['crash_info']
    thomson_data = data_dict[f'thomson_{thomson_position}']
    thomson_psibar = data_dict['thomson_psibar']
    shot_list_flt = data_dict['shot_list_flt']
    shot_list_int = data_dict['shot_list_int']
    
    # set up arrays
        # set temperature array
    thomson_temp_array_900 = []
        # set phase
    crash_phase_array = []
    crash_time_array = []
        # set psibar values
    thomson_psibar_array_900 = []
        # set shot labels
    shot_labels = []
    
    num_shots = len(shot_list_flt)
    for i in range(len(shot_list_flt)):
        shot = int(shot_list_flt[i])
        singleshot_thomson_data = thomson_data.loc[shot_list_flt[i]]
        ss_thoms_keys = singleshot_thomson_data.keys()
        
        # set up temporary arrays
            # set up temperature arrays
        ss_temps_900 = []
            # set up timing array
        ss_times = []
            # set up thomson psibar
        ss_thomson_psibar_900 = []
        
        # set up iterative variables
        j = 0
        cur_tempstring = f"T{j} (eV)"
        cur_timestring = f"t{j} (ms)"
        while (cur_timestring in ss_thoms_keys):
            if (singleshot_thomson_data[cur_tempstring] > 0) and (singleshot_thomson_data[cur_timestring] < len(thomson_psibar[str(shot)]['ThomsonR899'])):
                # get individual temperatures
                ss_temps_900.append(singleshot_thomson_data[cur_tempstring])
                # get times
                ss_times.append(singleshot_thomson_data[cur_timestring] / 1000)
                # append the psibar values
                ss_thomson_psibar_900.append(get_thomson_psibar_value(ss_times[-1], thomson_psibar[str(shot)]['ThomsonR899']))
                
                shot_labels.append(shot)

            # reset for next iteration
            j += 1
            cur_tempstring = f"T{j} (eV)"
            cur_timestring = f"t{j} (ms)"
        
        phases = convert_times_to_phases(shot_list_int[i], data_dir, ss_times)
        times_since_crashes = convert_to_times_since_crashes(shot_list_int[i], data_dir, ss_times)
        
        if connect_each_shot_psibar and len(phases) > 1 and max(ss_temps_900) > 200:
            phs, tmps, psibrs = reorder_arrays(phases, ss_temps_900, ss_thomson_psibar_900)
            if min(psibrs) < 0.6 and max(psibrs) > 0.6:
                plt.plot(phs, psibrs, linewidth=0.5, color='r')
            else:
                plt.plot(phs, psibrs, linewidth=0.25, color='k')
        
        if connect_each_shot_temperature and len(phases) > 1:
            phs, tmps, psibrs = reorder_arrays(phases, ss_temps_900, ss_thomson_psibar_900)
            if max(ss_temps_900) > 200:
                plt.plot(phs, tmps, linewidth=0.5, color='r')
            else:
                plt.plot(phs, tmps, linewidth=0.25, color='k')
        
        # get temperature array
        thomson_temp_array_900 += ss_temps_900
        # get phase
        crash_phase_array += phases
        crash_time_array += times_since_crashes
        # get psibar values
        thomson_psibar_array_900 += ss_thomson_psibar_900
        
        prog_bar.progress_bar_pct_only(i, num_shots)
    
    plot_psi_phase_temp = False
    if plot_psi_phase_temp:
        scatter = plt.scatter(crash_phase_array, thomson_psibar_array_900, c=thomson_temp_array_900, cmap='jet', marker='.')
        plt.colorbar(label="Thomson Temperature [eV]")
        cursor.add_cursors_to_scatter(scatter, shot_labels)
        plt.title(f"Normalized Psi over Phase Coloured by Temperature\nTS{thomson_position}")
        plt.ylabel("Normalized Psi")
        plt.xlabel("Phase")
        plt.show()
        
    plot_psi_temp_phase = True
    if plot_psi_temp_phase:
        scatter = plt.scatter(crash_phase_array, thomson_temp_array_900, c=thomson_psibar_array_900, cmap='jet_r', marker='.')
        plt.colorbar(label="Normalized Psi")
        cursor.add_cursors_to_scatter(scatter, shot_labels)
        plt.title(f"Temperature over Phase Coloured by Normalized Psi\nTS{thomson_position}")
        plt.ylabel("Thomson Temperature [eV]")
        plt.xlabel("Phase")
        click.add_click_action_timeseries_plots(data_dir, scatter, fig, shot_labels)
        plt.show()
    

    plot_stdev_bins = False
    if plot_stdev_bins:
        bin_centers, binned_temp_medians, binned_stdevs = bin_by_phase(phase_array=crash_phase_array, value_array=thomson_psibar_array_900, n_bins=20, percentiles_list=[0.16, 0.5, 0.84])
        plot_stdev_of_bins(bin_centers, binned_stdevs)
        plt.show()

    return
        
        


def thomson_phase_plot(data_dir, plt_psibar=True):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    data_dict = load_thomson_phase_data_plottable(data_dir, True, True, plt_psibar)
    
    # unpack data
    crash_info = data_dict['crash_info']
    thomson_data_600 = data_dict['thomson_600']
    thomson_data_730 = data_dict['thomson_730']
    thomson_data = data_dict['thomson_900']
    if plt_psibar:
        thomson_psibar = data_dict['thomson_psibar']
    shot_list_flt = data_dict['shot_list_flt']
    shot_list_int = data_dict['shot_list_int']
        
    # make plottable arrays
        # pure temperature arrays
    thomson_temp_array_600 = []
    thomson_temp_array_730 = []
    thomson_temp_array_900 = []
        # temperature ratio arrays
    thomson_temp_array_600_730 = []
    thomson_temp_array_600_900 = []
    thomson_temp_array_900_600 = []
        # phase array
    crash_phase_array = []
    crash_time_array = []
        # thomson psibar array
    thomson_psibar_array_600 = []
    thomson_psibar_array_730 = []
    thomson_psibar_array_900 = []
    
    num_shots = len(shot_list_flt)
    for i in range(len(shot_list_flt)):
        shot = int(shot_list_flt[i])
        singleshot_thomson_data_600 = thomson_data_600.loc[shot_list_flt[i]]
        singleshot_thomson_data_730 = thomson_data_730.loc[shot_list_flt[i]]
        singleshot_thomson_data = thomson_data.loc[shot_list_flt[i]]
        ss_thoms_keys = singleshot_thomson_data_600.keys()
        
        # set up temporary arrays
            # set up temperature arrays
        ss_temps_600 = []
        ss_temps_730 = []
        ss_temps_900 = []
            # set up temperature ratios
        ss_temps_600_730 = []
        ss_temps_600_900 = []
        ss_temps_900_600 = []
            # set up timings arrays
        ss_times = []
            # set up thomson psibar
        ss_thomson_psibar_600 = []
        ss_thomson_psibar_730 = []
        ss_thomson_psibar_900 = []
        
        # set up iterative variables
        j = 0
        cur_tempstring = f"T{j} (eV)"
        cur_timestring = f"t{j} (ms)"
        while (cur_timestring in ss_thoms_keys):
            if (singleshot_thomson_data_600[cur_tempstring] > 0):
                # get individual temperatures
                ss_temps_600.append(singleshot_thomson_data_600[cur_tempstring])
                ss_temps_730.append(singleshot_thomson_data_730[cur_tempstring])
                ss_temps_900.append(singleshot_thomson_data[cur_tempstring])
                # get temperature migration ratios
                ss_temps_600_730.append(singleshot_thomson_data_600[cur_tempstring] / singleshot_thomson_data_730[cur_tempstring])
                ss_temps_600_900.append(singleshot_thomson_data_600[cur_tempstring] / singleshot_thomson_data[cur_tempstring])
                ss_temps_900_600.append(singleshot_thomson_data[cur_tempstring] / singleshot_thomson_data_600[cur_tempstring])
                # get times
                ss_times.append(singleshot_thomson_data_600[cur_timestring] / 1000)
                
                ss_thomson_psibar_600.append(get_thomson_psibar_value(ss_times[-1], thomson_psibar[str(shot)]['ThomsonR600']))
                ss_thomson_psibar_730.append(get_thomson_psibar_value(ss_times[-1], thomson_psibar[str(shot)]['ThomsonR747']))
                ss_thomson_psibar_900.append(get_thomson_psibar_value(ss_times[-1], thomson_psibar[str(shot)]['ThomsonR899']))

            # reset for next iteration
            j += 1
            cur_tempstring = f"T{j} (eV)"
            cur_timestring = f"t{j} (eV)"

        phases = convert_times_to_phases(shot_list_int[i], data_dir, ss_times)
        times_since_crashes = convert_to_times_since_crashes(shot_list_int[i], data_dir, ss_times)
        
        # get temperature arrays
        thomson_temp_array_600 += ss_temps_600
        thomson_temp_array_730 += ss_temps_730
        thomson_temp_array_900 += ss_temps_900
        # get temperature migration ratios
        thomson_temp_array_600_730 += ss_temps_600_730
        thomson_temp_array_600_900 += ss_temps_600_900
        thomson_temp_array_900_600 += ss_temps_900_600
        # get phase
        crash_phase_array += phases
        crash_time_array += times_since_crashes
        # get psibar values
        thomson_psibar_array_600 += ss_thomson_psibar_600
        thomson_psibar_array_730 += ss_thomson_psibar_730
        thomson_psibar_array_900 += ss_thomson_psibar_900
        
        prog_bar.progress_bar_pct_only(i, num_shots)
    
    
    
    ######################################################################################################################################################################
    # plotting values now that the data has been loaded
    ######################################################################################################################################################################
    
    fig, ax = plt.subplots()
    
    plt.xlabel("Phase Between Two Crashes")
    
    crash_time_core_temp = False
    if crash_time_core_temp:
        scatter = plt.scatter(crash_time_array, thomson_temp_array_600, c='b', marker='.')
        cursor.add_cursors_to_scatter(scatter, shot_list_int)
        plt.title("Thomson Temperature Over Phase")
        plt.ylabel("Thomson Temperature [eV]")
        plt.show()
    
    plot_core_temp = False
    if plot_core_temp:
        scatter = plt.scatter(crash_phase_array, thomson_temp_array_600, c=thomson_psibar_array_600, cmap='jet', marker='.')
        plt.colorbar(label='psibar')
        cursor.add_cursors_to_scatter(scatter, shot_list_int)
        plt.title("Thomson Temperature Over Phase")
        plt.ylabel("Thomson Temperature [eV]")
        plt.show()
        
    plot_edge_temp = True
    if plot_edge_temp:
        scatter = plt.scatter(crash_phase_array, thomson_psibar_array_900, c=thomson_temp_array_900, cmap='jet', marker='.')
        psilabel = 'Psi'
        templabel_unitless = "Thomson Temperature"
        templabel = templabel_unitless + " [eV]"
        plt.colorbar(label=templabel)
        cursor.add_cursors_to_scatter(scatter, shot_list_int)
        plt.title(psilabel + " Over Phase at TS900")
        plt.ylabel(psilabel)
        bin_centers, binned_temp_medians, binned_stdevs = bin_by_phase(phase_array=crash_phase_array, value_array=thomson_psibar_array_900, n_bins=20, percentiles_list=[0.16, 0.5, 0.84])
        # plot_temperature_percentiles(bin_centers, binned_temp_medians)
        plt.show()
        
        plot_stdev_of_bins(bin_centers, binned_stdevs)
        plt.show()
    
    plot_temp_ratio_in_out = False
    if plot_temp_ratio_in_out:
        scatter = plt.scatter(crash_phase_array, thomson_temp_array_900_600, c='b', marker='.')
        cursor.add_cursors_to_scatter(scatter, shot_list_int)
        plt.title("Thomson Temperature Over Phase")
        plt.ylabel("Thomson Temperature Ratio (TS900/TS600)")
        bin_centers, binned_temp_medians, binned_temp_stdevs = bin_by_phase(phase_array=crash_phase_array, value_array=thomson_temp_array_900_600, n_bins=20, percentiles_list=[0.16, 0.5, 0.84])
        plot_temperature_percentiles(bin_centers, binned_temp_medians)
        plt.show()
    
    plot_temp_ratio_in_mid = False
    if plot_temp_ratio_in_mid:
        scatter = plt.scatter(crash_phase_array, thomson_temp_array_600_730, c='b', marker='.')
        cursor.add_cursors_to_scatter(scatter, shot_list_int)
        plt.title("Thomson Temperature Over Phase")
        plt.ylabel("Thomson Temperature Ratio (R730/R900)")
        plt.show()
    
    plt.show()
    
    return




