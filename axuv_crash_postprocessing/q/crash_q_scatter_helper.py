import numpy as np
import bisect
import load_save_data.load_data as load_data


def binned_means(t, y, dt):
    # Determine the number of bins based on the range of t and the specified bin width dt
    num_bins = int((max(t) - min(t)) / dt) + 1
    bin_edges = np.linspace(min(t), max(t), num_bins + 1)  # Bin edges from 0 to max(t) with bin width dt

    # Initialize lists to store the bin centers and means
    bin_centers = []
    bin_means = []

    # Calculate the mean of y values for each bin
    for i in range(num_bins):
        bin_start = bin_edges[i]
        bin_end = bin_edges[i + 1]
        
        # Select y values within the current bin range
        indices = (t >= bin_start) & (t < bin_end)
        indices = np.where(indices)[0]
        bin_values = []
        for index in indices:
            bin_values.append(y[index])
        
        bin_values = np.array(bin_values)

        # Compute mean if there are values in the bin, otherwise append NaN
        if bin_values.size > 0:
            bin_centers.append((bin_start + bin_end) / 2)
            bin_means.append(np.mean(bin_values))
        else:
            bin_centers.append((bin_start + bin_end) / 2)
            bin_means.append(np.nan)

    return np.array(bin_centers), np.array(bin_means)


def interp_q_time(q_array, toi):
    toi_ms = toi * 1000
    qoi = (q_array[int(toi_ms)] - q_array[int(toi_ms) - 1]) * (toi_ms - (int(toi_ms) - 1)) + q_array[int(toi_ms) - 1]
    
    return qoi


def median_of_bin(y_data, x_data, left_bin_limit, right_bin_limit):
    # Find the indices of the range boundaries
    start_idx = bisect.bisect_left(x_data, left_bin_limit)
    end_idx = bisect.bisect_right(x_data, right_bin_limit)
    
    # Slice the list to get the values within the range
    if start_idx <= end_idx:
        mean = np.nanmedian(y_data[start_idx:end_idx])
    else:
        mean = None

    return mean


def convert_times_to_phases(phase_data, toi):
    ind = find_closest_index(phase_data['time'], toi)
    return phase_data['phase'][ind]


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