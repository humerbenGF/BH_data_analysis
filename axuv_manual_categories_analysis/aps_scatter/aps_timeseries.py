# add AURORA_REPOS to path
#################################################################
import os
import sys

# import libraries
#################################################################
import matplotlib.pyplot as plt
import numpy as np
import json
import bson

# import personal files
#################################################################
import load_save_data.load_data as load_data


# plot timeserires averaged data
#################################################################
def plot_timeseries_average(sensor="sn021", average='median', normalize=True, lifetime_stretching=True, min_lifetime=0.001, threshold=0.20, shots_of_interest=[22714, 20342], plot_special_shots=True, plot_averages=True):
    multicategory_data = []
    dome_bin = [True, False]
    final_shot_of_interest_ts = []
    shots_of_interest_list = []
    for i in range(len(dome_bin)):
        data_mean_timeseries, lower_bound_timeseries, upper_bound_timeseries, shots_of_interest_ts, shots_list = gen_ts_data(dome_bin[i], lifetime_stretching, normalize, threshold, average, min_lifetime, shots_of_interest)
        
        for i in range(len(shots_of_interest_ts)):
            if shots_of_interest_ts[i] != False:
                final_shot_of_interest_ts.append(shots_of_interest_ts[i])
                shots_of_interest_list.append(shots_of_interest[i])

        # get upper and lower bound dictionaries for the plot
        upper_bound_dictionary = upper_bound_timeseries
        lower_bound_dictionary = lower_bound_timeseries


        multicategory_data.append([data_mean_timeseries, upper_bound_dictionary, lower_bound_dictionary])
        
        indices_of_interest = []
        for shot_of_interest in shots_of_interest:
            if shot_of_interest in shots_list:
                indices_of_interest.append([i, shots_list.index(shot_of_interest)])
    
    shots_of_interest_ts = final_shot_of_interest_ts

    colors=["red", "red", "red", "blue", "blue", "blue"]
    markers=["x", "o", "D", "x", "o", "D"]
    
    plt.rcParams['font.size'] = 16  # Change all font sizes
    plt.rcParams['axes.titlesize'] = 20  # Title font size
    plt.rcParams['axes.labelsize'] = 18  # Axis label font size
    plt.rcParams['xtick.labelsize'] = 14  # X tick label size
    plt.rcParams['ytick.labelsize'] = 14  # Y tick label size
    plt.rcParams['legend.fontsize'] = 14  # Legend font size
    
    plt.figure(figsize=(12,6))
    
    if plot_averages:
        for i in range(len(multicategory_data)):
            data_mean_timeseries   = multicategory_data[i][0]
            upper_bound_dictionary = multicategory_data[i][1]
            lower_bound_dictionary = multicategory_data[i][2]
            
            for k in data_mean_timeseries.keys():
                if k == sensor:
                    if i == 0:
                        labelstring = "Dome"
                    else:
                        labelstring = "Non-Dome"
                    plt.plot(data_mean_timeseries["t"], data_mean_timeseries[k], label=labelstring, color=colors[i])
                    plt.plot(data_mean_timeseries["t"], lower_bound_dictionary[k], color=colors[i], alpha=0.4)
                    plt.plot(data_mean_timeseries["t"], upper_bound_dictionary[k], color=colors[i], alpha=0.4)
                    plt.fill_between(data_mean_timeseries["t"], lower_bound_dictionary[k], upper_bound_dictionary[k], color=colors[i], alpha=0.3, interpolate=True, label=labelstring + " Median ± σ")
                
    # add single curve to the plot
    if plot_special_shots:
        i = 0
        for shot_of_interest_ts in shots_of_interest_ts:
            nth = 100
            plt.plot(shot_of_interest_ts["t"], shot_of_interest_ts[sensor], linewidth=2, color=colors[i], alpha=0.5)
            plt.scatter(shot_of_interest_ts["t"][::nth+5*i%3], shot_of_interest_ts[sensor][::nth+5*i%3], marker=markers[i], color=colors[i], label="Shot " + str(shots_of_interest_list[i]), s=40)
            i += 1
        plt.title("AXUV Timeseries Signals for Dome and Non-Dome Shots")
    else:
        plt.title("Average AXUV Timeseries Signals for Dome and Non-Dome Shots")
        
    plt.hlines([0], [-0.5], [1.5], colors=['k'])
    
    if not normalize:
        plt.ylabel("Photodiode Current [nA]")
    else:
        plt.ylabel("Normalized Photodiode Current")

    if not lifetime_stretching:
        plt.xlabel("Time [s]")
    else:
        plt.xlabel("Normalized Time [Fraction of Total Plasma Lifetime]")
    

    plt.legend()
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.savefig("test.png", dpi=400)
    
    return


