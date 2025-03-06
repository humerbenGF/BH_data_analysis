# import libraries
#################################################################
import numpy as np


def calc_slope_at_phase_singleshot(data_dict_singleshot, thomson_position, phase_of_interest):
    
    sorted_indices_phase = np.argsort(data_dict_singleshot[f"thomson_{thomson_position}_phases"])
    
    if data_dict_singleshot[f"thomson_{thomson_position}_phases"][sorted_indices_phase[-1]] < phase_of_interest or data_dict_singleshot[f"thomson_{thomson_position}_phases"][sorted_indices_phase[0]] > phase_of_interest or len(sorted_indices_phase) < 2:
        return np.NaN
    
    for i in range(len(sorted_indices_phase)):
        if data_dict_singleshot[f"thomson_{thomson_position}_phases"][sorted_indices_phase[i]] < phase_of_interest and data_dict_singleshot[f"thomson_{thomson_position}_phases"][sorted_indices_phase[i+1]] > phase_of_interest:
            break
    
    slope = (data_dict_singleshot[f"thomson_{thomson_position}_temps"][sorted_indices_phase[i+1]] - data_dict_singleshot[f"thomson_{thomson_position}_temps"][sorted_indices_phase[i]]) / (data_dict_singleshot[f"thomson_{thomson_position}_phases"][sorted_indices_phase[i+1]] - data_dict_singleshot[f"thomson_{thomson_position}_phases"][sorted_indices_phase[i]])
    
    return slope