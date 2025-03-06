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



def reconstruct_q_change_over_phase_without_last_half_cycle_num_crashes_sustain_non_sustain(data_dir, num_phase_bins, num_crashes, q_psibar='min', show_plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    if q_psibar == 'min':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q_min_data.json")
    if q_psibar == '95':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q95_data.json")
    if q_psibar == '00':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q00_data.json")
    sustainment_dict = load.load_json_file("machine_settings_and_state/sustainment/sustainment.json")
    crash_dict = load.load_json_file("2024-10-10_19718-23016/crash_info_with_hardware_error.json")
    
    # plotting arrays
        # q and phase arrays
    q_array_sustain = []
    q_array_non_sustain = []
    q_phase_array_sustain = []
    q_phase_array_non_sustain = []
        # q and phase slope arrays
    q_slope_array_sustain = []
    q_slope_array_non_sustain = []
    q_phase_slope_array_sustain = []
    q_phase_slope_array_non_sustain = []
        # shot number arrays
    shot_numbers_slope_array_sustain = []
    shot_numbers_slope_array_non_sustain = []
    
    unique_shots = []
    
    # make arrays of thomson temperature data
    fig, ax = plt.subplots(figsize=(16,9))
    cur = 1
    tot = len(q_dict)
    for s in q_dict.keys():
        if s in crash_dict.keys() and s in sustainment_dict:
            if type(sustainment_dict[s]) != type(str()) and type(q_dict[s]) != type(str()) and type(crash_dict[s]) != type(str()):
                temp_data = load_data.load_json_file(data_dir + "crash_phase/phase_" + str(s) + ".json")
                if sustainment_dict[s] > 0 and len(crash_dict[s]['times']) == num_crashes:
                    valid_q_points_shot=0
                    for i in range(len(q_dict[s]['data'])):
                        # get phase offset based on how many crashes have occurred
                        j = 0
                        while len(crash_dict[s]['times']) > j:
                            if crash_dict[s]['times'][j] < q_dict[s]['times'][i]:
                                j += 1
                            else:
                                break

                        cur_phase = convert_times_to_phases(temp_data, q_dict[s]['times'][i])
                        if cur_phase > 0.5 and j >= len(crash_dict[s]['times']):
                            continue
                        else:
                            q_array_sustain.append(q_dict[s]['data'][i])
                            q_phase_array_sustain.append(cur_phase + j)
                            valid_q_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_q_points_shot - 1):
                        q_slope_array_sustain.append((q_array_sustain[-(i+1)] - q_array_sustain[-i]) / (q_phase_array_sustain[-(i+1)] - q_phase_array_sustain[-i]))
                        q_phase_slope_array_sustain.append((q_phase_array_sustain[-(i+1)] + q_phase_array_sustain[-i]) / 2)
                        shot_numbers_slope_array_sustain.append(s)
                        
                    unique_shots.append(s)
                
                elif len(crash_dict[s]['times']) == num_crashes:
                    valid_q_points_shot=0
                    for i in range(len(q_dict[s]['data'])):
                        # get phase offset based on how many crashes have occurred
                        j = 0
                        while len(crash_dict[s]['times']) > j:
                            if crash_dict[s]['times'][j] < q_dict[s]['times'][i]:
                                j += 1
                            else:
                                break
                        
                        cur_phase = convert_times_to_phases(temp_data, q_dict[s]['times'][i])
                        if cur_phase > 0.5 and j >= len(crash_dict[s]['times']):
                            continue
                        else:
                            q_array_non_sustain.append(q_dict[s]['data'][i])
                            q_phase_array_non_sustain.append(cur_phase + j)
                            valid_q_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_q_points_shot - 1):
                        q_slope_array_non_sustain.append((q_array_non_sustain[-(i+1)] - q_array_non_sustain[-i]) / (q_phase_array_non_sustain[-(i+1)] - q_phase_array_non_sustain[-i]))
                        q_phase_slope_array_non_sustain.append((q_phase_array_non_sustain[-(i+1)] + q_phase_array_non_sustain[-i]) / 2)
                        shot_numbers_slope_array_non_sustain.append(s)
                        
                    unique_shots.append(s)


            pb_pct(cur, tot)
            cur += 1

    # reconstruct thomson temp from slope data
        # get indices of sorted arrays
            # sustain
    q_slope_indices_sorted_by_phase_sustain = np.argsort(q_phase_slope_array_sustain)
    q_slope_array_sustain = [q_slope_array_sustain[i] for i in q_slope_indices_sorted_by_phase_sustain]
    q_phase_slope_array_sustain = [q_phase_slope_array_sustain[i] for i in q_slope_indices_sorted_by_phase_sustain]
    shot_numbers_slope_array_sustain = [shot_numbers_slope_array_sustain[i] for i in q_slope_indices_sorted_by_phase_sustain]
            # non sustain
    q_slope_indices_sorted_by_phase_non_sustain = np.argsort(q_phase_slope_array_non_sustain)
    q_slope_array_non_sustain = [q_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_phase_non_sustain]
    q_phase_slope_array_non_sustain = [q_phase_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_phase_non_sustain]
    shot_numbers_slope_array_non_sustain = [shot_numbers_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_phase_non_sustain]
    
        # get boundaries of bins
            # sustain
    bin_edges_phase_sustain = np.linspace(q_phase_slope_array_sustain[0], q_phase_slope_array_sustain[-1], num_phase_bins + 1)
            # non sustain
    bin_edges_phase_non_sustain = np.linspace(q_phase_slope_array_non_sustain[0], q_phase_slope_array_non_sustain[-1], num_phase_bins + 1)
    
    q_slope_means_sustain = []
    q_slope_means_non_sustain = []
    q_slope_phase_means_sustain = []
    q_slope_phase_means_non_sustain = []
    
    for i in range(len(bin_edges_phase_sustain) - 1):
        # sustain
        q_mean_sustain = median_of_bin(q_slope_array_sustain, q_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        q_slope_means_sustain.append(q_mean_sustain) if q_mean_sustain is not None else None
        q_p_mean_sustain = median_of_bin(q_phase_slope_array_sustain, q_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        q_slope_phase_means_sustain.append(q_p_mean_sustain) if q_p_mean_sustain is not None else None
        # non sustain
        q_mean_non_sustain = median_of_bin(q_slope_array_non_sustain, q_phase_slope_array_non_sustain, bin_edges_phase_non_sustain[i], bin_edges_phase_non_sustain[i+1])
        q_slope_means_non_sustain.append(q_mean_non_sustain) if q_mean_non_sustain is not None else None
        q_p_mean_non_sustain = median_of_bin(q_phase_slope_array_non_sustain, q_phase_slope_array_non_sustain, bin_edges_phase_non_sustain[i], bin_edges_phase_non_sustain[i+1])
        q_slope_phase_means_non_sustain.append(q_p_mean_non_sustain) if q_p_mean_non_sustain is not None else None
        
    # integrate
        # sustain
    q_recon_array_sustain = cumtrapz(q_slope_means_sustain, q_slope_phase_means_sustain, initial=0)
    q_phase_recon_array_sustain = q_slope_phase_means_sustain
        # non sustain
    q_recon_array_non_sustain = cumtrapz(q_slope_means_non_sustain, q_slope_phase_means_non_sustain, initial=0)
    q_phase_recon_array_non_sustain = q_slope_phase_means_non_sustain


    # zero out array
        # sustain
    for i in range(len(q_recon_array_sustain)):
        q_recon_array_sustain[i] = q_recon_array_sustain[i] - min(q_recon_array_sustain)
        
        # non sustain
    for i in range(len(q_recon_array_non_sustain)):
        q_recon_array_non_sustain[i] = q_recon_array_non_sustain[i] - min(q_recon_array_non_sustain)

    # offset array by c
        # sustain
    c = np.nanmean(q_array_sustain) - np.nanmean(q_recon_array_sustain)
    for i in range(len(q_recon_array_sustain)):
        q_recon_array_sustain[i] = q_recon_array_sustain[i] + c
        
        # non sustain
    c = np.nanmean(q_array_non_sustain) - np.nanmean(q_recon_array_non_sustain)
    for i in range(len(q_recon_array_non_sustain)):
        q_recon_array_non_sustain[i] = q_recon_array_non_sustain[i] + c
    
    
    # Scatter of the q slope over phase data
    fig1 = go.Figure()

    # Add scatter points
    fig1.add_trace(go.Scatter(
        x=q_phase_slope_array_sustain,
        y=q_slope_array_sustain,
        mode='markers',
        name="dq/dp of Sustain Shots",
        marker=dict(color='red', opacity=0.3),
        text=shot_numbers_slope_array_sustain
    ))

    fig1.add_trace(go.Scatter(
        x=q_phase_slope_array_non_sustain,
        y=q_slope_array_non_sustain,
        mode='markers',
        name="dq/dp of Non-Sustain Shots",
        marker=dict(color='blue', opacity=0.3),
        text=shot_numbers_slope_array_non_sustain
    ))

    # Add median lines
    fig1.add_trace(go.Scatter(
        x=q_slope_phase_means_sustain,
        y=q_slope_means_sustain,
        mode='lines',
        name='Median of Sustain Shots',
        line=dict(color='red')
    ))

    fig1.add_trace(go.Scatter(
        x=q_slope_phase_means_non_sustain,
        y=q_slope_means_non_sustain,
        mode='lines',
        name='Median of Non-Sustain Shots',
        line=dict(color='blue')
    ))

    # Layout settings
    fig1.update_layout(
        title=f"dq/dp Over Phase at q{q_psibar}<br>{num_crashes} Crashes\n{len(q_phase_slope_array_sustain) + len(q_phase_slope_array_non_sustain)} Points, {len(unique_shots)} Shots",
                    xaxis=dict(
            title="Phase",
            showgrid=True,  # Enable grid lines for the x-axis
            gridcolor="lightgray",  # Color of the grid lines
            gridwidth=1  # Thickness of the grid lines
        ),
        yaxis=dict(
            title="dq/dp",
            showgrid=True,  # Enable grid lines for the y-axis
            gridcolor="lightgray",  # Color of the grid lines
            gridwidth=1  # Thickness of the grid lines
        ),
        legend=dict(title="Legend"),
    )
    if show_plotly:
        fig1.show()
    fig1.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/q/dq_dp_recon_q{q_psibar}_without_last_half_cycle_{num_crashes}_crashes.html")

    # Scatter of the reconstructed q slope over phase data
    fig2 = go.Figure()

    # Add reconstructed lines
    fig2.add_trace(go.Scatter(
        x=q_phase_recon_array_sustain,
        y=q_recon_array_sustain,
        mode='lines',
        name='Sustain',
        line=dict(color='red')
    ))

    fig2.add_trace(go.Scatter(
        x=q_phase_recon_array_non_sustain,
        y=q_recon_array_non_sustain,
        mode='lines',
        name='Non-Sustain',
        line=dict(color='blue')
    ))

    # Layout settings
    fig2.update_layout(
        title=f"q{q_psibar} Value Over Phase<br>Comparing Sustain and Non-Sustain for {num_crashes} Crashes\n{len(q_phase_array_sustain) + len(q_phase_array_non_sustain)} Points, {len(unique_shots)} Shots",
                    xaxis=dict(
            title="Phase",
            showgrid=True,  # Enable grid lines for the x-axis
            gridcolor="lightgray",  # Color of the grid lines
            gridwidth=1  # Thickness of the grid lines
        ),
        yaxis=dict(
            title=f"q{q_psibar} Value",
            showgrid=True,  # Enable grid lines for the y-axis
            gridcolor="lightgray",  # Color of the grid lines
            gridwidth=1  # Thickness of the grid lines
        ),
        legend=dict(title="Legend"),
    )
    if show_plotly:
        fig2.show()
    fig2.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/q/q_phase_recon_q{q_psibar}_without_last_half_cycle_{num_crashes}_crashes.html")
        
    return



def reconstruct_q_change_over_phase_without_last_half_cycle_crash_range_sustain_non_sustain(data_dir, num_phase_bins, q_psibar='min', min_crashes=0, max_crashes=100, matplotlib=True, plotly=False, show_plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    if q_psibar == 'min':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q_min_data.json")
    if q_psibar == '95':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q95_data.json")
    if q_psibar == '00':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q00_data.json")
    sustainment_dict = load.load_json_file("machine_settings_and_state/sustainment/sustainment.json")
    crash_dict = load.load_json_file("2024-10-10_19718-23016/crash_info_with_hardware_error.json")
    
    # plotting arrays
        # q and phase arrays
    q_array_sustain = []
    q_array_non_sustain = []
    q_phase_array_sustain = []
    q_phase_array_non_sustain = []
        # q and phase slope arrays
    q_slope_array_sustain = []
    q_slope_array_non_sustain = []
    q_phase_slope_array_sustain = []
    q_phase_slope_array_non_sustain = []
        # shot number arrays
    shot_numbers_slope_array_sustain = []
    shot_numbers_slope_array_non_sustain = []
    
    unique_shots = []
    
    # make arrays of thomson temperature data
    fig, ax = plt.subplots(figsize=(16,9))
    cur = 1
    tot = len(q_dict)
    for s in q_dict.keys():
        if s in crash_dict.keys() and s in sustainment_dict:
            if type(sustainment_dict[s]) != type(str()) and type(q_dict[s]) != type(str()) and type(crash_dict[s]) != type(str()):
                temp_data = load_data.load_json_file(data_dir + "crash_phase/phase_" + str(s) + ".json")
                if sustainment_dict[s] > 0 and len(crash_dict[s]['times']) >= min_crashes and len(crash_dict[s]['times']) <= max_crashes:
                    valid_q_points_shot=0
                    for i in range(len(q_dict[s]['data'])):
                        # get phase offset based on how many crashes have occurred
                        j = 0
                        while len(crash_dict[s]['times']) > j:
                            if crash_dict[s]['times'][j] < q_dict[s]['times'][i]:
                                j += 1
                            else:
                                break

                        cur_phase = convert_times_to_phases(temp_data, q_dict[s]['times'][i])
                        if cur_phase > 0.5 and j >= len(crash_dict[s]['times']):
                            continue
                        else:
                            q_array_sustain.append(q_dict[s]['data'][i])
                            q_phase_array_sustain.append(cur_phase + j)
                            valid_q_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_q_points_shot - 1):
                        q_slope_array_sustain.append((q_array_sustain[-(i+1)] - q_array_sustain[-i]) / (q_phase_array_sustain[-(i+1)] - q_phase_array_sustain[-i]))
                        q_phase_slope_array_sustain.append((q_phase_array_sustain[-(i+1)] + q_phase_array_sustain[-i]) / 2)
                        shot_numbers_slope_array_sustain.append(s)
                        
                    unique_shots.append(s)
                
                elif len(crash_dict[s]['times']) >= min_crashes and len(crash_dict[s]['times']) <= max_crashes:
                    valid_q_points_shot=0
                    for i in range(len(q_dict[s]['data'])):
                        # get phase offset based on how many crashes have occurred
                        j = 0
                        while len(crash_dict[s]['times']) > j:
                            if crash_dict[s]['times'][j] < q_dict[s]['times'][i]:
                                j += 1
                            else:
                                break
                        
                        cur_phase = convert_times_to_phases(temp_data, q_dict[s]['times'][i])
                        if cur_phase > 0.5 and j >= len(crash_dict[s]['times']):
                            continue
                        else:
                            q_array_non_sustain.append(q_dict[s]['data'][i])
                            q_phase_array_non_sustain.append(cur_phase + j)
                            valid_q_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_q_points_shot - 1):
                        q_slope_array_non_sustain.append((q_array_non_sustain[-(i+1)] - q_array_non_sustain[-i]) / (q_phase_array_non_sustain[-(i+1)] - q_phase_array_non_sustain[-i]))
                        q_phase_slope_array_non_sustain.append((q_phase_array_non_sustain[-(i+1)] + q_phase_array_non_sustain[-i]) / 2)
                        shot_numbers_slope_array_non_sustain.append(s)
                        
                    unique_shots.append(s)


            pb_pct(cur, tot)
            cur += 1

    # reconstruct thomson temp from slope data
        # get indices of sorted arrays
            # sustain
    q_slope_indices_sorted_by_phase_sustain = np.argsort(q_phase_slope_array_sustain)
    q_slope_array_sustain = [q_slope_array_sustain[i] for i in q_slope_indices_sorted_by_phase_sustain]
    q_phase_slope_array_sustain = [q_phase_slope_array_sustain[i] for i in q_slope_indices_sorted_by_phase_sustain]
    shot_numbers_slope_array_sustain = [shot_numbers_slope_array_sustain[i] for i in q_slope_indices_sorted_by_phase_sustain]
            # non sustain
    q_slope_indices_sorted_by_phase_non_sustain = np.argsort(q_phase_slope_array_non_sustain)
    q_slope_array_non_sustain = [q_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_phase_non_sustain]
    q_phase_slope_array_non_sustain = [q_phase_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_phase_non_sustain]
    shot_numbers_slope_array_non_sustain = [shot_numbers_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_phase_non_sustain]
    
        # get boundaries of bins
            # sustain
    bin_edges_phase_sustain = np.linspace(q_phase_slope_array_sustain[0], q_phase_slope_array_sustain[-1], num_phase_bins + 1)
            # non sustain
    bin_edges_phase_non_sustain = np.linspace(q_phase_slope_array_non_sustain[0], q_phase_slope_array_non_sustain[-1], num_phase_bins + 1)
    
    q_slope_means_sustain = []
    q_slope_means_non_sustain = []
    q_slope_phase_means_sustain = []
    q_slope_phase_means_non_sustain = []
    
    for i in range(len(bin_edges_phase_sustain) - 1):
        # sustain
        q_mean_sustain = median_of_bin(q_slope_array_sustain, q_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        q_slope_means_sustain.append(q_mean_sustain) if q_mean_sustain is not None else None
        q_p_mean_sustain = median_of_bin(q_phase_slope_array_sustain, q_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        q_slope_phase_means_sustain.append(q_p_mean_sustain) if q_p_mean_sustain is not None else None
        # non sustain
        q_mean_non_sustain = median_of_bin(q_slope_array_non_sustain, q_phase_slope_array_non_sustain, bin_edges_phase_non_sustain[i], bin_edges_phase_non_sustain[i+1])
        q_slope_means_non_sustain.append(q_mean_non_sustain) if q_mean_non_sustain is not None else None
        q_p_mean_non_sustain = median_of_bin(q_phase_slope_array_non_sustain, q_phase_slope_array_non_sustain, bin_edges_phase_non_sustain[i], bin_edges_phase_non_sustain[i+1])
        q_slope_phase_means_non_sustain.append(q_p_mean_non_sustain) if q_p_mean_non_sustain is not None else None
        
    # integrate
        # sustain
    q_recon_array_sustain = cumtrapz(q_slope_means_sustain, q_slope_phase_means_sustain, initial=0)
    q_phase_recon_array_sustain = q_slope_phase_means_sustain
        # non sustain
    q_recon_array_non_sustain = cumtrapz(q_slope_means_non_sustain, q_slope_phase_means_non_sustain, initial=0)
    q_phase_recon_array_non_sustain = q_slope_phase_means_non_sustain


    # zero out array
        # sustain
    for i in range(len(q_recon_array_sustain)):
        q_recon_array_sustain[i] = q_recon_array_sustain[i] - min(q_recon_array_sustain)
        
        # non sustain
    for i in range(len(q_recon_array_non_sustain)):
        q_recon_array_non_sustain[i] = q_recon_array_non_sustain[i] - min(q_recon_array_non_sustain)

    # offset array by c
        # sustain
    c = np.nanmean(q_array_sustain) - np.nanmean(q_recon_array_sustain)
    for i in range(len(q_recon_array_sustain)):
        q_recon_array_sustain[i] = q_recon_array_sustain[i] + c
        
        # non sustain
    c = np.nanmean(q_array_non_sustain) - np.nanmean(q_recon_array_non_sustain)
    for i in range(len(q_recon_array_non_sustain)):
        q_recon_array_non_sustain[i] = q_recon_array_non_sustain[i] + c
        


    if matplotlib:
        # Plots of Temperature over Phase
        #######################################################################################################

        # scatter of the thomson slope over phase data
            # scatter
        plt.scatter(q_phase_slope_array_sustain, q_slope_array_sustain, color='r', marker='.', alpha=0.3, label=r"\frac{dT}{dp} of Sustain Shots")
        plt.scatter(q_phase_slope_array_non_sustain, q_slope_array_non_sustain, color='b', marker='.', alpha=0.3, label=r"\frac{dT}{dp} of Non-Sustain Shots")
            # lines
        plt.plot(q_slope_phase_means_sustain, q_slope_means_sustain, color='r', label='Median of Sustain Shots')
        plt.plot(q_slope_phase_means_non_sustain, q_slope_means_non_sustain, color='b', label='Median of Non-Sustain Shots')
        plt.title(r"$\frac{dq}{dp}$ Over Phase" + f"at q{q_psibar}\n{min_crashes}-{max_crashes} Crashes // {len(q_phase_slope_array_sustain)+len(q_phase_slope_array_non_sustain)} Points")
        plt.xlabel("Phase")
        plt.ylabel(r"$\frac{dq}{dp}$")
        plt.grid(True)
        plt.legend()
        plt.show()
        
        # scatter of the reconstructed thomson slope over phase data
        plt.plot(q_phase_recon_array_sustain, q_recon_array_sustain, color='r', label='Sustain')
        plt.plot(q_phase_recon_array_non_sustain, q_recon_array_non_sustain, color='b', label='Non-Sustain')
        plt.title(f"q{q_psibar} Value Over Phase\nComparing Sustain and Non-Sustain for {min_crashes}-{max_crashes} Crashes")
        plt.xlabel("Phase")
        plt.ylabel(f"q{q_psibar}")
        plt.grid(True)
        plt.legend()
        plt.show()
    
    if plotly:
        # Scatter of the q slope over phase data
        fig1 = go.Figure()

        # Add scatter points
        fig1.add_trace(go.Scatter(
            x=q_phase_slope_array_sustain,
            y=q_slope_array_sustain,
            mode='markers',
            name="dq/dp of Sustain Shots",
            marker=dict(color='red', opacity=0.3),
            text=shot_numbers_slope_array_sustain
        ))

        fig1.add_trace(go.Scatter(
            x=q_phase_slope_array_non_sustain,
            y=q_slope_array_non_sustain,
            mode='markers',
            name="dq/dp of Non-Sustain Shots",
            marker=dict(color='blue', opacity=0.3),
            text=shot_numbers_slope_array_non_sustain
        ))

        # Add median lines
        fig1.add_trace(go.Scatter(
            x=q_slope_phase_means_sustain,
            y=q_slope_means_sustain,
            mode='lines',
            name='Median of Sustain Shots',
            line=dict(color='red')
        ))

        fig1.add_trace(go.Scatter(
            x=q_slope_phase_means_non_sustain,
            y=q_slope_means_non_sustain,
            mode='lines',
            name='Median of Non-Sustain Shots',
            line=dict(color='blue')
        ))

        # Layout settings
        fig1.update_layout(
            title=f"dq/dp Over Phase at q{q_psibar}<br>{min_crashes}-{max_crashes} Crashes\n{len(q_phase_slope_array_sustain) + len(q_phase_slope_array_non_sustain)} Points, {len(unique_shots)} Shots",
                        xaxis=dict(
                title="Phase",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(
                title="dq/dp",
                showgrid=True,  # Enable grid lines for the y-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            legend=dict(title="Legend"),
        )
        if show_plotly:
            fig1.show()
        fig1.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/q/dq_dp_recon_q{q_psibar}_without_last_half_cycle.html")

        # Scatter of the reconstructed q slope over phase data
        fig2 = go.Figure()

        # Add reconstructed lines
        fig2.add_trace(go.Scatter(
            x=q_phase_recon_array_sustain,
            y=q_recon_array_sustain,
            mode='lines',
            name='Sustain',
            line=dict(color='red')
        ))

        fig2.add_trace(go.Scatter(
            x=q_phase_recon_array_non_sustain,
            y=q_recon_array_non_sustain,
            mode='lines',
            name='Non-Sustain',
            line=dict(color='blue')
        ))

        # Layout settings
        fig2.update_layout(
            title=f"q{q_psibar} Value Over Phase<br>Comparing Sustain and Non-Sustain for {min_crashes}-{max_crashes} Crashes\n{len(q_phase_array_sustain) + len(q_phase_array_non_sustain)} Points, {len(unique_shots)} Shots",
                        xaxis=dict(
                title="Phase",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(
                title=f"q{q_psibar} Value",
                showgrid=True,  # Enable grid lines for the y-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            legend=dict(title="Legend"),
        )
        if show_plotly:
            fig2.show()
        fig2.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/q/q_phase_recon_q{q_psibar}_without_last_half_cycle.html")
        
    return




def reconstruct_q_change_over_norm_time_crash_range_sustain_non_sustain(data_dir, num_norm_time_bins, q_psibar='min', min_crashes=0, max_crashes=100, matplotlib=True, plotly=False, show_plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    if q_psibar == 'min':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q_min_data.json")
    if q_psibar == '95':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q95_data.json")
    if q_psibar == '00':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q00_data.json")
    sustainment_dict = load.load_json_file("machine_settings_and_state/sustainment/sustainment.json")
    crash_dict = load.load_json_file("2024-10-10_19718-23016/crash_info_with_hardware_error.json")
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    # plotting arrays
        # q and norm_time arrays
    q_array_sustain = []
    q_array_non_sustain = []
    q_norm_time_array_sustain = []
    q_norm_time_array_non_sustain = []
        # q and norm_time slope arrays
    q_slope_array_sustain = []
    q_slope_array_non_sustain = []
    q_norm_time_slope_array_sustain = []
    q_norm_time_slope_array_non_sustain = []
        # shots
    shot_numbers_slope_array_sustain = []
    shot_numbers_slope_array_non_sustain = []
    
    unique_shots = []
    
    # make arrays of thomson temperature data
    fig, ax = plt.subplots(figsize=(16,9))
    cur = 1
    tot = len(q_dict)
    for s in q_dict.keys():
        if s in crash_dict.keys() and s in sustainment_dict:
            if type(str()) not in [type(sustainment_dict[s]), type(q_dict[s]), type(crash_dict[s]), type(lifetimes_dict[s])]:
                if sustainment_dict[s] > 0 and len(crash_dict[s]['times']) >= min_crashes and len(crash_dict[s]['times']) <= max_crashes:
                    valid_q_points_shot=0
                    for i in range(len(q_dict[s]['data'])):
                        q_array_sustain.append(q_dict[s]['data'][i])
                        # get norm_time offset based on how many crashes have occurred
                        j = 0
                        while len(crash_dict[s]['times']) > j:
                            if crash_dict[s]['times'][j] < q_dict[s]['times'][i]:
                                j += 1
                            else:
                                break
                        
                        q_norm_time_array_sustain.append((i+1)/1000 / lifetimes_dict[s])
                        valid_q_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_q_points_shot - 1):
                        q_slope_array_sustain.append((q_array_sustain[-(i+1)] - q_array_sustain[-i]) / (q_norm_time_array_sustain[-(i+1)] - q_norm_time_array_sustain[-i]))
                        q_norm_time_slope_array_sustain.append((q_norm_time_array_sustain[-(i+1)] + q_norm_time_array_sustain[-i]) / 2)
                        shot_numbers_slope_array_sustain.append(s)
                        
                    unique_shots.append(s)
                
                elif len(crash_dict[s]['times']) >= min_crashes and len(crash_dict[s]['times']) <= max_crashes:
                    valid_q_points_shot=0
                    for i in range(len(q_dict[s]['data'])):
                        q_array_non_sustain.append(q_dict[s]['data'][i])
                        # get norm_time offset based on how many crashes have occurred
                        j = 0
                        while len(crash_dict[s]['times']) > j:
                            if crash_dict[s]['times'][j] < q_dict[s]['times'][i]:
                                j += 1
                            else:
                                break
                        
                        q_norm_time_array_non_sustain.append((i+1)/1000 / lifetimes_dict[s])
                        valid_q_points_shot += 1
                    
                        
                    # make array of all slopes
                    for i in range(valid_q_points_shot - 1):
                        q_slope_array_non_sustain.append((q_array_non_sustain[-(i+1)] - q_array_non_sustain[-i]) / (q_norm_time_array_non_sustain[-(i+1)] - q_norm_time_array_non_sustain[-i]))
                        q_norm_time_slope_array_non_sustain.append((q_norm_time_array_non_sustain[-(i+1)] + q_norm_time_array_non_sustain[-i]) / 2)
                        shot_numbers_slope_array_non_sustain.append(s)
                        
                    unique_shots.append(s)

            pb_pct(cur, tot)
            cur += 1

    # reconstruct thomson temp from slope data
        # get indices of sorted arrays
            # sustain
    q_slope_indices_sorted_by_norm_time_sustain = np.argsort(q_norm_time_slope_array_sustain)
    q_slope_array_sustain = [q_slope_array_sustain[i] for i in q_slope_indices_sorted_by_norm_time_sustain]
    q_norm_time_slope_array_sustain = [q_norm_time_slope_array_sustain[i] for i in q_slope_indices_sorted_by_norm_time_sustain]
    shot_numbers_slope_array_sustain = [shot_numbers_slope_array_sustain[i] for i in q_slope_indices_sorted_by_norm_time_sustain]
            # non sustain
    q_slope_indices_sorted_by_norm_time_non_sustain = np.argsort(q_norm_time_slope_array_non_sustain)
    q_slope_array_non_sustain = [q_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_norm_time_non_sustain]
    q_norm_time_slope_array_non_sustain = [q_norm_time_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_norm_time_non_sustain]
    shot_numbers_slope_array_non_sustain = [shot_numbers_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_norm_time_non_sustain]

    
    
        # get boundaries of bins
            # sustain
    bin_edges_norm_time_sustain = np.linspace(q_norm_time_slope_array_sustain[0], q_norm_time_slope_array_sustain[-1], num_norm_time_bins + 1)
            # non sustain
    bin_edges_norm_time_non_sustain = np.linspace(q_norm_time_slope_array_non_sustain[0], q_norm_time_slope_array_non_sustain[-1], num_norm_time_bins + 1)
    
    q_slope_means_sustain = []
    q_slope_means_non_sustain = []
    q_slope_norm_time_means_sustain = []
    q_slope_norm_time_means_non_sustain = []
    
    for i in range(len(bin_edges_norm_time_sustain) - 1):
        # sustain
        q_mean_sustain = median_of_bin(q_slope_array_sustain, q_norm_time_slope_array_sustain, bin_edges_norm_time_sustain[i], bin_edges_norm_time_sustain[i+1])
        q_slope_means_sustain.append(q_mean_sustain) if q_mean_sustain is not None else None
        q_p_mean_sustain = median_of_bin(q_norm_time_slope_array_sustain, q_norm_time_slope_array_sustain, bin_edges_norm_time_sustain[i], bin_edges_norm_time_sustain[i+1])
        q_slope_norm_time_means_sustain.append(q_p_mean_sustain) if q_p_mean_sustain is not None else None
        # non sustain
        q_mean_non_sustain = median_of_bin(q_slope_array_non_sustain, q_norm_time_slope_array_non_sustain, bin_edges_norm_time_non_sustain[i], bin_edges_norm_time_non_sustain[i+1])
        q_slope_means_non_sustain.append(q_mean_non_sustain) if q_mean_non_sustain is not None else None
        q_p_mean_non_sustain = median_of_bin(q_norm_time_slope_array_non_sustain, q_norm_time_slope_array_non_sustain, bin_edges_norm_time_non_sustain[i], bin_edges_norm_time_non_sustain[i+1])
        q_slope_norm_time_means_non_sustain.append(q_p_mean_non_sustain) if q_p_mean_non_sustain is not None else None
        
    # integrate
        # sustain
    q_recon_array_sustain = cumtrapz(q_slope_means_sustain, q_slope_norm_time_means_sustain, initial=0)
    q_norm_time_recon_array_sustain = q_slope_norm_time_means_sustain
        # non sustain
    q_recon_array_non_sustain = cumtrapz(q_slope_means_non_sustain, q_slope_norm_time_means_non_sustain, initial=0)
    q_norm_time_recon_array_non_sustain = q_slope_norm_time_means_non_sustain


    # zero out array
        # sustain
    for i in range(len(q_recon_array_sustain)):
        q_recon_array_sustain[i] = q_recon_array_sustain[i] - min(q_recon_array_sustain)
        
        # non sustain
    for i in range(len(q_recon_array_non_sustain)):
        q_recon_array_non_sustain[i] = q_recon_array_non_sustain[i] - min(q_recon_array_non_sustain)

    # offset array by c
        # sustain
    c = np.nanmean(q_array_sustain) - np.nanmean(q_recon_array_sustain)
    for i in range(len(q_recon_array_sustain)):
        q_recon_array_sustain[i] = q_recon_array_sustain[i] + c
        
        # non sustain
    c = np.nanmean(q_array_non_sustain) - np.nanmean(q_recon_array_non_sustain)
    for i in range(len(q_recon_array_non_sustain)):
        q_recon_array_non_sustain[i] = q_recon_array_non_sustain[i] + c
        


    if matplotlib:
        # Plots of Temperature over norm_time
        #######################################################################################################

        # scatter of the thomson slope over norm_time data
            # scatter
        plt.scatter(q_norm_time_slope_array_sustain, q_slope_array_sustain, color='r', marker='.', alpha=0.3, label=r"\frac{dq}{dt} of Sustain Shots")
        plt.scatter(q_norm_time_slope_array_non_sustain, q_slope_array_non_sustain, color='b', marker='.', alpha=0.3, label=r"\frac{dq}{dt} of Non-Sustain Shots")
            # lines
        plt.plot(q_slope_norm_time_means_sustain, q_slope_means_sustain, color='r', label='Median of Sustain Shots')
        plt.plot(q_slope_norm_time_means_non_sustain, q_slope_means_non_sustain, color='b', label='Median of Non-Sustain Shots')
        plt.title(r"$\frac{dq}{dt}$ Over Normalized Time" + f"\n{min_crashes}-{max_crashes} Crashes // {len(q_norm_time_slope_array_sustain)+len(q_norm_time_slope_array_non_sustain)} Points")
        plt.xlabel("Normalized Time")
        plt.ylabel(r"$\frac{dq}{dt}$")
        plt.grid(True)
        plt.legend()
        plt.show()
        
        # scatter of the reconstructed thomson slope over norm_time data
        plt.plot(q_norm_time_recon_array_sustain, q_recon_array_sustain, color='r', label='Sustain')
        plt.plot(q_norm_time_recon_array_non_sustain, q_recon_array_non_sustain, color='b', label='Non-Sustain')
        plt.title(f"q{q_psibar} Over Normalized Time\nComparing Sustain and Non-Sustain for {min_crashes}-{max_crashes} Crashes")
        plt.xlabel("norm_time")
        plt.ylabel(f"q{q_psibar}")
        plt.grid(True)
        plt.legend()
        plt.show()
    
    if plotly:
        # Scatter of the q slope over norm_time data
        fig1 = go.Figure()

        # Add scatter points
        fig1.add_trace(go.Scatter(
            x=q_norm_time_slope_array_sustain,
            y=q_slope_array_sustain,
            mode='markers',
            name="dq/dp of Sustain Shots",
            marker=dict(color='red', opacity=0.3),
            text=shot_numbers_slope_array_sustain
        ))

        fig1.add_trace(go.Scatter(
            x=q_norm_time_slope_array_non_sustain,
            y=q_slope_array_non_sustain,
            mode='markers',
            name="dq/dp of Non-Sustain Shots",
            marker=dict(color='blue', opacity=0.3),
            text=shot_numbers_slope_array_non_sustain
        ))

        # Add median lines
        fig1.add_trace(go.Scatter(
            x=q_slope_norm_time_means_sustain,
            y=q_slope_means_sustain,
            mode='lines',
            name='Median of Sustain Shots',
            line=dict(color='red')
        ))

        fig1.add_trace(go.Scatter(
            x=q_slope_norm_time_means_non_sustain,
            y=q_slope_means_non_sustain,
            mode='lines',
            name='Median of Non-Sustain Shots',
            line=dict(color='blue')
        ))

        # Layout settings
        fig1.update_layout(
            title=f"dq/dp at q{q_psibar} Over Normalized Time<br>{min_crashes}-{max_crashes} Crashes\n{len(q_norm_time_slope_array_sustain) + len(q_norm_time_slope_array_non_sustain)} Points, {len(unique_shots)} Shots",
            xaxis=dict(
                title="Normalized Time",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(
                title="dq/dt",
                showgrid=True,  # Enable grid lines for the y-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            legend=dict(title="Legend"),
        )
        if show_plotly:
            fig1.show()
        fig1.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/q/dq_dt_recon_q{q_psibar}.html")

        # Scatter of the reconstructed q slope over norm_time data
        fig2 = go.Figure()

        # Add reconstructed lines
        fig2.add_trace(go.Scatter(
            x=q_norm_time_recon_array_sustain,
            y=q_recon_array_sustain,
            mode='lines',
            name='Sustain',
            line=dict(color='red')
        ))

        fig2.add_trace(go.Scatter(
            x=q_norm_time_recon_array_non_sustain,
            y=q_recon_array_non_sustain,
            mode='lines',
            name='Non-Sustain',
            line=dict(color='blue')
        ))

        # Layout settings
        fig2.update_layout(
            title=f"q{q_psibar} Value Over Normalized Time<br>Comparing Sustain and Non-Sustain for {min_crashes}-{max_crashes} Crashes\n{len(q_norm_time_slope_array_sustain) + len(q_norm_time_slope_array_non_sustain)} Points, {len(unique_shots)} Shots",
            xaxis=dict(
                title="Normalized Time",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(
                title=f"q{q_psibar} Value",
                showgrid=True,  # Enable grid lines for the y-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            legend=dict(title="Legend"),
        )
        if show_plotly:
            fig2.show()
        fig2.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/q/q_norm_time_recon_q{q_psibar}.html")
        
    return




def reconstruct_q_change_over_phase_crash_range_sustain_non_sustain(data_dir, num_phase_bins, q_psibar='min', min_crashes=0, max_crashes=100, matplotlib=True, plotly=False, show_plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data
    if q_psibar == 'min':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q_min_data.json")
    if q_psibar == '95':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q95_data.json")
    if q_psibar == '00':
        q_dict = load.load_json_file("plasma_data_and_parameters/q_profile/q00_data.json")
    sustainment_dict = load.load_json_file("machine_settings_and_state/sustainment/sustainment.json")
    crash_dict = load.load_json_file("2024-10-10_19718-23016/crash_info_with_hardware_error.json")
    
    # plotting arrays
        # q and phase arrays
    q_array_sustain = []
    q_array_non_sustain = []
    q_phase_array_sustain = []
    q_phase_array_non_sustain = []
        # q and phase slope arrays
    q_slope_array_sustain = []
    q_slope_array_non_sustain = []
    q_phase_slope_array_sustain = []
    q_phase_slope_array_non_sustain = []
        # shot number arrays
    shot_numbers_slope_array_sustain = []
    shot_numbers_slope_array_non_sustain = []
    
    unique_shots = []
    
    # make arrays of thomson temperature data
    fig, ax = plt.subplots(figsize=(16,9))
    cur = 1
    tot = len(q_dict)
    for s in q_dict.keys():
        if s in crash_dict.keys() and s in sustainment_dict:
            if type(sustainment_dict[s]) != type(str()) and type(q_dict[s]) != type(str()) and type(crash_dict[s]) != type(str()):
                temp_data = load_data.load_json_file(data_dir + "crash_phase/phase_" + str(s) + ".json")
                if sustainment_dict[s] > 0 and len(crash_dict[s]['times']) >= min_crashes and len(crash_dict[s]['times']) <= max_crashes:
                    valid_q_points_shot=0
                    for i in range(len(q_dict[s]['data'])):
                        q_array_sustain.append(q_dict[s]['data'][i])
                        # get phase offset based on how many crashes have occurred
                        j = 0
                        while len(crash_dict[s]['times']) > j:
                            if crash_dict[s]['times'][j] < q_dict[s]['times'][i]:
                                j += 1
                            else:
                                break
                        
                        q_phase_array_sustain.append(convert_times_to_phases(temp_data, q_dict[s]['times'][i]) + j)
                        valid_q_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_q_points_shot - 1):
                        q_slope_array_sustain.append((q_array_sustain[-(i+1)] - q_array_sustain[-i]) / (q_phase_array_sustain[-(i+1)] - q_phase_array_sustain[-i]))
                        q_phase_slope_array_sustain.append((q_phase_array_sustain[-(i+1)] + q_phase_array_sustain[-i]) / 2)
                        shot_numbers_slope_array_sustain.append(s)
                        
                    unique_shots.append(s)
                
                elif len(crash_dict[s]['times']) >= min_crashes and len(crash_dict[s]['times']) <= max_crashes:
                    valid_q_points_shot=0
                    for i in range(len(q_dict[s]['data'])):
                        q_array_non_sustain.append(q_dict[s]['data'][i])
                        # get phase offset based on how many crashes have occurred
                        j = 0
                        while len(crash_dict[s]['times']) > j:
                            if crash_dict[s]['times'][j] < q_dict[s]['times'][i]:
                                j += 1
                            else:
                                break
                        
                        q_phase_array_non_sustain.append(convert_times_to_phases(temp_data, q_dict[s]['times'][i]) + j)
                        valid_q_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_q_points_shot - 1):
                        q_slope_array_non_sustain.append((q_array_non_sustain[-(i+1)] - q_array_non_sustain[-i]) / (q_phase_array_non_sustain[-(i+1)] - q_phase_array_non_sustain[-i]))
                        q_phase_slope_array_non_sustain.append((q_phase_array_non_sustain[-(i+1)] + q_phase_array_non_sustain[-i]) / 2)
                        shot_numbers_slope_array_non_sustain.append(s)
                        
                    unique_shots.append(s)


            pb_pct(cur, tot)
            cur += 1

    # reconstruct thomson temp from slope data
        # get indices of sorted arrays
            # sustain
    q_slope_indices_sorted_by_phase_sustain = np.argsort(q_phase_slope_array_sustain)
    q_slope_array_sustain = [q_slope_array_sustain[i] for i in q_slope_indices_sorted_by_phase_sustain]
    q_phase_slope_array_sustain = [q_phase_slope_array_sustain[i] for i in q_slope_indices_sorted_by_phase_sustain]
    shot_numbers_slope_array_sustain = [shot_numbers_slope_array_sustain[i] for i in q_slope_indices_sorted_by_phase_sustain]
            # non sustain
    q_slope_indices_sorted_by_phase_non_sustain = np.argsort(q_phase_slope_array_non_sustain)
    q_slope_array_non_sustain = [q_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_phase_non_sustain]
    q_phase_slope_array_non_sustain = [q_phase_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_phase_non_sustain]
    shot_numbers_slope_array_non_sustain = [shot_numbers_slope_array_non_sustain[i] for i in q_slope_indices_sorted_by_phase_non_sustain]
    
        # get boundaries of bins
            # sustain
    bin_edges_phase_sustain = np.linspace(q_phase_slope_array_sustain[0], q_phase_slope_array_sustain[-1], num_phase_bins + 1)
            # non sustain
    bin_edges_phase_non_sustain = np.linspace(q_phase_slope_array_non_sustain[0], q_phase_slope_array_non_sustain[-1], num_phase_bins + 1)
    
    q_slope_means_sustain = []
    q_slope_means_non_sustain = []
    q_slope_phase_means_sustain = []
    q_slope_phase_means_non_sustain = []
    
    for i in range(len(bin_edges_phase_sustain) - 1):
        # sustain
        q_mean_sustain = median_of_bin(q_slope_array_sustain, q_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        q_slope_means_sustain.append(q_mean_sustain) if q_mean_sustain is not None else None
        q_p_mean_sustain = median_of_bin(q_phase_slope_array_sustain, q_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        q_slope_phase_means_sustain.append(q_p_mean_sustain) if q_p_mean_sustain is not None else None
        # non sustain
        q_mean_non_sustain = median_of_bin(q_slope_array_non_sustain, q_phase_slope_array_non_sustain, bin_edges_phase_non_sustain[i], bin_edges_phase_non_sustain[i+1])
        q_slope_means_non_sustain.append(q_mean_non_sustain) if q_mean_non_sustain is not None else None
        q_p_mean_non_sustain = median_of_bin(q_phase_slope_array_non_sustain, q_phase_slope_array_non_sustain, bin_edges_phase_non_sustain[i], bin_edges_phase_non_sustain[i+1])
        q_slope_phase_means_non_sustain.append(q_p_mean_non_sustain) if q_p_mean_non_sustain is not None else None
        
    # integrate
        # sustain
    q_recon_array_sustain = cumtrapz(q_slope_means_sustain, q_slope_phase_means_sustain, initial=0)
    q_phase_recon_array_sustain = q_slope_phase_means_sustain
        # non sustain
    q_recon_array_non_sustain = cumtrapz(q_slope_means_non_sustain, q_slope_phase_means_non_sustain, initial=0)
    q_phase_recon_array_non_sustain = q_slope_phase_means_non_sustain


    # zero out array
        # sustain
    for i in range(len(q_recon_array_sustain)):
        q_recon_array_sustain[i] = q_recon_array_sustain[i] - min(q_recon_array_sustain)
        
        # non sustain
    for i in range(len(q_recon_array_non_sustain)):
        q_recon_array_non_sustain[i] = q_recon_array_non_sustain[i] - min(q_recon_array_non_sustain)

    # offset array by c
        # sustain
    c = np.nanmean(q_array_sustain) - np.nanmean(q_recon_array_sustain)
    for i in range(len(q_recon_array_sustain)):
        q_recon_array_sustain[i] = q_recon_array_sustain[i] + c
        
        # non sustain
    c = np.nanmean(q_array_non_sustain) - np.nanmean(q_recon_array_non_sustain)
    for i in range(len(q_recon_array_non_sustain)):
        q_recon_array_non_sustain[i] = q_recon_array_non_sustain[i] + c
        


    if matplotlib:
        # Plots of Temperature over Phase
        #######################################################################################################

        # scatter of the thomson slope over phase data
            # scatter
        plt.scatter(q_phase_slope_array_sustain, q_slope_array_sustain, color='r', marker='.', alpha=0.3, label=r"\frac{dT}{dp} of Sustain Shots")
        plt.scatter(q_phase_slope_array_non_sustain, q_slope_array_non_sustain, color='b', marker='.', alpha=0.3, label=r"\frac{dT}{dp} of Non-Sustain Shots")
            # lines
        plt.plot(q_slope_phase_means_sustain, q_slope_means_sustain, color='r', label='Median of Sustain Shots')
        plt.plot(q_slope_phase_means_non_sustain, q_slope_means_non_sustain, color='b', label='Median of Non-Sustain Shots')
        plt.title(r"$\frac{dq}{dp}$ Over Phase" + f"at q{q_psibar}\n{min_crashes}-{max_crashes} Crashes // {len(q_phase_slope_array_sustain)+len(q_phase_slope_array_non_sustain)} Points")
        plt.xlabel("Phase")
        plt.ylabel(r"$\frac{dq}{dp}$")
        plt.grid(True)
        plt.legend()
        plt.show()
        
        # scatter of the reconstructed thomson slope over phase data
        plt.plot(q_phase_recon_array_sustain, q_recon_array_sustain, color='r', label='Sustain')
        plt.plot(q_phase_recon_array_non_sustain, q_recon_array_non_sustain, color='b', label='Non-Sustain')
        plt.title(f"q{q_psibar} Value Over Phase\nComparing Sustain and Non-Sustain for {min_crashes}-{max_crashes} Crashes")
        plt.xlabel("Phase")
        plt.ylabel(f"q{q_psibar}")
        plt.grid(True)
        plt.legend()
        plt.show()
    
    if plotly:
        # Scatter of the q slope over phase data
        fig1 = go.Figure()

        # Add scatter points
        fig1.add_trace(go.Scatter(
            x=q_phase_slope_array_sustain,
            y=q_slope_array_sustain,
            mode='markers',
            name="dq/dp of Sustain Shots",
            marker=dict(color='red', opacity=0.3),
            text=shot_numbers_slope_array_sustain
        ))

        fig1.add_trace(go.Scatter(
            x=q_phase_slope_array_non_sustain,
            y=q_slope_array_non_sustain,
            mode='markers',
            name="dq/dp of Non-Sustain Shots",
            marker=dict(color='blue', opacity=0.3),
            text=shot_numbers_slope_array_non_sustain
        ))

        # Add median lines
        fig1.add_trace(go.Scatter(
            x=q_slope_phase_means_sustain,
            y=q_slope_means_sustain,
            mode='lines',
            name='Median of Sustain Shots',
            line=dict(color='red')
        ))

        fig1.add_trace(go.Scatter(
            x=q_slope_phase_means_non_sustain,
            y=q_slope_means_non_sustain,
            mode='lines',
            name='Median of Non-Sustain Shots',
            line=dict(color='blue')
        ))

        # Layout settings
        fig1.update_layout(
            title=f"dq/dp Over Phase at q{q_psibar}<br>{min_crashes}-{max_crashes} Crashes\n{len(q_phase_slope_array_sustain) + len(q_phase_slope_array_non_sustain)} Points, {len(unique_shots)} Shots",
                        xaxis=dict(
                title="Phase",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(
                title="dq/dp",
                showgrid=True,  # Enable grid lines for the y-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            legend=dict(title="Legend"),
        )
        if show_plotly:
            fig1.show()
        fig1.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/q/dq_dp_recon_q{q_psibar}.html")

        # Scatter of the reconstructed q slope over phase data
        fig2 = go.Figure()

        # Add reconstructed lines
        fig2.add_trace(go.Scatter(
            x=q_phase_recon_array_sustain,
            y=q_recon_array_sustain,
            mode='lines',
            name='Sustain',
            line=dict(color='red')
        ))

        fig2.add_trace(go.Scatter(
            x=q_phase_recon_array_non_sustain,
            y=q_recon_array_non_sustain,
            mode='lines',
            name='Non-Sustain',
            line=dict(color='blue')
        ))

        # Layout settings
        fig2.update_layout(
            title=f"q{q_psibar} Value Over Phase<br>Comparing Sustain and Non-Sustain for {min_crashes}-{max_crashes} Crashes\n{len(q_phase_array_sustain) + len(q_phase_array_non_sustain)} Points, {len(unique_shots)} Shots",
                        xaxis=dict(
                title="Phase",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(
                title=f"q{q_psibar} Value",
                showgrid=True,  # Enable grid lines for the y-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            legend=dict(title="Legend"),
        )
        if show_plotly:
            fig2.show()
        fig2.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/q/q_phase_recon_q{q_psibar}.html")
        
    return



def plot_q_scatter_crashes(crash_dir, min_lifetime=0.01, only_largest_crash=True, end_exclusion=2, plot_means=False, matplotlib=True, plotly=False):
    q_min_data = load.load_json_file("plasma_data_and_parameters/q_profile/q_min_data.json")
    crash_data = load.load_json_file(f"{crash_dir}/crash_info_with_hardware_error.json")
    lifetime_data = load.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    crash_keys = crash_data.keys()
    lifetime_keys = lifetime_data.keys()
    
    times_crashes = []
    times_non_crashes = []
    
    dq_crashes = []
    dq_non_crashes = []
    
    shots_crashes = []
    shots_non_crashes = []
    
    labels_crashes = []
    labels_non_crashes = []
    
    cur_num = 1
    total_num = len(q_min_data)
    non_crash=True
    for shot in q_min_data.keys():
        if shot in crash_keys and shot in lifetime_keys:
            if type(str()) not in [type(crash_data[shot]), type(q_min_data[shot]), type(lifetime_data[shot])] and len(crash_data[shot]['times']) > 0 and lifetime_data[shot] > min_lifetime:
                for i in range(max(len(q_min_data[shot]['data']) - (1+end_exclusion), 0)):
                    if only_largest_crash:
                        time_largest_crash = crash_data[shot]['times'][np.argmax(crash_data[shot]['times'])]
                        if time_largest_crash < q_min_data[shot]['times'][i+1] and time_largest_crash > q_min_data[shot]['times'][i]:
                            times_crashes.append(time_largest_crash)
                            dq_crashes.append(interp_q_time(q_min_data[shot]['data'], time_largest_crash + 0.0005) - interp_q_time(q_min_data[shot]['data'], time_largest_crash - 0.0005))
                            shots_crashes.append(shot)
                            labels_crashes.append(f"{shot}: {t*1000:.2g}ms")
                        else:
                            for t in crash_data[shot]['times']:
                                if t < q_min_data[shot]['times'][i+1] and t > q_min_data[shot]['times'][i]:
                                    non_crash=False
                            if non_crash:
                                times_non_crashes.append(i/1000+0.0015)
                                dq_non_crashes.append(q_min_data[shot]['data'][i+1] - q_min_data[shot]['data'][i])
                                shots_non_crashes.append(shot)
                                labels_non_crashes.append(f"{shot}: {i+1.5}ms")
                            non_crash=True
                    
                    else:
                        for t in crash_data[shot]['times']:
                            if t < q_min_data[shot]['times'][i+1] and t > q_min_data[shot]['times'][i]:
                                times_crashes.append(t)
                                dq_crashes.append(interp_q_time(q_min_data[shot]['data'], t + 0.0005) - interp_q_time(q_min_data[shot]['data'], t - 0.0005))
                                shots_crashes.append(shot)
                                labels_crashes.append(f"{shot}: {t*1000:.2g}ms")
                                non_crash=False
                            if non_crash:
                                times_non_crashes.append(i/1000+0.0015)
                                dq_non_crashes.append(q_min_data[shot]['data'][i+1] - q_min_data[shot]['data'][i])
                                shots_non_crashes.append(shot)
                                labels_non_crashes.append(f"{shot}: {i+1.5}ms")
                            non_crash=True

        pb_pct(cur_num, total_num)
        cur_num += 1

    if matplotlib:
        fig, axs = plt.subplots()
        scatter_non_crashes = plt.scatter(times_non_crashes, dq_non_crashes, c='b', alpha=0.1, s=20, picker=5, label="Non-Crashes Scatter")
        scatter_crashes = plt.scatter(times_crashes, dq_crashes, c='r', alpha=0.2, s=20, marker='x', picker=5, label="Crashes")
        plt.hlines([0], 0, 35/1000, 'k', linewidth=1)
        plt.title("Changes in Minimum q value in 1ms Intervals Over Crashes and non Crashes")
        plt.ylabel("Change in Minimum q")
        plt.xlabel("Time [s]")
        
        # add in binned means
        if plot_means:
            t_non_crashes_means, dq_non_crashes_means = binned_means(times_non_crashes, dq_non_crashes, 0.001)
            t_crashes_means, dq_crashes_means = binned_means(times_crashes, dq_crashes, 0.001)
            plt.plot(t_non_crashes_means, dq_non_crashes_means, c='b', linestyle='-', marker='o', label="Non-Crashes Mean")
            plt.plot(t_crashes_means, dq_crashes_means, c='r', linestyle='-', marker='x', label="Crashes Mean")
        
        cursors.add_cursors_to_scatter(scatter_crashes, labels_crashes)
        cursors.add_cursors_to_scatter(scatter_non_crashes, labels_non_crashes)
        
        click.add_click_action_axuv_q_ts(scatter_crashes, fig, shots_crashes)
        click.add_click_action_axuv_q_ts(scatter_non_crashes, fig, shots_non_crashes)
        
        plt.legend()
        
        plt.show()
        
    if plotly:
        # Create the figure
        fig = go.Figure()

        # Add scatter plots for crashes and non-crashes
        fig.add_trace(go.Scatter(
            x=times_non_crashes,
            y=dq_non_crashes,
            mode='markers',
            marker=dict(color='blue', opacity=0.1, size=8),
            name="Non-Crashes Scatter",
            text=labels_non_crashes  # Add labels as hover text
        ))

        fig.add_trace(go.Scatter(
            x=times_crashes,
            y=dq_crashes,
            mode='markers',
            marker=dict(color='red', opacity=0.2, size=8, symbol='x'),
            name="Crashes Scatter",
            text=labels_crashes  # Add labels as hover text
        ))

        # Add a horizontal line at y=0
        fig.add_trace(go.Scatter(
            x=[0, 35 / 1000],
            y=[0, 0],
            mode='lines',
            line=dict(color='black', width=1),
            showlegend=False
        ))

        # Add binned means if enabled
        if plot_means:
            t_non_crashes_means, dq_non_crashes_means = binned_means(times_non_crashes, dq_non_crashes, 0.001)
            t_crashes_means, dq_crashes_means = binned_means(times_crashes, dq_crashes, 0.001)
            fig.add_trace(go.Scatter(
                x=t_non_crashes_means,
                y=dq_non_crashes_means,
                mode='lines+markers',
                line=dict(color='blue', dash='solid'),
                marker=dict(symbol='circle'),
                name="Non-Crashes Mean"
            ))

            fig.add_trace(go.Scatter(
                x=t_crashes_means,
                y=dq_crashes_means,
                mode='lines+markers',
                line=dict(color='red', dash='solid'),
                marker=dict(symbol='x'),
                name="Crashes Mean"
            ))

        # Update layout with titles and labels
        fig.update_layout(
            title="Changes in Minimum q Value in 1ms Intervals Over Crashes and Non-Crashes",
            xaxis=dict(title="Time [s]",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(title="Change in Minimum q",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            legend=dict(title="Legend"),
            template='plotly_white'
        )

        # Show the plot
        fig.write_html("plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/q/dq_crashes_vs_non_crashes.html")
        fig.show()

    return