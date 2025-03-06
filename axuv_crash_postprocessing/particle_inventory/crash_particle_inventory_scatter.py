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
from axuv_crash_postprocessing.particle_inventory.crash_particle_inventory_scatter_helper import *


def reconstruct_particle_inventory_over_phase_single_num_crashes(data_dir, num_phase_bins, num_time_bins, num_crashes=0, matplotlib=True, plotly=False, show_plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
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
    
    part_invent_slope_array_time = []
    part_invent_time_slope_array = []

    part_invent_recon_array = []
    part_invent_phase_recon_array = []
    part_invent_time_recon_array = []
    
    unique_shots = []
    
    # make arrays of thomson Particle Inventory data
    fig, ax = plt.subplots(figsize=(16,9))
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
                        part_invent_slope_array_time.append((part_invent_array[-(i+1)] - part_invent_array[-i]) / (part_invent_time_array[-(i+1)] - part_invent_time_array[-i]))
                        part_invent_time_slope_array.append((part_invent_time_array[-(i+1)] + part_invent_time_array[-i]) / 2)
        
                    unique_shots.append(s)
        
        prog_bar.progress_bar_pct_only(cur, tot)
        cur += 1
                    
    # reconstruct thomson temp from slope data
        # get indices of sorted arrays
    thomson_slope_indices_sorted_by_phase = np.argsort(part_invent_phase_slope_array)
    part_invent_slope_array = [part_invent_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    part_invent_phase_slope_array = [part_invent_phase_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    
    thomson_slope_indices_sorted_by_time = np.argsort(part_invent_time_slope_array)
    part_invent_slope_array_time = [part_invent_slope_array_time[i] for i in thomson_slope_indices_sorted_by_time]
    part_invent_time_slope_array = [part_invent_time_slope_array[i] for i in thomson_slope_indices_sorted_by_time]
    
        # get boundaries of bins
    bin_edges_phase = np.linspace(part_invent_phase_slope_array[0], part_invent_phase_slope_array[-1], num_phase_bins + 1)
    bin_edges_times = np.linspace(0.9*part_invent_time_slope_array[0], part_invent_time_slope_array[-1]*1.1, num_time_bins + 1)
    
    thomson_slope_temp_means = []
    thomson_slope_phase_means = []
    
    thomson_slope_temp_means_ts = []
    thomson_slope_time_means = []
    
    for i in range(len(bin_edges_phase) - 1):
        # handle phase
        t_s_t_mean = median_of_bin(part_invent_slope_array, part_invent_phase_slope_array, bin_edges_phase[i], bin_edges_phase[i+1])
        thomson_slope_temp_means.append(t_s_t_mean) if t_s_t_mean is not None else None
        t_s_p_mean = median_of_bin(part_invent_phase_slope_array, part_invent_phase_slope_array, bin_edges_phase[i], bin_edges_phase[i+1])
        thomson_slope_phase_means.append(t_s_p_mean) if t_s_p_mean is not None else None
        
    # integrate
    part_invent_recon_array = cumtrapz(thomson_slope_temp_means, thomson_slope_phase_means, initial=0)
    part_invent_phase_recon_array = thomson_slope_phase_means

    # zero out array
    for i in range(len(part_invent_recon_array)):
        part_invent_recon_array[i] = part_invent_recon_array[i] - min(part_invent_recon_array)

    # offset array by c
    c = np.mean(part_invent_array) - np.mean(part_invent_recon_array)
    for i in range(len(part_invent_recon_array)):
        part_invent_recon_array[i] = part_invent_recon_array[i] + c


    if matplotlib:
        # Plots of Particle Inventory over Phase
        #######################################################################################################

        # scatter of the thomson slope over phase data
        plt.scatter(part_invent_phase_slope_array, part_invent_slope_array, color='k', marker='.')
        plt.plot(thomson_slope_phase_means, thomson_slope_temp_means, color='r')
        plt.title(r"$\frac{dN}{dp}$ Over Phase" + f"\n{num_crashes} Crashes")
        plt.xlabel("Phase")
        plt.ylabel(r"$\frac{dN}{dp}$")
        plt.grid(True)
        plt.show()
        
        # scatter of the reconstructed thomson slope over phase data
        # plt.scatter(part_invent_phase_array, thomson_temp_array, color='k', marker='.')
        plt.plot(part_invent_phase_recon_array, part_invent_recon_array, color='r')
        plt.title(f"Particle Inventory Over Phase\n{num_crashes} Crashes")
        plt.xlabel("Phase")
        plt.ylabel("Particle Inventory")
        plt.grid(True)
        plt.show()
        
    
    if plotly:
        # Plots of Particle Inventory over Phase
        #######################################################################################################

        # Scatter of the Thomson slope over phase data
        scatter_phase_slope = go.Scatter(x=part_invent_phase_slope_array, 
                                        y=part_invent_slope_array, 
                                        mode='markers', 
                                        marker=dict(color='black'),
                                        name='Slope Data')

        # Line of the mean values for the Thomson slope
        line_slope_phase = go.Scatter(x=thomson_slope_phase_means, 
                                    y=thomson_slope_temp_means, 
                                    mode='lines', 
                                    line=dict(color='red'),
                                    name='Mean Slope')

        # Create layout for the phase plot
        layout_phase = go.Layout(title=r"dN/dp Over Phase" + f"{num_crashes} Crashes\n{len(part_invent_phase_slope_array)} Points, {len(unique_shots)} Shots",
                                xaxis=dict(title='Phase',
                                    showgrid=True,  # Enable grid lines for the x-axis
                                    gridcolor="lightgray",  # Color of the grid lines
                                    gridwidth=1  # Thickness of the grid lines
                                ),
                                yaxis=dict(title="dt/dp",
                                    showgrid=True,  # Enable grid lines for the x-axis
                                    gridcolor="lightgray",  # Color of the grid lines
                                    gridwidth=1  # Thickness of the grid lines
                                ),
                                showlegend=True,
                                template='plotly_white')

        # Create the figure and plot the phase data
        fig_phase = go.Figure(data=[scatter_phase_slope, line_slope_phase], layout=layout_phase)
        fig_phase.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/recon_particle_inventory/dNdp_over_phase__{num_crashes}crash.html")
        if show_plotly:
            fig_phase.show()

        # Scatter of the reconstructed Thomson slope over phase data
        recon_line_phase = go.Scatter(x=part_invent_phase_recon_array, 
                                    y=part_invent_recon_array, 
                                    mode='lines', 
                                    line=dict(color='red'),
                                    name='Reconstructed')

        # Create layout for the phase recon plot
        layout_recon_phase = go.Layout(title=f"Particle Inventory Over Phase {num_crashes} Crashes\n{len(part_invent_phase_array)} Points, {len(unique_shots)} Shots",
                                    xaxis=dict(title='Phase',
                                        showgrid=True,  # Enable grid lines for the x-axis
                                        gridcolor="lightgray",  # Color of the grid lines
                                        gridwidth=1  # Thickness of the grid lines
                                    ),
                                    yaxis=dict(title='Particle Inventory',
                                        showgrid=True,  # Enable grid lines for the x-axis
                                        gridcolor="lightgray",  # Color of the grid lines
                                        gridwidth=1  # Thickness of the grid lines
                                    ),
                                    showlegend=True,
                                    template='plotly_white')

        # Create the figure and plot the phase recon data
        fig_recon_phase = go.Figure(data=[recon_line_phase], layout=layout_recon_phase)
        fig_recon_phase.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/recon_particle_inventory/particle_inventory_over_phase_{num_crashes}crash.html")
        if show_plotly:
            fig_recon_phase.show()

    
    return



def particle_inventory_over_normalized_time_scatter_single_num_crashes(data_dir, time_bin_width, num_crashes, max_num_particles, matplotlib=True, plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data dicts
    crash_dict = load_data.load_json_file("2024-10-10_19718-23016/crash_info.json")
    particle_inventory_dict = load_data.load_json_file("plasma_data_and_parameters/particle_inventory/particle_inventory.json")
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    # initialize plottable arrays
    particle_inventory_array = []
    norm_time_array = []
    num_crashes_array = []
    phase_array = []    
    shots_list = []
    unique_shots = []
    
    # make arrays of thomson temperature data
    fig, ax = plt.subplots(figsize=(16,9))
    cur=1
    tot=len(particle_inventory_dict)
    for s in particle_inventory_dict.keys():
        if s in lifetimes_dict.keys() and s in crash_dict.keys() and type(particle_inventory_dict[s]) != type(str()) and os.path.isfile(f"2024-10-10_19718-23016/crash_phase/phase_{s}.json"):
            if type(lifetimes_dict[s]) != type(str()) and type(crash_dict[s]) != type(str()):
                if len(crash_dict[s]['times']) == num_crashes and max_num_particles > max(particle_inventory_dict[s]['data']) and 0 < min(particle_inventory_dict[s]['data']):
                    phase_dict = load_data.load_json_file(f"2024-10-10_19718-23016/crash_phase/phase_{s}.json")

                    for i in range(len(particle_inventory_dict[s]["data"])):
                        particle_inventory_array.append(particle_inventory_dict[s]["data"][i])
                        norm_time_array.append((i+1)/1000 / lifetimes_dict[s])
                        phase_array.append(find_crashes_before_time(crash_dict[s]['times'], (i+1)/1000) + phase_dict['phase'][find_closest_index(phase_dict['time'], (i+1)/1000)])
                        num_crashes_array.append(len(crash_dict[s]['times']))
                        shots_list.append(s)
                
                    unique_shots.append(s)
                
        prog_bar.progress_bar_pct_only(cur, tot)
        cur += 1

    # get the line for mean
        # sort arrays based on normalized time
    norm_time_array = np.array(norm_time_array)
    particle_inventory_array = np.array(particle_inventory_array)
    time_sorted_indices = np.argsort(norm_time_array)
    time_sorted_array = norm_time_array[time_sorted_indices]
    time_sorted_particle_inventory_array = particle_inventory_array[time_sorted_indices]
        # get information about number of bins
    num_bins = int(1 / time_bin_width)
    bin_edges = np.linspace(0, 1, num_bins)
    
    means = []
    means_times = []
    for i in range(num_bins - 1):
        means.append(np.median(time_sorted_particle_inventory_array[find_closest_index(time_sorted_array,bin_edges[i]):find_closest_index(time_sorted_array,bin_edges[i+1])]))
        means_times.append(np.median(time_sorted_array[find_closest_index(time_sorted_array,bin_edges[i]):find_closest_index(time_sorted_array,bin_edges[i+1])]))


    if matplotlib:
        # Define a colormap and create a mapping for discrete values
        cmap = plt.cm.gist_rainbow

        # plot the data
        norm = Normalize(vmin=min(phase_array), vmax=max(phase_array))
        scatter = plt.scatter(norm_time_array, particle_inventory_array, c=phase_array, marker='.', cmap=cmap, norm=norm)
        plt.plot(means_times, means, 'k', linewidth=3)
        plt.title(f"Particle Inventory Over Phase (Shots with {num_crashes} Crashes)")
        plt.xlabel("Normalized Time")
        plt.ylabel("Particle Inventory")
        cbar = plt.colorbar(scatter)
        cbar.set_label("Phase")
        plt.grid(True)
                
        cursor.add_cursors_to_scatter(scatter, shots_list)
        click.add_click_action_axuv_part_inv_ts(scatter, fig, shots_list)

        plt.show()
        
    if plotly:
        # Create the color scale (similar to cmap)
        color_scale = 'Rainbow'  # You can change this to other plotly-supported scales

        # Create the scatter plot
        scatter = go.Scatter(
            x=norm_time_array,
            y=particle_inventory_array,
            mode='markers',
            marker=dict(
                color=phase_array,
                colorscale=color_scale,
                colorbar=dict(title='Phase'),
                size=10,
                showscale=True
            ),
            name="Particle Inventory",
            text=shots_list,  # Add shot number to the hover text
            hoverinfo='text+x+y'  # Display shot number, x, y, and phase value
        )

        # Create the line plot for the means
        line = go.Scatter(
            x=means_times,
            y=means,
            mode='lines',
            line=dict(color='black', width=3),
            name="Means"
        )

        # Create layout for the plot
        layout = go.Layout(
            title=f"Particle Inventory Over Phase (Shots with {num_crashes} Crashes)\n{len(phase_array)} Points, {len(unique_shots)} Shots",
            xaxis=dict(title="Normalized Time",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(title="Particle Inventory",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            showlegend=False,
            template='plotly_white'
        )

        # Combine the scatter and line plots in a figure
        fig = go.Figure(data=[scatter, line], layout=layout)

        # Show the plot
        fig.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/particle_inventory/particle_inventory_over_normalized_time_scatter_{num_crashes}crashes.html")
        fig.show()
        

    return



def particle_inventory_over_phase_scatter_single_num_crashes(data_dir, phase_bin_width, num_crashes, max_num_particles, matplotlib=True, plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data dicts
    crash_dict = load_data.load_json_file("2024-10-10_19718-23016/crash_info.json")
    particle_inventory_dict = load_data.load_json_file("plasma_data_and_parameters/particle_inventory/particle_inventory.json")
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    # initialize plottable arrays
    particle_inventory_array = []
    phase_array = []
    num_crashes_array = []
    colors_array = []
    shots_list = []
    lifetimes_array = []
    unique_shots = []
    
    # make arrays of thomson temperature data
    fig, ax = plt.subplots(figsize=(16,9))
    cur=1
    tot=len(particle_inventory_dict)
    for s in particle_inventory_dict.keys():
        if s in lifetimes_dict.keys() and s in crash_dict.keys() and type(particle_inventory_dict[s]) != type(str()) and os.path.isfile(f"2024-10-10_19718-23016/crash_phase/phase_{s}.json"):
            if type(lifetimes_dict[s]) != type(str()) and type(crash_dict[s]) != type(str()):
                if len(crash_dict[s]['times']) == num_crashes and max_num_particles > max(particle_inventory_dict[s]['data']) and 0 < min(particle_inventory_dict[s]['data']):
                    phase_dict = load_data.load_json_file(f"2024-10-10_19718-23016/crash_phase/phase_{s}.json")

                    for i in range(len(particle_inventory_dict[s]["data"])):
                        particle_inventory_array.append(particle_inventory_dict[s]["data"][i])
                        phase_array.append(find_crashes_before_time(crash_dict[s]['times'], (i+1)/1000) + phase_dict['phase'][find_closest_index(phase_dict['time'], (i+1)/1000)])
                        num_crashes_array.append(len(crash_dict[s]['times']))
                        shots_list.append(s)
                        lifetimes_array.append(lifetimes_dict[s])

                    unique_shots.append(s)
        prog_bar.progress_bar_pct_only(cur, tot)
        cur += 1

    # turn number of crashes array into a colored array
    max_num_crashes = max(num_crashes_array)
    max_lifetime = max(lifetimes_array)
    for i in range(len(lifetimes_array)):
        colors_array.append(lifetimes_array[i]/max_lifetime)

    # get the line for mean
        # sort arrays based on phase
    phase_array = np.array(phase_array)
    particle_inventory_array = np.array(particle_inventory_array)
    phase_sorted_indices = np.argsort(phase_array)
    phase_sorted_array = phase_array[phase_sorted_indices]
    phase_sorted_particle_inventory_array = particle_inventory_array[phase_sorted_indices]
        # get information about number of bins
    num_bins = int(phase_sorted_array[-1] / phase_bin_width)
    bin_edges = np.linspace(0, phase_sorted_array[-1], num_bins)
    
    means = []
    means_times = []
    for i in range(num_bins - 1):
        means.append(np.median(phase_sorted_particle_inventory_array[find_closest_index(phase_sorted_array,bin_edges[i]):find_closest_index(phase_sorted_array,bin_edges[i+1])]))
        means_times.append(np.median(phase_sorted_array[find_closest_index(phase_sorted_array,bin_edges[i]):find_closest_index(phase_sorted_array,bin_edges[i+1])]))


    if matplotlib:
        # Define a colormap and create a mapping for discrete values
        cmap = plt.cm.gist_rainbow

        # plot the data
        scatter = plt.scatter(phase_array, particle_inventory_array, c=colors_array, marker='.', cmap=cmap)
        plt.plot(means_times, means, 'k', linewidth=3)
        plt.title("Particle Inventory Over Phase")
        plt.xlabel("Phase")
        plt.ylabel("Particle Inventory")
        plt.grid(True)
        
        cursor.add_cursors_to_scatter(scatter, shots_list)
        click.add_click_action_axuv_part_inv_ts(scatter, fig, shots_list)
        
        plt.show()
        
    if plotly:
        # Create the color scale (similar to cmap)
        color_scale = 'Rainbow'  # You can change this to other plotly-supported scales

        # Create the scatter plot
        scatter = go.Scatter(
            x=phase_array,
            y=particle_inventory_array,
            mode='markers',
            marker=dict(
                color=lifetimes_array,
                colorscale=color_scale,
                colorbar=dict(title='Lifetime [s]'),
                size=10,
                showscale=True
            ),
            name="Particle Inventory",
            text=shots_list,  # Add shot number to the hover text
            hoverinfo='text+x+y'  # Display shot number, x, y, and crash count
        )

        # Create the line plot for the means
        line = go.Scatter(
            x=means_times,
            y=means,
            mode='lines',
            line=dict(color='black', width=3),
            name="Means"
        )

        # Create layout for the plot
        layout = go.Layout(
            title=f"Particle Inventory Over Phase: {num_crashes} Crashes\n{len(phase_array)} Points, {len(unique_shots)} Shots",
            xaxis=dict(title="Phase",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(title="Particle Inventory",
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            showlegend=False,
            template='plotly_white'
        )

        # Combine the scatter and line plots in a figure
        fig = go.Figure(data=[scatter, line], layout=layout)

        # Show the plot
        fig.write_html(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/particle_inventory/particle_inventory_over_phase_scatter_{num_crashes}crashes.html")
        fig.show()

    return
    

def particle_inventory_over_phase_scatter(data_dir, phase_bin_width, matplotlib=True, plotly=False):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in data dicts
    crash_dict = load_data.load_json_file("2024-10-10_19718-23016/crash_info.json")
    particle_inventory_dict = load_data.load_json_file("plasma_data_and_parameters/particle_inventory/particle_inventory.json")
    lifetimes_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    # initialize plottable arrays
    particle_inventory_array = []
    phase_array = []
    num_crashes_array = []
    colors_array = []
    shots_list = []
    unique_shots = []
    
    # make arrays of thomson temperature data
    fig, ax = plt.subplots(figsize=(16,9))
    cur=1
    tot=len(particle_inventory_dict)
    for s in particle_inventory_dict.keys():
        if s in lifetimes_dict.keys() and s in crash_dict.keys() and type(particle_inventory_dict[s]) != type(str()) and os.path.isfile(f"2024-10-10_19718-23016/crash_phase/phase_{s}.json"):
            if type(lifetimes_dict[s]) != type(str()) and type(crash_dict[s]) != type(str()):
                phase_dict = load_data.load_json_file(f"2024-10-10_19718-23016/crash_phase/phase_{s}.json")

                for i in range(len(particle_inventory_dict[s]["data"])):
                    particle_inventory_array.append(particle_inventory_dict[s]["data"][i])
                    phase_array.append(find_crashes_before_time(crash_dict[s]['times'], (i+1)/1000) + phase_dict['phase'][find_closest_index(phase_dict['time'], (i+1)/1000)])
                    num_crashes_array.append(len(crash_dict[s]['times']))
                    shots_list.append(s)
                    
                unique_shots.append(s)
                
        prog_bar.progress_bar_pct_only(cur, tot)
        cur += 1

    # turn number of crashes array into a colored array
    max_num_crashes = max(num_crashes_array)
    for i in range(len(num_crashes_array)):
        colors_array.append(num_crashes_array[i]/max_num_crashes)

    # get the line for mean
        # sort arrays based on phase
    phase_array = np.array(phase_array)
    particle_inventory_array = np.array(particle_inventory_array)
    phase_sorted_indices = np.argsort(phase_array)
    phase_sorted_array = phase_array[phase_sorted_indices]
    phase_sorted_particle_inventory_array = particle_inventory_array[phase_sorted_indices]
        # get information about number of bins
    num_bins = int(phase_sorted_array[-1] / phase_bin_width)
    bin_edges = np.linspace(0, phase_sorted_array[-1], num_bins)
    
    means = []
    means_times = []
    for i in range(num_bins - 1):
        means.append(np.median(phase_sorted_particle_inventory_array[find_closest_index(phase_sorted_array,bin_edges[i]):find_closest_index(phase_sorted_array,bin_edges[i+1])]))
        means_times.append(np.median(phase_sorted_array[find_closest_index(phase_sorted_array,bin_edges[i]):find_closest_index(phase_sorted_array,bin_edges[i+1])]))

    if matplotlib:
        # Define a colormap and create a mapping for discrete values
        cmap = plt.cm.gist_rainbow
        norm = mcolors.BoundaryNorm(boundaries=np.arange(-0.5, max_num_crashes+1, 1), ncolors=max_num_crashes+1)

        # plot the data
        plt.scatter(phase_array, particle_inventory_array, c=colors_array, marker='.', cmap=cmap)
        plt.plot(means_times, means, 'k', linewidth=3)
        plt.title("Particle Inventory Over Phase")
        plt.xlabel("Phase")
        plt.ylabel("Particle Inventory")
        plt.grid(True)
        
        # Create a legend
        unique_c = np.unique(colors_array)
        unique_numcrashes = np.unique(num_crashes_array)
        handles = [plt.Line2D([0], [0], marker='o', color=cmap(val), linestyle='', markersize=10) for val in unique_c]
        labels = [f"{val} Crashes" for val in unique_numcrashes]
        plt.legend(handles, labels, title="Number of Crashes")
        plt.show()

    if plotly:
        # Define the color scale
        color_scale = 'Rainbow'
        color_map = np.linspace(0, 1, max_num_crashes+1)  # Mapping for the color scale

        # Create the scatter plot with a color scale
        scatter = go.Scatter(
            x=phase_array,
            y=particle_inventory_array,
            mode='markers',
            marker=dict(
                color=num_crashes_array,
                colorscale=color_scale,
                colorbar=dict(title='Number of Crashes'),
                size=10,
                showscale=True
            ),
            name='Data Points',
            text=shots_list,  # Add shot number to the hover text
            hoverinfo='text+x+y'  # Display shot number, x, y, and crash count
        )

        # Create the line plot for means
        line = go.Scatter(
            x=means_times,
            y=means,
            mode='lines',
            line=dict(color='black', width=3),
            name='Means'
        )

        # Create layout for the plot
        layout = go.Layout(
            title=f'Particle Inventory Over Phase\n{len(particle_inventory_array)} Points, {len(unique_shots)} Shots',
            xaxis=dict(title='Phase',
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            yaxis=dict(title='Particle Inventory',
                showgrid=True,  # Enable grid lines for the x-axis
                gridcolor="lightgray",  # Color of the grid lines
                gridwidth=1  # Thickness of the grid lines
            ),
            showlegend=False,
            template='plotly_white'
        )

        # Combine the scatter and line plots in a figure
        fig = go.Figure(data=[scatter, line], layout=layout)

        # Show the plot
        fig.write_html("plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/particle_inventory/particle_inventory_over_phase_scatter.html")
        fig.show()
    
    
    return