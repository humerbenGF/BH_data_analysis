# import libraries
#################################################################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.lines import Line2D



# import personal files
#################################################################
import load_save_data.load_data as load_data
from axuv_crash_postprocessing.thomson.crash_thomson_load_data import load_thomson_phase_data_by_shot
import cursors.scatter_cursors as cursors
from axuv_crash_postprocessing.thomson.crash_thomson_scatter_helpers import median_of_bin
import plots_github.GF_html_plot_viewer.plot_generation_tools.plotly_scatter as plotly_scatter



def plot_multishot_core_edge_slopes_sustain_non_sustain(crash_data_dir, slope_type, matplotlib=True, plotly=False, show_plotly=False):
    # load data
    data_dict_by_shot = load_thomson_phase_data_by_shot(crash_data_dir, True, True, True, True)
    thomson_slope_data_by_shot = load_data.load_json_file("plasma_data_and_parameters/thomson/thomson_psibar_slopes.json")
    sustainment_dict = load_data.load_json_file("machine_settings_and_state/sustainment/sustainment.json")

    
    # choose which slope is going to be in the scatter plot
    if slope_type == '600_730':
        slope_key = 'slope_600_730_arr'
    elif slope_type == '600_900':
        slope_key = 'slope_600_900_arr'
    elif slope_type == '730_900':
        slope_key = 'slope_730_900_arr'
    elif slope_type == 'best_fit':
        slope_key = 'slope_best_fit'
    else:
        print("INVALID DECLARATION OF 'slope_type' VARIABLE")
        print("\tOptions are: '600_730', '600_900', '730_900', 'best_fit'")
        return
    
    # intialize sustain arrays
    phase_data_sustain = []
    slope_data_sustain = []
    hover_text_array_sustain = []
    # initialize sustain arrays
    phase_data_non_sustain = []
    slope_data_non_sustain = []
    hover_text_array_non_sustain = []
    
    for k in thomson_slope_data_by_shot.keys():
        if k in sustainment_dict.keys():
            for i in range(len(thomson_slope_data_by_shot[k]['phases'])):
                # determine how many crashes have elapsed
                cur_time = thomson_slope_data_by_shot[k]['times'][i]
                num_elapsed_crashes = 0
                for j in range(len(data_dict_by_shot[k]['crash_info']['times'])):
                    if cur_time > data_dict_by_shot[k]['crash_info']['times'][j]:
                        num_elapsed_crashes += 1
                    else:
                        break
                
                # write phase and slope data to arrays
                if sustainment_dict[k] > 0:
                    phase_data_sustain.append(thomson_slope_data_by_shot[k]['phases'][i] + num_elapsed_crashes)
                    if slope_key == 'slope_best_fit':
                        slope_data_sustain.append(thomson_slope_data_by_shot[k][slope_key][i][0])
                    else:
                        slope_data_sustain.append(thomson_slope_data_by_shot[k][slope_key][i])
                    hover_text_array_sustain.append(k)
                else:
                    phase_data_non_sustain.append(thomson_slope_data_by_shot[k]['phases'][i] + num_elapsed_crashes)
                    if slope_key == 'slope_best_fit':
                        slope_data_non_sustain.append(thomson_slope_data_by_shot[k][slope_key][i][0])
                    else:
                        slope_data_non_sustain.append(thomson_slope_data_by_shot[k][slope_key][i])
                    hover_text_array_non_sustain.append(k)
        
    
    # Sort sustain data by phase (since rolling operations work best on ordered data)
    sorted_indices_sustain = np.argsort(phase_data_sustain)
    phase_data_sorted_sustain = np.array(phase_data_sustain)[sorted_indices_sustain]
    slope_data_sorted_sustain = np.array(slope_data_sustain)[sorted_indices_sustain]

    # Compute rolling median with a window of 10 points
    window_size = 80  # Adjust based on your data density
    rolling_median_sustain = pd.Series(slope_data_sorted_sustain).rolling(window=window_size, center=True).median()
    
    # Sort non-sustain data by phase (since rolling operations work best on ordered data)
    sorted_indices_non_sustain = np.argsort(phase_data_non_sustain)
    phase_data_sorted_non_sustain = np.array(phase_data_non_sustain)[sorted_indices_non_sustain]
    slope_data_sorted_non_sustain = np.array(slope_data_non_sustain)[sorted_indices_non_sustain]

    # Compute rolling median with a window of 10 points
    window_size = 80  # Adjust based on your data density
    rolling_median_non_sustain = pd.Series(slope_data_sorted_non_sustain).rolling(window=window_size, center=True).median()
    
        
    if matplotlib:
        scatter_sustain = plt.scatter(phase_data_sustain, slope_data_sustain, marker='.', color='r', alpha=0.2,  label="Sustain Shots")
        scatter_non_sustain = plt.scatter(phase_data_non_sustain, slope_data_non_sustain, marker='.', color='b', alpha=0.2, label="Non-Sustain Shots")
        plt.plot(phase_data_sorted_sustain, rolling_median_sustain, color='r', label=f"Rolling Median With Window={window_size} for Sustain Shots")
        plt.plot(phase_data_sorted_non_sustain, rolling_median_non_sustain, color='b', label=f"Rolling Median With Window={window_size} for Non-Sustain Shots")
        plt.title(f"Thomson Slope {slope_type} Over Phase\n{len(phase_data_sustain)+len(phase_data_non_sustain)} Points")
        plt.ylabel(r"Slope of $\Delta$T/$\Delta$$\Psi$")
        plt.xlabel("Phase")
        plt.legend()
        plt.grid(True)
        
        # add cursors
        cursors.add_cursors_to_scatter(scatter_sustain, hover_text_array_sustain)
        cursors.add_cursors_to_scatter(scatter_non_sustain, hover_text_array_non_sustain)
        
        plt.show()
        
    if plotly:
        plotly_scatter.make_plotly_multi_scatter(
            [phase_data_sustain, phase_data_non_sustain],
            [slope_data_sustain, slope_data_non_sustain],
            ["Sustain Shots", "Non-Sustain Shots"],
            ["red", "blue"],
            [hover_text_array_sustain, hover_text_array_non_sustain],
            [phase_data_sorted_sustain, phase_data_sorted_non_sustain],
            [rolling_median_sustain, rolling_median_non_sustain],
            [f"Rolling Median With Window={window_size} for Sustain Shots",f"Rolling Median With Window={window_size} for Non-Sustain Shots"],
            ["red", "blue"],
            f"Thomson Slope {slope_type} Over Phase\n{len(phase_data_sustain)+len(phase_data_non_sustain)} Points",
            "Phase",
            "dT/dPsi",
            f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/thomson_migration/thomson_psibar_slope_{slope_type}_sustain_non_sustain.html",
            show_plotly
        )
    
    return



