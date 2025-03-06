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


def q_change_over_phase_colored_by_ssli_sustain_only(data_dir, num_phase_bins, min_num_crashes, max_num_crashes, q_psibar='min', show_plotly=False):
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
    crash_dict = load.load_json_file(f"{data_dir}crash_info_with_hardware_error.json")
    ssli_dict = load.load_json_file("machine_settings_and_state/shots_since_li/shots_since_li.json")
    
    # plotting arrays
        # q and phase arrays
    q_array_sustain = []
    q_phase_array_sustain = []
        # q and phase slope arrays
    q_slope_array_sustain = []
    q_phase_slope_array_sustain = []
        # shot number arrays
    shot_numbers_slope_array_sustain = []
        # ssli array
    ssli_array = []
    ssli_array_slopes = []
    
    unique_shots = []
    
    # make arrays of thomson temperature data
    cur = 1
    tot = len(q_dict)
    for s in q_dict.keys():
        if s in crash_dict.keys() and s in sustainment_dict:
            if  type(str()) not in [type(sustainment_dict[s]), type(q_dict[s]), type(crash_dict[s]), type(ssli_dict[s])]:
                temp_data = load_data.load_json_file(data_dir + "crash_phase/phase_" + str(s) + ".json")
                if sustainment_dict[s] > 0 and len(crash_dict[s]['times']) > min_num_crashes and len(crash_dict[s]['times']) < max_num_crashes:
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
                            ssli_array.append(ssli_dict[s])
                            valid_q_points_shot += 1
                        
                    # make array of all slopes
                    for i in range(valid_q_points_shot - 1):
                        q_slope_array_sustain.append((q_array_sustain[-(i+1)] - q_array_sustain[-i]) / (q_phase_array_sustain[-(i+1)] - q_phase_array_sustain[-i]))
                        q_phase_slope_array_sustain.append((q_phase_array_sustain[-(i+1)] + q_phase_array_sustain[-i]) / 2)
                        shot_numbers_slope_array_sustain.append(s)
                        ssli_array_slopes.append(np.log10((ssli_array[-(i+1)] + ssli_array[-i]) / 2))
                        
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
    ssli_array_slopes = [ssli_array_slopes[i] for i in q_slope_indices_sorted_by_phase_sustain]

    
        # get boundaries of bins
            # sustain
    bin_edges_phase_sustain = np.linspace(q_phase_slope_array_sustain[0], q_phase_slope_array_sustain[-1], num_phase_bins + 1)

    
    q_slope_means_sustain = []
    q_slope_phase_means_sustain = []
    
    for i in range(len(bin_edges_phase_sustain) - 1):
        # sustain
        q_mean_sustain = median_of_bin(q_slope_array_sustain, q_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        q_slope_means_sustain.append(q_mean_sustain) if q_mean_sustain is not None else None
        q_p_mean_sustain = median_of_bin(q_phase_slope_array_sustain, q_phase_slope_array_sustain, bin_edges_phase_sustain[i], bin_edges_phase_sustain[i+1])
        q_slope_phase_means_sustain.append(q_p_mean_sustain) if q_p_mean_sustain is not None else None

    
    
    # Scatter of the q slope over phase data
    fig1 = go.Figure()

    # Add scatter points with colormap
    fig1.add_trace(go.Scatter(
        x=q_phase_slope_array_sustain,
        y=q_slope_array_sustain,
        mode='markers',
        name="dq/dp of Sustain Shots",
        marker=dict(
            color=ssli_array_slopes,  # Use values from color_array
            colorscale='jet',  # Change this to your desired colormap ('viridis', 'jet', etc.)
            opacity=0.7,
            showscale=True,  # Show colorbar
            colorbar=dict(title="log(shots since li)")  # Label the colorbar
        ),
        text=shot_numbers_slope_array_sustain
    ))
    

    # Add median lines
    fig1.add_trace(go.Scatter(
        x=q_slope_phase_means_sustain,
        y=q_slope_means_sustain,
        mode='lines',
        name='Median of Sustain Shots',
        line=dict(color='black')
    ))

    # Layout settings
    fig1.update_layout(
        title=f"dq/dp Over Phase at q{q_psibar}<br>{min_num_crashes}-{max_num_crashes} Crashes\n{len(q_phase_slope_array_sustain)} Points, {len(unique_shots)} Shots\nColored by ssli",
        xaxis=dict(
            title="Phase",
            showgrid=True,
            gridcolor="lightgray",
            gridwidth=1
        ),
        yaxis=dict(
            title="dq/dp",
            showgrid=True,
            gridcolor="lightgray",
            gridwidth=1
        ),
        legend=dict(title="Legend"),
    )

    if show_plotly:
        fig1.show()
    fig1.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/q/dq_dp_colored_by_ssli_{min_num_crashes}-{max_num_crashes}_crashes.html")
    
    
    return