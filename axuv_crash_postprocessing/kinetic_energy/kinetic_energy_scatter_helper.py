# import libraries
#################################################################
import numpy as np
import bisect
from scipy.interpolate import interp1d



# import personal files
#################################################################



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

def find_crashes_before_time(crash_times, toi):
    i = 0
    for crash_time in crash_times:
        if crash_time < toi:
            i += 1
        
    return i

def median_of_bin(y_data, x_data, left_bin_limit, right_bin_limit):
    # Find the indices of the range boundaries
    start_idx = bisect.bisect_left(x_data, left_bin_limit)
    end_idx = bisect.bisect_right(x_data, right_bin_limit)
    
    # Slice the list to get the values within the range
    if start_idx != end_idx:
        mean = np.median(y_data[start_idx:end_idx])
    else:
        mean = None

    return mean

def get_interp_value(time_array, value_array, time_of_interest):
    """
    Interpolates the value from `value_array` at `time_of_interest` based on the times in `time_array`.
    
    Parameters:
        time_array (array-like): Array of time values (does not need to be evenly spaced).
        value_array (array-like): Array of values corresponding to `time_array`.
        time_of_interest (float): The time at which to interpolate the value.
        
    Returns:
        float: Interpolated value at `time_of_interest`, or `nan` if inputs are invalid.
    """
    
    try:
        # Ensure inputs are numpy arrays
        time_array = np.array(time_array)
        value_array = np.array(value_array)
        
        # Create an interpolation function (allow extrapolation)
        interp_func = interp1d(time_array, value_array, bounds_error=False, fill_value="extrapolate")
        
        # Return the interpolated value
        return interp_func(time_of_interest)
    except Exception as e:
        print(f"Error during interpolation: {e}")
        return np.nan