def plot_multishot_core_edge_slopes(crash_data_dir, slope_type, matplotlib=True, plotly=False, show_plotly=False):
    # load data
    data_dict_by_shot = load_thomson_phase_data_by_shot(crash_data_dir, True, True, True, True)
    thomson_slope_data_by_shot = load_data.load_json_file("plasma_data_and_parameters/thomson/thomson_psibar_slopes.json")
    
    # choose which slope is going to be in the scatter plot
    if slope_type == '600_730':
        slope_key = 'slope_600_730_arr'
    elif slope_type == '600_900':
        slope_key = 'slope_600_900_arr'
    elif slope_type == '730_900':
        slope_key = 'slope_730_900_arr'
    elif slope_type == 'best_fit':
        slope_key = 'slope_best_fit'
    else:
        print("INVALID DECLARATION OF 'slope_type' VARIABLE")
        print("\tOptions are: '600_730', '600_900', '730_900', 'best_fit'")
        return
    
    phase_data = []
    slope_data = []
    hover_text_array = []
    for k in thomson_slope_data_by_shot.keys():
        for i in range(len(thomson_slope_data_by_shot[k]['phases'])):
            # determine how many crashes have elapsed
            cur_time = thomson_slope_data_by_shot[k]['times'][i]
            num_elapsed_crashes = 0
            for j in range(len(data_dict_by_shot[k]['crash_info']['times'])):
                if cur_time > data_dict_by_shot[k]['crash_info']['times'][j]:
                    num_elapsed_crashes += 1
                else:
                    break
            
            # write phase and slope data to arrays
            phase_data.append(thomson_slope_data_by_shot[k]['phases'][i] + num_elapsed_crashes)
            if slope_key == 'slope_best_fit':
                slope_data.append(thomson_slope_data_by_shot[k][slope_key][i][0])
            else:
                slope_data.append(thomson_slope_data_by_shot[k][slope_key][i])
            hover_text_array.append(k)
        
    
    # Sort data by phase (since rolling operations work best on ordered data)
    sorted_indices = np.argsort(phase_data)
    phase_data_sorted = np.array(phase_data)[sorted_indices]
    slope_data_sorted = np.array(slope_data)[sorted_indices]

    # Compute rolling median with a window of 10 points
    window_size = 80  # Adjust based on your data density
    rolling_median = pd.Series(slope_data_sorted).rolling(window=window_size, center=True).median()
    
        
    if matplotlib:
        scatter = plt.scatter(phase_data, slope_data, marker='.', color='k', label="Scatter of Slope Over Phase")
        plt.plot(phase_data_sorted, rolling_median, color='r', label=f"Rolling Median With Window={window_size}")
        plt.title(f"Thomson Slope {slope_type} Over Phase\n{len(phase_data)} Points")
        plt.ylabel(r"Slope of $\Delta$T/$\Delta$$\Psi$")
        plt.xlabel("Phase")
        plt.legend()
        
        # add cursors
        cursors.add_cursors_to_scatter(scatter, hover_text_array)
        
        plt.show()
    
    return



