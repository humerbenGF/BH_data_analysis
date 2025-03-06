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


def save_J_05_multishot(shot_list):
    J_05_data_path = "plasma_data_and_parameters/J_profile/J_05_data.json"
    if os.path.isfile(J_05_data_path):
        J_05_multishot = load.load_json_file(J_05_data_path)
    else:
        J_05_multishot = {}
    
    i = 1
    n = len(shot_list)
    for shot in shot_list:
        if str(shot) not in J_05_multishot.keys():
            J_05_info = load_J_05_array(shot)
            if type(J_05_info) != type(str()):
                J_05_array, J_05_errors, J_05_psibars, J_profile_times = J_05_info
                J_05_multishot[str(shot)] = {"data":list(J_05_array), "errors":list(J_05_errors), "psibars":J_05_psibars, "times":list(J_profile_times)}
            else:
                J_05_multishot[str(shot)] = J_05_info
                
        save.save_json(J_05_data_path, J_05_multishot)
        pb_pct(i, n)
        i += 1
        
    return

def load_J_05_array(shot_number):
    try:
        J_profile_multitime, J_profile_multitime_errors, J_profile_multitime_psibar = load_J.load_J_profile(shot_number)
    except:
        return "no_recon_data"
    
    J_profile_times = np.linspace(1/1000, len(J_profile_multitime)/1000, len(J_profile_multitime))
    
    J_05_array = []
    J_05_errors = []
    J_05_psibars = []
    for i in range(len(J_profile_multitime)):
        J_05_index = 0
                
        J_05_array.append(J_profile_multitime[i][J_05_index])
        J_05_errors.append(J_profile_multitime_errors[i][J_05_index])
        J_05_psibars.append(J_profile_multitime_psibar[J_05_index])
    
    
    return J_05_array, J_05_errors, J_05_psibars, J_profile_times