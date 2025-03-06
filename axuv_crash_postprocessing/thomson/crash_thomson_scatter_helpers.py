import numpy as np
import load_save_data.load_data as load_data
import matplotlib.pyplot as plt
import bisect




###########################################################################################################
# helper functions
###########################################################################################################

def get_thomson_psibar_value(thomson_time, thomson_psibar_singlesensor, non_interp_threshold=0.01):
    # convert back to ms for easier implementation in this function
    thomson_time_seconds = thomson_time*1000
    # print(thomson_psibar_singlesensor)
    
    if (thomson_time_seconds - int(thomson_time_seconds)) < non_interp_threshold:
        if int(thomson_time_seconds) > len(thomson_psibar_singlesensor):
            print(f"thomson_time_rawval: {thomson_time} // thomson_psibar_singlesensor: {thomson_psibar_singlesensor}")
        return thomson_psibar_singlesensor[int(thomson_time_seconds) - 1]

    else:
        interp_val = (thomson_psibar_singlesensor[int(thomson_time_seconds)] - thomson_psibar_singlesensor[int(thomson_time_seconds) - 1]) * (thomson_time_seconds - int(thomson_time_seconds)) + thomson_psibar_singlesensor[int(thomson_time_seconds) - 1]
        return interp_val


def convert_to_times_since_crashes(shot, data_dir, ss_times):    
    phase = load_data.load_json_file(data_dir + "crash_phase/phase_" + str(shot) + ".json")
    
    times_since_crashes = []
    
    for time in ss_times:
        time_prev_crash = find_time_at_local_minimum(phase['time'], phase['phase'], time)
        dt_since_crash = time - time_prev_crash
        times_since_crashes.append(dt_since_crash)
    
    return times_since_crashes


def plot_temperature_percentiles(bin_centers, binned_temp_medians):
    for i in range(len(binned_temp_medians)):
        plt.plot(bin_centers, binned_temp_medians[i], 'r')
    
    return

def plot_stdev_of_bins(bin_centers, binned_stdevs):
    plt.plot(bin_centers, binned_stdevs, c='r')
    plt.title("Stdev of Psi Over Phase")
    plt.ylabel("Stdev of Psi")
    plt.xlabel("Phase")
    return


def bin_by_phase(phase_array, value_array, n_bins, percentiles_list):
    bin_edges = np.linspace(0, 1, n_bins+1)
    
    binned_temp_values = []
    for i in range(len(bin_edges) - 1):
        binned_temp_values.append([])
        indices = np.where((phase_array >= bin_edges[i]) & (phase_array < bin_edges[i+1]))[0]
        for j in range(len(indices)):
            binned_temp_values[i].append(value_array[indices[j]])


    binned_temp_medians = []
    binned_temp_stdevs = []
    for p in range(len(percentiles_list)):
        binned_temp_medians.append([])
        for i in range(len(binned_temp_values)):        
            binned_temp_values[i] = sorted(list(binned_temp_values[i]))
            binned_temp_medians[p].append(binned_temp_values[i][int(len(binned_temp_values[i]) * percentiles_list[p])])
            if p == 0:
                binned_temp_stdevs.append(np.std(binned_temp_values[i]))
        
    bin_centers = np.linspace((bin_edges[0] + bin_edges[1])/2, (bin_edges[-1] + bin_edges[-2])/2, (len(bin_edges) - 1))
    
    return bin_centers, binned_temp_medians, binned_temp_stdevs


def find_time_at_zero_phase(time, phase, t0):
    # Find the index of the time value closest to t0
    closest_index = (np.abs(np.array(time) - t0)).argmin()

    # Work backwards from closest_index until we find a phase of 0
    for i in range(closest_index, -1, -1):
        if phase[i] == 0:
            return time[i]

    # If no phase of 0 is found before closest_index, return None or raise an error
    return None  # Or raise ValueError("No zero phase found before t0")


def find_time_at_local_minimum(time, phase, t0):
    # Find the index of the time value closest to t0
    closest_index = (np.abs(np.array(time) - t0)).argmin()

    # Work backwards from closest_index to find the local minimum
    for i in range(closest_index, -1, -1):
        # Check if the phase at i-1 is much larger than at i
        if ((phase[i-1] - phase[i]) > 0) or (phase[i-1] == 0):
            return time[i]
    
    # If no local minimum is found, return None
    return None


def convert_times_to_phases(shot, data_dir, times_list):
    phase = load_data.load_json_file(data_dir + "crash_phase/phase_" + str(shot) + ".json")
    
    phases = []
    for toi in times_list:
        ind = find_closest_index(phase['time'], toi)
        phases.append(phase['phase'][ind])
    
    return phases


def find_closest_index(times, toi):
    """
    Finds the index of the value in the sorted array `times` that is closest to the specified value `toi`.

    Parameters:
    times (list or np.ndarray): An ordered array of time values.
    toi (float): The target time of interest.

    Returns:
    int: The index of the value in `times` that is closest to `toi`.
    """
    times = np.asarray(times)  # Ensure times is a NumPy array for element-wise operations
    idx = (np.abs(times - toi)).argmin()  # Find index of the minimum distance to `toi`
    return idx


def reorder_arrays(a, b, c):
    # Get the indices that would sort array a in ascending order
    sorted_indices = np.argsort(a)
    
    # Reorder a, b, and c using the sorted indices
    a_sorted = np.array(a)[sorted_indices]
    b_sorted = np.array(b)[sorted_indices]
    c_sorted = np.array(c)[sorted_indices]
    
    return a_sorted, b_sorted, c_sorted


def mean_of_bin(y_data, x_data, left_bin_limit, right_bin_limit):
    # Find the indices of the range boundaries
    start_idx = bisect.bisect_left(x_data, left_bin_limit)
    end_idx = bisect.bisect_right(x_data, right_bin_limit)
    
    # Slice the list to get the values within the range
    if start_idx != end_idx:
        mean = np.mean(y_data[start_idx:end_idx])
    else:
        mean = None

    return mean


def median_of_bin(y_data, x_data, left_bin_limit, right_bin_limit):
    # Find the indices of the range boundaries
    start_idx = bisect.bisect_left(x_data, left_bin_limit)
    end_idx = bisect.bisect_right(x_data, right_bin_limit)
    
    # Slice the list to get the values within the range
    if start_idx != end_idx:
        mean = np.nanmedian(y_data[start_idx:end_idx])
    else:
        mean = None

    return mean