def plot_multitime_thomson_core_edge_singleshot(crash_data_dir, shot_number):
    # load data
    data_dict_by_shot = load_thomson_phase_data_by_shot(crash_data_dir, True, True, True, True)
    thomson_slope_data_by_shot = load_data.load_json_file("plasma_data_and_parameters/thomson/thomson_psibar_slopes.json")
    
    data_dict_singleshot = data_dict_by_shot[str(shot_number)]
    thomson_slope_data = thomson_slope_data_by_shot[str(shot_number)]
    
    # set up colormap
    num_times_avail = len(thomson_slope_data['slope_600_730_arr'])
    colormap = get_cmap("jet")  # You can replace 'viridis' with any Matplotlib colormap
    # Linearly spaced values between 0 and 1 for the colormap
    if num_times_avail > 1:
        colors = [colormap(i / (num_times_avail - 1)) for i in range(num_times_avail)]
    else:
        colors = [colormap(0)]
        
    legend_elements = [
        Line2D([0], [0], color='gray', linestyle='--', label="Slope Between TS600 and TS730"),
        Line2D([0], [0], color='gray', linestyle='-.', label="Slope Between TS730 and TS900"),
        Line2D([0], [0], color='gray', linestyle=':',  label="Slope Between TS600 and TS900"),
        Line2D([0], [0], color='gray', linestyle='-',  label="Line of Best Fit Between Available Thomson Points"),
    ]
    
    for i in range(len(thomson_slope_data['slope_600_730_arr'])):
        thomson = np.array([data_dict_singleshot['thomson_600_temps'][i], data_dict_singleshot['thomson_730_temps'][i], data_dict_singleshot['thomson_900_temps'][i]])
        psibar = np.array([data_dict_singleshot['thomson_600_psibars'][i], data_dict_singleshot['thomson_730_psibars'][i], data_dict_singleshot['thomson_900_psibars'][i]])
        # add scattered vertices to plot
        plt.scatter(psibar, thomson, marker='x', color=colors[i])
        legend_elements.append(Line2D([0], [0], marker='x', linestyle='None', color=colors[i], label=f"Thomson Data for t={data_dict_singleshot['thomson_600_times'][i]*1000}ms"))
        # plot between 600 and 730
        x,y = [data_dict_singleshot['thomson_600_psibars'][i], data_dict_singleshot['thomson_730_psibars'][i]], [data_dict_singleshot['thomson_600_temps'][i], data_dict_singleshot['thomson_730_temps'][i]]
        plt.plot(x, y, color=colors[i], linestyle='--', alpha=0.4)
        # plot between 730 and 900
        x,y = [data_dict_singleshot['thomson_730_psibars'][i], data_dict_singleshot['thomson_900_psibars'][i]], [data_dict_singleshot['thomson_730_temps'][i], data_dict_singleshot['thomson_900_temps'][i]]
        plt.plot(x, y, color=colors[i], linestyle='-.', alpha=0.4)
        # plot between 600 and 900
        x,y = [data_dict_singleshot['thomson_600_psibars'][i], data_dict_singleshot['thomson_900_psibars'][i]], [data_dict_singleshot['thomson_600_temps'][i], data_dict_singleshot['thomson_900_temps'][i]]
        plt.plot(x, y, color=colors[i], linestyle=':', alpha=0.4)
        # plot best fit
        x = [data_dict_singleshot['thomson_600_psibars'][i], data_dict_singleshot['thomson_900_psibars'][i]]
        y = [thomson_slope_data['slope_best_fit'][i][0]*x[0]+thomson_slope_data['slope_best_fit'][i][1], thomson_slope_data['slope_best_fit'][i][0]*x[1]+thomson_slope_data['slope_best_fit'][i][1]]
        plt.plot(x, y, color=colors[i], linestyle='-', alpha=0.7)
    
    plt.title(f"Multitime Thomson Temperature Over Psi\nShot {shot_number}")
    plt.xlabel(r"$\Psi$")
    plt.ylabel("Temperature [eV]")
    plt.legend(handles=legend_elements)
    plt.show()





