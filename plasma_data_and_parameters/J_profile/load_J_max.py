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


def save_J_max_multishot(shot_list):
    J_max_data_path = "plasma_data_and_parameters/J_profile/J_max_data.json"
    if os.path.isfile(J_max_data_path):
        J_max_multishot = load.load_json_file(J_max_data_path)
    else:
        J_max_multishot = {}
    
    i = 1
    n = len(shot_list)
    for shot in shot_list:
        if str(shot) not in J_max_multishot.keys():
            J_max_info = load_J_max_array(shot)
            if type(J_max_info) != type(str()):
                J_max_array, J_max_errors, J_max_psibars, J_profile_times = J_max_info
                J_max_multishot[str(shot)] = {"data":list(J_max_array), "errors":list(J_max_errors), "psibars":J_max_psibars, "times":list(J_profile_times)}
            else:
                J_max_multishot[str(shot)] = J_max_info
                
        save.save_json(J_max_data_path, J_max_multishot)
        pb_pct(i, n)
        i += 1
        
    return

def load_J_max_array(shot_number):
    try:
        J_profile_multitime, J_profile_multitime_errors, J_profile_multitime_psibar = load_J.load_J_profile(shot_number)
    except:
        return "no_recon_data"
    
    J_profile_times = np.linspace(1/1000, len(J_profile_multitime)/1000, len(J_profile_multitime))
    
    J_max_array = []
    J_max_errors = []
    J_max_psibars = []
    for i in range(len(J_profile_multitime)):
        max_index = np.argmax(J_profile_multitime[i])
                
        J_max_array.append(J_profile_multitime[i][max_index])
        J_max_errors.append(J_profile_multitime_errors[i][max_index])
        J_max_psibars.append(J_profile_multitime_psibar[max_index])
    
    
    return J_max_array, J_max_errors, J_max_psibars, J_profile_times