# add AURORA_REPOS to path
#################################################################
import os
import sys
sys.path.append(os.environ['AURORA_REPOS'])

# import functions from AXUV_crash_detection
#################################################################
from AXUV_crash_detection import load_axuv_crash_data           # type: ignore


# import libraries
#################################################################
import matplotlib.pyplot as plt
import numpy as np
import json
import bson





def generate_timeseries_average(rise_category, fall_category, average='median', threshold=0.16, normalize=False, lifetime_stretching=False, min_lifetime=0.001):
    # generate the list of shots that fall into the correct category
    prelim_shots_list = make_shots_list(rise_category, fall_category)
    lifetime_dict, lifetime_list = load_lifetimes(prelim_shots_list)
    
    shots_list = []
    for s in range(len(prelim_shots_list)):
        if lifetime_list[s] != "no data":
            if lifetime_list[s] > min_lifetime:
                shots_list.append(prelim_shots_list[s])
        
    if len(shots_list) == 0:
        return -1
    
    # load in all the data
    multishot_data = []
    for s in shots_list:
        data = load_bson_file(filename=shot_number_to_filename(s))
        multishot_data.append(data)
    
    # stretch to lifetimes if relevant
    if lifetime_stretching:
        multishot_data = stretch_to_lifetimes(shots_list, multishot_data[:])
        
    # normalize data if relevant
    if normalize:
        multishot_data = normalize_multishot_data(multishot_data[:])

    # calculate the mean
    data_mean_timeseries = {}
    data_stdev_timeseries = {}
    lower_bound_timeseries = {}
    upper_bound_timeseries = {}
    for k in multishot_data[0].keys():
        if k != "t":
            data_mean_timeseries[k] = []
            data_stdev_timeseries[k] = []
            lower_bound_timeseries[k] = []
            upper_bound_timeseries[k] = []
            for i in range(len(multishot_data[0][k])):
                singletime_array = []
                for s in range(len(multishot_data)):
                    singletime_array.append(multishot_data[s][k][i])
                if len(singletime_array) > 0:
                    if average == 'median':
                        data_mean_timeseries[k].append(np.median(singletime_array))
                    elif average == 'mean':
                        data_mean_timeseries[k].append(np.mean(singletime_array))
                    # calculate the lower and upper thresholds
                    if threshold > 0.5 or len(singletime_array) < 3:
                        data_stdev_timeseries[k].append(np.std(singletime_array))
                        lower_bound_timeseries[k].append(data_mean_timeseries[k][i] - data_stdev_timeseries[k][i])
                        upper_bound_timeseries[k].append(data_mean_timeseries[k][i] + data_stdev_timeseries[k][i])
                    else:
                        singletime_len = len(singletime_array)
                        num_entries = threshold*singletime_len
                        singletime_array.sort()
                        num_entries_floor = int(num_entries)
                        offset = num_entries - num_entries_floor
                        lower_bound = singletime_array[num_entries_floor] - abs(singletime_array[num_entries_floor] - singletime_array[num_entries_floor - 1]) * offset
                        upper_bound = singletime_array[singletime_len - (num_entries_floor + 1)] + abs(singletime_array[singletime_len - num_entries_floor] - singletime_array[singletime_len - (num_entries_floor + 1)]) * offset
                        lower_bound_timeseries[k].append(lower_bound)
                        upper_bound_timeseries[k].append(upper_bound)

        else:
            data_mean_timeseries["t"]  = multishot_data[s]["t"]
            data_stdev_timeseries["t"] = multishot_data[s]["t"]

    return data_mean_timeseries, lower_bound_timeseries, upper_bound_timeseries, shots_list