def scatter_core_edge_slope_over_phase(crash_data_dir, num_phase_bins):
    # change formatting of crash_data_dir if required
    if crash_data_dir[-1] != "/":
        crash_data_dir += "/"
        
    # load data by shot
    data_dict_by_shot = load_thomson_phase_data_by_shot(crash_data_dir, True, True, True, True)
    
    # arrays for plotting
        # temperatures
    thomson_600_array = []
    thomson_900_array = []
        # psibars
    thomson_600_psibar_array = []
    thomson_900_psibar_array = []
        # slopes
    thomson_psibar_slope_array = []
        # misc
    phase_array = []
    shots_array = []
    cursors_array = []
    num_crashes_array = []
    
    for s in data_dict_by_shot.keys():
        if type(data_dict_by_shot[s]) != type(str()):
            for i in range(min(len(data_dict_by_shot[s]["thomson_600_temps"]), len(data_dict_by_shot[s]["thomson_900_temps"]))):
                # get the values for thomson 600 and 900
                    # temperatures
                thomson_600_array.append(data_dict_by_shot[s]["thomson_600_temps"][i])
                thomson_900_array.append(data_dict_by_shot[s]["thomson_900_temps"][i])
                    # psibars
                thomson_600_psibar_array.append(data_dict_by_shot[s]["thomson_600_psibars"][i])
                thomson_900_psibar_array.append(data_dict_by_shot[s]["thomson_900_psibars"][i])
                    # slopes
                thomson_psibar_slope_array.append((thomson_600_array[-1] - thomson_900_array[-1]) / (thomson_600_psibar_array[-1] - thomson_900_psibar_array[-1]))
                    # misc
                k=0
                for j in range(len(data_dict_by_shot[s]["crash_info"]["times"])):
                    if data_dict_by_shot[s]["crash_info"]["times"][j] < data_dict_by_shot[s]["thomson_600_times"][i]:
                        k += 1
                phase_array.append(data_dict_by_shot[s]["thomson_600_phases"][i] + k)
                shots_array.append(s)
                num_crashes_array.append(len(data_dict_by_shot[s]["crash_info"]["times"]))
                cursors_array.append(f"Shot {s}, TS600={thomson_600_array[-1]} eV, TS900={thomson_900_array[-1]} eV")
    
    
    
    thomson_slope_indices_sorted_by_phase = np.argsort(phase_array)
    thomson_psibar_slope_array_sorted = [thomson_psibar_slope_array[i] for i in thomson_slope_indices_sorted_by_phase]
    phase_array_sorted = [phase_array[i] for i in thomson_slope_indices_sorted_by_phase]
    
    
    # get boundaries of bins
    bin_edges_phase = np.linspace(phase_array_sorted[0], phase_array_sorted[-1], num_phase_bins + 1)
    
    thomson_slope_temp_means = []
    thomson_slope_phase_means = []
    
    for i in range(len(bin_edges_phase) - 1):
        # handle phase
        thomson_slope_means = median_of_bin(thomson_psibar_slope_array_sorted, phase_array_sorted, bin_edges_phase[i], bin_edges_phase[i+1])
        thomson_slope_temp_means.append(thomson_slope_means) if thomson_slope_means is not None else None
        thomson_phase_means = median_of_bin(phase_array_sorted, phase_array_sorted, bin_edges_phase[i], bin_edges_phase[i+1])
        thomson_slope_phase_means.append(thomson_phase_means) if thomson_phase_means is not None else None
    
    scatter = plt.scatter(phase_array, thomson_psibar_slope_array, c=num_crashes_array, cmap='jet',marker='.')
    plt.plot(thomson_slope_phase_means, thomson_slope_temp_means, 'k')
    plt.colorbar(label="Num Crashes")
    plt.ylabel("dT/dPsibar")
    plt.xlabel("Phase")
    plt.title("dT/dPsibar Over Phase")
    plt.grid(True)
    
    cursors.add_cursors_to_scatter(scatter, cursors_array)
    
    plt.show()
    
    return



