# import libraries
#################################################################
import numpy as np


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