def plot_all_ts_avg_individually(sensor, min_lifetime, average='median', threshold=1):
    training_classification = load_json_file("axuv_categories_analysis/training_classifications.json")
    rise_categories = training_classification["rise_classifications"].keys()
    fall_categories = training_classification["fall_classifications"].keys()
    
    all_cat_array = []
    for i in rise_categories:
        for j in fall_categories:
            all_cat_array.append([int(i), int(j)])
    
    for c in all_cat_array:
        if generate_timeseries_average(c[0], c[1]) != -1:
            non_normalized_mean, non_normalized_lower_bound_timeseries, non_normalized_upper_bound_timeseries, shots_list = generate_timeseries_average(c[0], c[1], average, threshold, False, True, min_lifetime=min_lifetime)
            normalized_mean, normalized_lower_bound_timeseries, normalized_upper_bound_timeseries, shots_list = generate_timeseries_average(c[0], c[1], average, threshold, True, True, min_lifetime=min_lifetime)
        else:
            continue
        
        # get upper and lower bound dictionaries for the plot
        non_normalized_upper_bound_dictionary = non_normalized_upper_bound_timeseries
        non_normalized_lower_bound_dictionary = non_normalized_lower_bound_timeseries
        normalized_upper_bound_dictionary = normalized_upper_bound_timeseries
        normalized_lower_bound_dictionary = normalized_lower_bound_timeseries
            
        
        colors = ['blue', 'red']
        for k in non_normalized_mean.keys():
            if k == sensor:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))
                labelstring = "Rise Classification: " + training_classification["rise_classifications"][str(c[0])] + " | Fall Classification: " + training_classification["fall_classifications"][str(c[1])]
                ax1.plot(non_normalized_mean["t"], non_normalized_mean[k], label=labelstring, color=colors[0])
                ax1.plot(non_normalized_mean["t"], non_normalized_lower_bound_dictionary[k], color=colors[0], alpha=0.4)
                ax1.plot(non_normalized_mean["t"], non_normalized_upper_bound_dictionary[k], color=colors[0], alpha=0.4)
                ax1.fill_between(non_normalized_mean["t"], non_normalized_lower_bound_dictionary[k], non_normalized_upper_bound_dictionary[k], color=colors[0], alpha=0.3, interpolate=True)
    
                ax2.plot(normalized_mean["t"], normalized_mean[k], label=labelstring, color=colors[1])
                ax2.plot(normalized_mean["t"], normalized_lower_bound_dictionary[k], color=colors[1], alpha=0.4)
                ax2.plot(normalized_mean["t"], normalized_upper_bound_dictionary[k], color=colors[1], alpha=0.4)
                ax2.fill_between(normalized_mean["t"], normalized_lower_bound_dictionary[k], normalized_upper_bound_dictionary[k], color=colors[1], alpha=0.3, interpolate=True)
    
                ax1.set_title("Raw Current Signal Normalized to Lifetime")
                ax1.set_ylabel("Photodiode Current [nA]")
                ax1.set_xlabel("Normalized Time [Fraction of Lifetime]")
                ax1.legend()
                
                ax2.set_title("Normalized Current Signal Over Normalized Lifetime")
                ax2.set_ylabel("Normalized Photodiode Current")
                ax2.set_xlabel("Normalized Time [Fraction of Lifetime]")
                ax2.legend()
                
                fig.suptitle("Photodiode Signals Over Normalized Lifetime for " + str(len(shots_list)) + " Shots\n" + labelstring)

        plt.tight_layout()
        folder_path = "axuv_categories_analysis/plots"
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        plt.savefig(folder_path + "/ts_avg_" + str(c[0]) + "-" + str(c[1]) + ".png")

    return
    