def scatter_core_edge_temp(crash_data_dir):
    # change formatting of crash_data_dir if required
    if crash_data_dir[-1] != "/":
        crash_data_dir += "/"

    # load data by shot
    data_dict_by_shot = load_thomson_phase_data_by_shot(crash_data_dir, True, True, True, True)
    
    # arrays for plotting
    thomson_600_array = []
    thomson_900_array = []
    phase_array = []
    shots_array = []
    cursors_array = []
    unique_shots = []
    
    for s in data_dict_by_shot.keys():
        if type(data_dict_by_shot[s]) != type(str()):
            for i in range(min(len(data_dict_by_shot[s]["thomson_600_temps"]), len(data_dict_by_shot[s]["thomson_900_temps"]))):
                thomson_600_array.append(data_dict_by_shot[s]["thomson_600_temps"][i])
                thomson_900_array.append(data_dict_by_shot[s]["thomson_900_temps"][i])
                phase_array.append(data_dict_by_shot[s]["thomson_600_phases"][i])
                shots_array.append(s)
                cursors_array.append(f"Shot {s}, TS600={thomson_600_array[-1]} eV, TS900={thomson_900_array[-1]} eV")
            unique_shots.append(s)
    
    # fig = plt.figure(figsize=(16,9))
    scatter = plt.scatter(thomson_600_array, thomson_900_array, c=phase_array, cmap='twilight')
    plt.plot([0,max(max(thomson_600_array),max(thomson_900_array))], [0,max(max(thomson_600_array),max(thomson_900_array))], 'k')
    plt.colorbar(label="Phase")
    plt.xlabel("TS600 Temperature [eV]")
    plt.ylabel("TS900 Temperature [eV]")
    plt.title(f"TS600 and TS900 Temperature\n {len(thomson_600_array)} Points, {len(unique_shots)} Shots")
    
    cursors.add_cursors_to_scatter(scatter, cursors_array)
    
    plt.show()
    
    return