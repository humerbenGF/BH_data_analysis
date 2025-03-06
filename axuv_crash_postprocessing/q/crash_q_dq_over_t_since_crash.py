# import libraries
#################################################################
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap


# import personal files
#################################################################
import load_save_data.load_data as load_data
import printouts.progress_bar as pb
import cursors.scatter_cursors as cursors


def plot_dq_over_t_since_crash(crash_dir, q_psibar, crash_num, num_points_per_crash, num_bins=50, write_cursors=False):
        # check crash directory string
    if crash_dir[-1] != "/":
        crash_dir += "/"
    
    # load in q data
    if q_psibar == 'min':
        q_dict = load_data.load_json_file("plasma_data_and_parameters/q_profile/q_min_data.json")
    if q_psibar == '95':
        q_dict = load_data.load_json_file("plasma_data_and_parameters/q_profile/q95_data.json")
    if q_psibar == '00':
        q_dict = load_data.load_json_file("plasma_data_and_parameters/q_profile/q00_data.json")
    
    # load in crash and lifetime data
    crash_info = load_data.load_json_file(f"{crash_dir}crash_info_with_hardware_error.json")
    lifetime_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    sustain_dict = load_data.load_json_file("machine_settings_and_state/sustainment/sustainment.json")
    
    i = 1
    tot = len(crash_info.keys())
        # sustain
    dq_array_sustain = []
    time_since_crash_array_sustain = []
    hover_text_array_sustain = []
    crash_time_array_sustain = []
        # non_sustain
    dq_array_non_sustain = []
    time_since_crash_array_non_sustain = []
    hover_text_array_non_sustain = []
    crash_time_array_non_sustain = []
    
    unique_shots = []
    
    for s in crash_info.keys():
        if s in lifetime_dict.keys() and s in q_dict.keys() and s in sustain_dict.keys():
            if type(str()) not in [type(lifetime_dict[s]), type(q_dict[s]), type(crash_info[s]), type(sustain_dict[s])] and len(crash_info[s]['times']) >= crash_num:
                crash_time = crash_info[s]['times'][crash_num-1]
                q_index = int(crash_time*1000)
                if sustain_dict[s] > 0:
                    for i in range(num_points_per_crash):
                        dq_array_sustain.append(q_dict[s]['data'][q_index+i] - q_dict[s]['data'][q_index-1+i])
                        time_since_crash_array_sustain.append(((q_index+(1+i))/1000 - crash_time)*1000)
                        hover_text_array_sustain.append(f"Shot: {s} // Lifetime: {lifetime_dict[s]}")
                        crash_time_array_sustain.append(crash_time)    
                else:
                    for i in range(num_points_per_crash):
                        dq_array_non_sustain.append(q_dict[s]['data'][q_index+i] - q_dict[s]['data'][q_index-1+i])
                        time_since_crash_array_non_sustain.append(((q_index+(1+i))/1000 - crash_time)*1000)
                        hover_text_array_non_sustain.append(f"Shot: {s} // Lifetime: {lifetime_dict[s]}")
                        crash_time_array_non_sustain.append(crash_time)
                        
                unique_shots.append(s)

        pb.progress_bar_pct_only(i, tot)
        i += 1
    
    # sustain
    indices_sorted_sustain = np.argsort(time_since_crash_array_sustain)
    time_since_crash_array_sorted_sustain = [time_since_crash_array_sustain[i] for i in indices_sorted_sustain]
    dq_array_sorted_sustain = [dq_array_sustain[i] for i in indices_sorted_sustain]
    bin_edges_sustain = np.linspace(time_since_crash_array_sorted_sustain[0], time_since_crash_array_sorted_sustain[-1], num_bins+1)
    indices = np.digitize(time_since_crash_array_sorted_sustain, bin_edges_sustain) - 1  # Find bin indices for each time
    binned_indices_sustain = {i: np.where(indices == i)[0].tolist() for i in range(len(bin_edges_sustain) - 1)}
    
    # non non_sustain
    indices_sorted_non_sustain = np.argsort(time_since_crash_array_non_sustain)
    time_since_crash_array_sorted_non_sustain = [time_since_crash_array_non_sustain[i] for i in indices_sorted_non_sustain]
    dq_array_sorted_non_sustain = [dq_array_non_sustain[i] for i in indices_sorted_non_sustain]
    bin_edges_non_sustain = np.linspace(time_since_crash_array_sorted_non_sustain[0], time_since_crash_array_sorted_non_sustain[-1], num_bins+1)
    indices = np.digitize(time_since_crash_array_sorted_non_sustain, bin_edges_non_sustain) - 1  # Find bin indices for each time
    binned_indices_non_sustain = {i: np.where(indices == i)[0].tolist() for i in range(len(bin_edges_non_sustain) - 1)}
    
    # sustain
    averages_sustain = []
    average_times_sustain = []
    for k in binned_indices_sustain.keys():
        averages_sustain.append(np.median([dq_array_sorted_sustain[i] for i in binned_indices_sustain[k]]))
        average_times_sustain.append(np.median([time_since_crash_array_sorted_sustain[i] for i in binned_indices_sustain[k]]))
        
    # non sustain
    averages_non_sustain = []
    average_times_non_sustain = []
    for k in binned_indices_non_sustain.keys():
        averages_non_sustain.append(np.median([dq_array_sorted_non_sustain[i] for i in binned_indices_non_sustain[k]]))
        average_times_non_sustain.append(np.median([time_since_crash_array_sorted_non_sustain[i] for i in binned_indices_non_sustain[k]]))
    
    
    # plot things
    scatter_sustain = plt.scatter(time_since_crash_array_sustain, dq_array_sustain, marker='.', color='r', alpha=0.2, label='Sustain Shots')
    scatter_non_sustain = plt.scatter(time_since_crash_array_non_sustain, dq_array_non_sustain, marker='.', color='b', alpha=0.2, label='Non-Sustain Shots')
    plt.plot(average_times_sustain, averages_sustain, 'r', label='Median of Sustain Shots')
    plt.plot(average_times_non_sustain, averages_non_sustain, 'b', label='Median of Non-Sustain Shots')
    # titles and labels
    plt.title(r"$\Delta$q Over Time Since Crash"+f" {crash_num}\n{len(unique_shots)} Shots // {len(time_since_crash_array_non_sustain)+len(time_since_crash_array_sustain)} Points")
    plt.ylabel(r"$\Delta$q")
    plt.xlabel("Time Since Crash [ms]")
    plt.grid(True)
    plt.legend()
    # add cursors to plot
    if write_cursors:
        cursors.add_cursors_to_scatter(scatter_sustain, hover_text_array_sustain)
        cursors.add_cursors_to_scatter(scatter_non_sustain, hover_text_array_non_sustain)
    # show plot
    plt.show()
    
    return