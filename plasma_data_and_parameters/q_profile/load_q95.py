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


def save_q95_multishot(shot_list):
    q95_data_path = "plasma_data_and_parameters/q_profile/q95_data.json"
    if os.path.isfile(q95_data_path):
        q95_multishot = load.load_json_file(q95_data_path)
    else:
        q95_multishot = {}
    
    i = 1
    n = len(shot_list)
    for shot in shot_list:
        if str(shot) not in q95_multishot.keys():
            q95_info = load_q95_array(shot)
            if type(q95_info) != type(str()):
                q95_array, q95_errors, q_profile_times = q95_info
                q95_multishot[str(shot)] = {"data":list(q95_array), "errors":list(q95_errors), "times":list(q_profile_times)}
            else:
                q95_multishot[str(shot)] = q95_info
                
        save.save_json(q95_data_path, q95_multishot)
        pb_pct(i, n)
        i += 1
        
    return


def load_q95_array(shot_number):
    try:
        q_profile_multitime, q_profile_multitime_errors, q_profile_multitime_psibar = load_q.load_q_profile(shot_number)
    except:
        return "no_recon_data"
    
    q_profile_times = np.linspace(1/1000, len(q_profile_multitime)/1000, len(q_profile_multitime))
    
    q95_array = []
    q95_errors = []
    for i in range(len(q_profile_multitime)):
        q95_array.append(q_profile_multitime[i][np.where(q_profile_multitime_psibar == 0.95)[0][0]])
        q95_errors.append(q_profile_multitime_errors[i][np.where(q_profile_multitime_psibar == 0.95)[0][0]])
    
    return q95_array, q95_errors, q_profile_times