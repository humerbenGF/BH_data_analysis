# import packages
#################################################################
import matplotlib.pyplot as plt
import numpy as np


# import personal files
#################################################################
import load_save_data.load_data as load_data
import signal_processing.signal_processing as sig_proc


def plot_axuv_ts(shot_number, sensors_to_exclude=[]):
    axuv_data = load_data.load_bson_file(f"preprocessed_data/raw_axuv_data/{int(shot_number/1000)*1000}/axuv_rawdata_{shot_number}.bson")
    lifetime = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")[str(shot_number)]
    
    lifetime_index = find_closest_index(axuv_data['t'], lifetime)
        
    for i in range(len(axuv_data.keys())):
        axuv_data[list(axuv_data.keys())[i]] = axuv_data[list(axuv_data.keys())[i]][:lifetime_index]
        if list(axuv_data.keys())[i] != 't':
            axuv_data[list(axuv_data.keys())[i]] = sig_proc.low_pass(axuv_data[list(axuv_data.keys())[i]], axuv_data['t'][1] - axuv_data['t'][0], 100*10**3)
            
    # Create the plot
    plt.figure(figsize=(10,6))

    for i in range(len(axuv_data.keys())):
        if list(axuv_data.keys())[i] != 't' and list(axuv_data.keys())[i] not in sensors_to_exclude:
            plt.plot(axuv_data['t'], axuv_data[list(axuv_data.keys())[i]], label=f"Sensor: {list(axuv_data.keys())[i]}")
            
    plt.ylabel("Photodiode Current [A]")
    plt.xlabel("Time [s]")
    plt.legend()
    plt.title(f"AXUV Signal Over Time\nShot: {shot_number}")
    plt.show()
    
    return


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