# import packages
#################################################################
import numpy as np 
import matplotlib.pyplot as plt
import os
import pandas as pd

# import personal files
#################################################################
import load_save_data.load_data as load
import load_save_data.save_data as save
from printouts.progress_bar import progress_bar_pct_only as pb_pct



def search_based_on_example_shots(example_shots_list, crash_dir, search_parameters, search_parameters_tolerances):
    search_dict = {}
    for search_parameter in search_parameters:
        search_dict[search_parameter] = []
    
    # load in files
    crash_info_multishot = load.load_json_file(f"{crash_dir}/crash_info_with_hardware_error.json")
    lifetimes_multishot = load.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    # get crash info parameters for example shots
    for shot in example_shots_list:
        search_dict = get_crash_info_search_parameters(shot, crash_info_multishot, search_parameters, search_dict)

    # get search parameters from means
    search_dict_means = {}
    for search_parameter in search_parameters:
        search_dict_means[search_parameter] = np.mean(search_dict[search_parameter])
        
    # l
    
    shots_of_interest = generate_shots_of_interest(crash_info_multishot, lifetimes_multishot)
    
    # now search for similar shots
    similar_shots = []
    for shot in shots_of_interest:
        singleshot_info_parameters = get_crash_info_singleshot_parameters(shot, crash_info_multishot, search_parameters)
        valid=True
        for i in range(len(search_parameters)):
            if abs(search_dict_means[search_parameters[i]] - singleshot_info_parameters[search_parameters[i]]) > search_parameters_tolerances[i]:
                valid = False

        if valid:
            similar_shots.append(shot)
    
    print(search_dict, "\n\n")
    print(search_dict_means, "\n\n")
    print(similar_shots)
    
    return


def generate_shots_of_interest(crash_info_multishot, lifetimes_multishot):
    shots_of_interest = []
    for k in crash_info_multishot.keys():
            if k in lifetimes_multishot.keys():
                if type(lifetimes_multishot[k]) != type(str()) and type(crash_info_multishot[k]) != type(str()):
                    if len(crash_info_multishot[k]['times']) > 0:
                        shots_of_interest.append(int(k))
    
    return shots_of_interest



def get_crash_info_singleshot_parameters(shot, crash_info_multishot, search_parameters):
    info_dict = {}
    for search_parameter in search_parameters:
        if str(shot) in crash_info_multishot.keys():
            if type(crash_info_multishot[str(shot)]) != type(str()):
                if len(crash_info_multishot[str(shot)]['times']) > 0:
                    if search_parameter == "num_crashes":
                        info_dict[search_parameter] = (len(crash_info_multishot[str(shot)]['times']))
                    if search_parameter == "max_crash_amp":
                        info_dict[search_parameter] = (max(crash_info_multishot[str(shot)]['amps']))
                    if search_parameter == "max_crash_amp_norm":
                        info_dict[search_parameter] = (max(crash_info_multishot[str(shot)]['rel_amps']))
                    if search_parameter == "time_largest_crash":
                        info_dict[search_parameter] = (crash_info_multishot[str(shot)]['times'][np.argmax(crash_info_multishot[str(shot)]['rel_amps'])])
                    if search_parameter == "first_crash_amp":
                        info_dict[search_parameter] = (crash_info_multishot[str(shot)]['amps'][0])
                    if search_parameter == "first_crash_amp_norm":
                        info_dict[search_parameter] = (crash_info_multishot[str(shot)]['rel_amps'][0])
                    if search_parameter == "first_crash_time":
                        info_dict[search_parameter] = (crash_info_multishot[str(shot)]['times'][0])
                    
    return info_dict



def get_crash_info_search_parameters(shot, crash_info_multishot, search_parameters, search_dict):
    for search_parameter in search_parameters:
        if str(shot) in crash_info_multishot.keys():
            if type(crash_info_multishot[str(shot)]) != type(str()):
                if len(crash_info_multishot[str(shot)]['times']) > 0:
                    if search_parameter == "num_crashes":
                        search_dict[search_parameter].append(len(crash_info_multishot[str(shot)]['times']))
                    if search_parameter == "max_crash_amp":
                        search_dict[search_parameter].append(max(crash_info_multishot[str(shot)]['amps']))
                    if search_parameter == "max_crash_amp_norm":
                        search_dict[search_parameter].append(max(crash_info_multishot[str(shot)]['rel_amps']))
                    if search_parameter == "time_largest_crash":
                        search_dict[search_parameter].append(crash_info_multishot[str(shot)]['times'][np.argmax(crash_info_multishot[str(shot)]['rel_amps'])])
                    if search_parameter == "first_crash_amp":
                        search_dict[search_parameter].append(crash_info_multishot[str(shot)]['amps'][0])
                    if search_parameter == "first_crash_amp_norm":
                        search_dict[search_parameter].append(crash_info_multishot[str(shot)]['rel_amps'][0])
                    if search_parameter == "first_crash_time":
                        search_dict[search_parameter].append(crash_info_multishot[str(shot)]['times'][0])
                    
    return search_dict