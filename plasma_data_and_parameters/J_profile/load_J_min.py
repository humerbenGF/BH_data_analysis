# import packages
#################################################################
import numpy as np 
import matplotlib.pyplot as plt
import os

# import personal files
#################################################################
import plasma_data_and_parameters.J_profile.load_J_profile as load_J
import load_save_data.load_data as load
import load_save_data.save_data as save
from printouts.progress_bar import progress_bar_pct_only as pb_pct


def save_J_min_multishot(shot_list):
    J_min_data_path = "plasma_data_and_parameters/J_profile/J_min_data.json"
    if os.path.isfile(J_min_data_path):
        J_min_multishot = load.load_json_file(J_min_data_path)
    else:
        J_min_multishot = {}
    
    i = 1
    n = len(shot_list)
    for shot in shot_list:
        if str(shot) not in J_min_multishot.keys():
            J_min_info = load_J_min_array(shot)
            if type(J_min_info) != type(str()):
                J_min_array, J_min_errors, J_min_psibars, J_profile_times = J_min_info
                J_min_multishot[str(shot)] = {"data":list(J_min_array), "errors":list(J_min_errors), "psibars":list(J_min_psibars), "times":list(J_profile_times)}
            else:
                J_min_multishot[str(shot)] = J_min_info
                
        save.save_json(J_min_data_path, J_min_multishot)
        pb_pct(i, n)
        i += 1
        
    return

def load_J_min_array(shot_number):
    try:
        J_profile_multitime, J_profile_multitime_errors, J_profile_multitime_psibar = load_J.load_J_profile(shot_number)
    except:
        return "no_recon_data"
    
    J_profile_times = np.linspace(1/1000, len(J_profile_multitime)/1000, len(J_profile_multitime))
    
    J_min_array = []
    J_min_errors = []
    J_min_psibars = []
    for i in range(len(J_profile_multitime)):
        J_min_array.append(min(J_profile_multitime[i]))
        J_min_errors.append(J_profile_multitime_errors[i][np.argmin(J_profile_multitime[i])])
        J_min_psibars.append(J_profile_multitime_psibar[np.argmin(J_profile_multitime[i])])
    
    return J_min_array, J_min_errors, J_min_psibars, J_profile_times

