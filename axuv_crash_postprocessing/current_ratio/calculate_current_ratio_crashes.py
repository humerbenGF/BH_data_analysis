# import libraries
#################################################################
import numpy as np
import os
import matplotlib.pyplot as plt


# import personal files
#################################################################
import load_save_data.load_data as load_data
import load_save_data.save_data as save_data
import printouts.progress_bar as p_b


def calculate_current_ratio_crashes(crash_data_dir):
    # reformat crash_data_dir if necessary
    if crash_data_dir[-1] != "/":
        crash_data_dir += "/"
    
    # load in multishot info dictionaries
    crash_data = load_data.load_json_file(crash_data_dir + "crash_info_with_hardware_error.json")
    poloidal_data = load_data.load_json_file("plasma_data_and_parameters/poloidal_current/poloidal_current.json")
    toroidal_data = load_data.load_json_file("plasma_data_and_parameters/toroidal_current/toroidal_current.json")
    
    if os.path.isfile(crash_data_dir + "crash_info_with_cur_ratio.json"):
        multishot_crash_data_with_current = load_data.load_json_file(crash_data_dir + "crash_info_with_cur_ratio.json")
    else:
        multishot_crash_data_with_current = {}
    
    i = 1
    n = len(crash_data.keys())
    for shot in crash_data.keys():
        # cur_shot_toroidal_filename = f"plasma_data_and_parameters/toroidal_spline_current/toroidal_current_data/current_spline_{shot}.json"
        if type(crash_data[shot]) != type(str()) and shot not in multishot_crash_data_with_current.keys():
            # if os.path.isfile(cur_shot_toroidal_filename) and shot in poloidal_data.keys():
            if shot in poloidal_data.keys() and shot in toroidal_data.keys():
                # toroidal_spline_current_dict = load_data.load_json_file(cur_shot_toroidal_filename)
                multishot_crash_data_with_current[shot] = generate_crash_current_ratio_singleshot(crash_data[shot], toroidal_data[shot], poloidal_data[shot])
                # multishot_crash_data_with_current[shot] = generate_crash_current_ratio_spline_singleshot(crash_data[shot], toroidal_spline_current_dict, poloidal_data[shot])

        save_data.save_json(crash_data_dir + "crash_info_with_cur_ratio.json", multishot_crash_data_with_current)

        p_b.progress_bar_pct_only(i, n)
        i += 1
    
    return


def generate_crash_current_ratio_singleshot(singleshot_crash_data, toroidal_current_dict, poloidal_current_dict):
    current_ratio = []
    for i in range(len(singleshot_crash_data['times'])):
        if type(str()) in [type(toroidal_current_dict), type(poloidal_current_dict), type(singleshot_crash_data)]:
            return 'error'
        t_cur = interp_poloidal_cur(singleshot_crash_data['times'][i], toroidal_current_dict['data'])
        p_cur = interp_poloidal_cur(singleshot_crash_data['times'][i], poloidal_current_dict['data'])
        current_ratio.append(t_cur/p_cur)
    
    return current_ratio



def generate_crash_current_ratio_spline_singleshot(singleshot_crash_data, toroidal_current_dict, poloidal_current_dict):
    current_ratio = []
    for i in range(len(singleshot_crash_data['times'])):
        if type(str()) in [type(toroidal_current_dict), type(poloidal_current_dict), type(singleshot_crash_data)]:
            return 'error'
        t_cur = toroidal_current_dict['data'][find_closest_index(toroidal_current_dict['time'], singleshot_crash_data['times'][i])]
        p_cur = interp_poloidal_cur(singleshot_crash_data['times'][i], poloidal_current_dict['data'])
        current_ratio.append(t_cur/p_cur)
    
    return current_ratio


def interp_poloidal_cur(time, pol_current_array):
    time = time*1000
    return (pol_current_array[int(time)] - pol_current_array[int(time) - 1]) * (time - int(time)) + pol_current_array[int(time) - 1]


def find_closest_index(t, t0):
    # Convert the list to a numpy array if it isn't one already
    t = np.array(t)
    
    # Find the index of the closest value to t0
    closest_index = np.abs(t - t0).argmin()
    
    return closest_index