# generate timeserires averaged data
#################################################################
def gen_ts_data(dome=False, lifetime_stretching=True, normalize=True, threshold=0.15, average='median', min_lifetime=0.001, shots_of_interest=[22714]):
        # generate the list of shots that fall into the correct category
    dome_shots_list, non_dome_shots_list = make_shots_lists_dome_non_dome()
    if dome:
        prelim_shots_list = dome_shots_list
    else:
        prelim_shots_list = non_dome_shots_list
        
    lifetime_dict, lifetime_list = load_lifetimes(prelim_shots_list)
    
    shots_list = []
    for s in range(len(prelim_shots_list)):
        if type(lifetime_list[s]) != type(""):
            if lifetime_list[s] > min_lifetime:
                shots_list.append(prelim_shots_list[s])
        
    if len(shots_list) == 0:
        return -1
    
    # load in all the data
    multishot_data = []
    for s in shots_list:
        data = load_data.load_bson_file("preprocessed_data/axuv_timeseries_plotting/" + str(int(s/1000) * 1000) + "/" + str(s) + "_ts.bson")
        multishot_data.append(data)
    
    # stretch to lifetimes if relevant
    if lifetime_stretching:
        multishot_data = stretch_to_lifetimes(shots_list, multishot_data[:])
        
    # normalize data if relevant
    if normalize:
        multishot_data = normalize_multishot_data(multishot_data[:])

    shots_of_interest_timeseries = []
    for shot_of_interest in shots_of_interest:
        if shot_of_interest in shots_list:
            shots_of_interest_timeseries.append(multishot_data[shots_list.index(shot_of_interest)])
        else:
            shots_of_interest_timeseries.append(False)

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

    return data_mean_timeseries, lower_bound_timeseries, upper_bound_timeseries, shots_of_interest_timeseries, shots_list


# stretch to lifetimes
#################################################################
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


# helper functions
#################################################################
def make_shots_lists_dome_non_dome():
    data_categories = load_data.load_json_file("axuv_categories_analysis/aps_scatter/thomson_classification.json")

    dome_list = []
    non_dome_list = []
    for sustainment in data_categories.keys():
        for s in data_categories[sustainment].keys():
            if data_categories[sustainment][s][0] in ["2"]:
                dome_list.append(int(s))
            else:
                non_dome_list.append(int(s))
        
    return dome_list, non_dome_list

def load_lifetimes(shot_list):
    lifetimes_dict = load_data.load_json_file("plasma_lifetime/lifetimes_list.json")
    lifetimes_list = []
    for s in shot_list:
        lifetimes_list.append(lifetimes_dict[str(s)])
        
    return lifetimes_dict, lifetimes_list

def normalize_multishot_data(multishot_data):
    for s in range(len(multishot_data)):
        for k in multishot_data[s].keys():
            if k != "t":
                max_val = max(multishot_data[s][k][:int(0.7*len(multishot_data[s][k]))])
                for i in range(len(multishot_data[s][k])):
                    multishot_data[s][k][i] = multishot_data[s][k][i] / max_val
                
    return multishot_data

def find_closest_index(time_array, ref_time):
    left, right = 0, len(time_array) - 1

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

    if abs(time_array[left] - ref_time) < abs(time_array[right] - ref_time):
        return left
    else:
        return right