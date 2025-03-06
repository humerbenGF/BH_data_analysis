# import packages
#################################################################
import numpy as np 
import matplotlib.pyplot as plt
import os

# import personal files
#################################################################
import plasma_data_and_parameters.q_profile.load_q_profile as load_q
import load_save_data.load_data as load
import load_save_data.save_data as save
from printouts.progress_bar import progress_bar_pct_only as pb_pct


def save_q_min_multishot(shot_list):
    q_min_data_path = "plasma_data_and_parameters/q_profile/q_min_data.json"
    if os.path.isfile(q_min_data_path):
        q_min_multishot = load.load_json_file(q_min_data_path)
    else:
        q_min_multishot = {}
    
    i = 1
    n = len(shot_list)
    for shot in shot_list:
        if str(shot) not in q_min_multishot.keys():
            q_min_info = load_q_min_array(shot)
            if type(q_min_info) != type(str()):
                q_min_array, q_min_errors, q_profile_times = q_min_info
                q_min_multishot[str(shot)] = {"data":list(q_min_array), "errors":list(q_min_errors), "times":list(q_profile_times)}
            else:
                q_min_multishot[str(shot)] = q_min_info
                
        save.save_json(q_min_data_path, q_min_multishot)
        pb_pct(i, n)
        i += 1
        
    return

def load_q_min_array(shot_number):
    try:
        q_profile_multitime, q_profile_multitime_errors, q_profile_multitime_psibar = load_q.load_q_profile(shot_number)
    except:
        return "no_recon_data"
    
    q_profile_times = np.linspace(1/1000, len(q_profile_multitime)/1000, len(q_profile_multitime))
    
    q_min_array = []
    q_min_errors = []
    for i in range(len(q_profile_multitime)):
        q_min_array.append(min(q_profile_multitime[i]))
        q_min_errors.append(q_profile_multitime_errors[i][np.argmin(q_profile_multitime[i])])
    
    
    return q_min_array, q_min_errors, q_profile_times