def plot_timeseries_average(categories_array, sensor, average='median', normalize=False, lifetime_stretching=False, min_lifetime=0.001):
    training_classification = load_json_file("axuv_categories_analysis/training_classifications.json")
    
    multicategory_data = []
    for i in range(len(categories_array)):
        rise_category, fall_category = categories_array[i][0], categories_array[i][1]
        data_mean_timeseries, lower_bound_timeseries, upper_bound_timeseries, shots_list = generate_timeseries_average(rise_category, fall_category, average, normalize, lifetime_stretching, min_lifetime)
        
        # get upper and lower bound dictionaries for the plot
        upper_bound_dictionary = upper_bound_timeseries
        lower_bound_dictionary = lower_bound_timeseries
        
        
        multicategory_data.append([data_mean_timeseries, upper_bound_dictionary, lower_bound_dictionary])
    
    colors=["blue", "red", "green"]
    i = 0
    
    plt.figure(figsize=(16,9))
    
    for i in range(len(multicategory_data)):
        data_mean_timeseries   = multicategory_data[i][0]
        upper_bound_dictionary = multicategory_data[i][1]
        lower_bound_dictionary = multicategory_data[i][2]
        
        for k in data_mean_timeseries.keys():
            if k == sensor:
                labelstring = "Rise Classification: " + training_classification["rise_classifications"][str(categories_array[i][0])] + " | Fall Classification: " + training_classification["fall_classifications"][str(categories_array[i][1])]
                plt.plot(data_mean_timeseries["t"], data_mean_timeseries[k], label=labelstring, color=colors[i])
                plt.plot(data_mean_timeseries["t"], lower_bound_dictionary[k], color=colors[i], alpha=0.4)
                plt.plot(data_mean_timeseries["t"], upper_bound_dictionary[k], color=colors[i], alpha=0.4)
                plt.fill_between(data_mean_timeseries["t"], lower_bound_dictionary[k], upper_bound_dictionary[k], color=colors[i], alpha=0.3, interpolate=True)
                i += 1
    
    if not normalize and not lifetime_stretching:
        plt.ylabel("Photodiode Current [nA]")
    else:
        plt.ylabel("Normalized Photodiode Current")

    if not lifetime_stretching:
        plt.xlabel("Time [s]")
    else:
        plt.xlabel("Normalized Time [Fraction of Lifetime]")
    
    
    
    plt.title("Average of AXUV Signal for Categorized Data\nSensor: " + sensor + ", Number of Shots: " + str(len(shots_list)))
    plt.legend()
    plt.show()
    
    return


def stretch_to_lifetimes(shot_list, multishot_data):
    lifetime_dict, lifetime_list = load_lifetimes(shot_list)
    
    # normalize lifetimes
    for s in range(len(multishot_data)):
        lifetime_index = find_closest_index(multishot_data[s]["t"], lifetime_list[s])
        zero_index = find_closest_index(multishot_data[s]["t"], 0)
        for k in multishot_data[s].keys():
            multishot_data[s][k] = multishot_data[s][k][zero_index:lifetime_index]
            for i in range(len(multishot_data[s][k])):
                multishot_data[s][k][i] = multishot_data[s][k][i] / lifetime_list[s]
    
    # find the minimum length
    minimum_length = len(multishot_data[s][k])
    minimum_length_index = s
    for s in range(len(multishot_data)):
        for k in multishot_data[s].keys():
            temp_len = len(multishot_data[s][k])
            if temp_len < minimum_length:
                minimum_length = temp_len
                minimum_length_index = s
    
    # make a dictionary to keep track of indices
    indices_dict = {}
    for k in multishot_data[minimum_length_index].keys():
        indices_dict[k] = []
        for s in range(len(multishot_data)):
            indices_dict[k].append(0)
    
    # make the new multishot_data array to be filled
    new_multishot_data = []
    for s in range(len(multishot_data)):
        new_multishot_data.append({})
        for k in multishot_data[s].keys():
            new_multishot_data[s][k] = []
            
    
    
    dt_min = multishot_data[minimum_length_index]["t"][1] - multishot_data[minimum_length_index]["t"][0]
    prev_mean = 0
    # use the minimum length to condense the other arrays
    for k in multishot_data[minimum_length_index].keys():
        for i in range(len(multishot_data[minimum_length_index][k])):
            bin_lhs = multishot_data[minimum_length_index]["t"][i] - (dt_min / 2)
            bin_rhs = multishot_data[minimum_length_index]["t"][i] + (dt_min / 2)
            for s in range(len(multishot_data)):
                temp_index = indices_dict[k][s]
                temp_list = []
                while multishot_data[s]["t"][temp_index] < bin_rhs:
                    temp_list.append(multishot_data[s][k][temp_index])
                    temp_index += 1
                    if temp_index == len(multishot_data[s]["t"]):
                        break
                indices_dict[k][s] = temp_index
                if len(temp_list) > 0:
                    mean_val = np.mean(temp_list)
                else:
                    mean_val = prev_mean
                new_multishot_data[s][k].append(mean_val)
                prev_mean = mean_val



    return new_multishot_data







def make_shots_list(rise_category, fall_category):
    if fall_category != "all":
        fall_data = load_json_file("axuv_categories_analysis/axuv_fall_training_data.json")[str(fall_category)]
    if rise_category != "all":
        rise_data = load_json_file("axuv_categories_analysis/axuv_rise_training_data.json")[str(rise_category)]
        
    if rise_category == fall_category == "all":
        print("Rise and fall categories cannot both be all.")
        
    if fall_category == "all":
        shots_list = rise_data
    elif rise_category == "all":
        shots_list = fall_data
    else:
        shots_list = []
        for i in range(len(rise_data)):
            if rise_data[i] in fall_data:
                shots_list.append(rise_data[i])
    
    return shots_list





def load_json_file(filename):
    """
    Loads a JSON file and returns the data as a Python object.

    Parameters:
    filename (str): The name or path of the JSON file to load.

    Returns:
    dict or list: The data parsed from the JSON file.
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        

    
def load_bson_file(filename):
    """
    Loads a BSON file and returns the data as a Python object.

    Parameters:
    filename (str): The name or path of the BSON file to load.

    Returns:
    dict or list: The data parsed from the BSON file.
    """
    try:
        with open(filename, 'rb') as file:
            data = bson.decode(file.read())
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except bson.errors.InvalidBSON:
        print(f"Error: The file '{filename}' is not a valid BSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        

def shot_number_to_filename(shot_number):
    return "preprocessed_data/timeseries_plotting/" + str(int(shot_number/1000) * 1000) + "/" + str(shot_number) + "_ts.bson"

def normalize_multishot_data(multishot_data):
    for s in range(len(multishot_data)):
        for k in multishot_data[s].keys():
            if k != "t":
                max_val = max(multishot_data[s][k])
                for i in range(len(multishot_data[s][k])):
                    multishot_data[s][k][i] = multishot_data[s][k][i] / max_val
                
    return multishot_data


def load_lifetimes(shot_list):
    lifetime_dict = load_json_file("plasma_lifetime/lifetimes_list.json")
    lifetime_list = []
    for s in shot_list:
        lifetime_list.append(lifetime_dict[str(s)])
    
    return lifetime_dict, lifetime_list




def find_closest_index(time_array, ref_time):
    """
    Perform a binary search to find the index of the time in time_array closest to ref_time.

    Parameters:
    time_array (list of floats): The array of times (must be sorted).
    ref_time (float): The reference time to find the closest time to.

    Returns:
    int: The index of the closest time in time_array.
    """
    left, right = 0, len(time_array) - 1

    # Handle edge cases where ref_time is out of the bounds of the array
    if ref_time <= time_array[left]:
        return left
    if ref_time >= time_array[right]:
        return right

    while left <= right:
        mid = (left + right) // 2

        # Check if mid is the closest
        if time_array[mid] == ref_time:
            return mid

        # Adjust the search bounds
        if time_array[mid] < ref_time:
            left = mid + 1
        else:
            right = mid - 1

    # When the loop exits, left is the index of the smallest number greater than ref_time,
    # and right is the index of the largest number less than ref_time.

    # Compare which is closer to ref_time
    if abs(time_array[left] - ref_time) < abs(time_array[right] - ref_time):
        return left
    else:
        return right