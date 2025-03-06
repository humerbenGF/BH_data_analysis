# import libraries
#################################################################
import matplotlib.pyplot as plt

# import personal files
#################################################################
from axuv_crash_postprocessing.thomson.crash_thomson_data_filters_helpers import *


def filter_by_slope(slope_at_phase, slope_minimum, slope_maximum):
    shots_list_new = []
    for k in slope_at_phase.keys():
        if slope_at_phase[k] > slope_minimum and slope_at_phase < slope_maximum:
            shots_list_new.append(slope_at_phase[k])
        
    return shots_list_new
    

def get_slope_at_phase_by_shot(data_dict_by_shot, thomson_position, phase_of_interest, plot_hist=False):
    slope_at_phase = {}
    for s in data_dict_by_shot.keys():
        slope_at_phase[s] = calc_slope_at_phase_singleshot(data_dict_by_shot[s], thomson_position, phase_of_interest)
    
    if plot_hist:
        plt.hist(slope_at_phase.values(), bins=100)
        plt.title(f"Histogram of the Slope of Temperature Over Phase\n(Phase = {phase_of_interest})")
        plt.xlabel("Slope")
        plt.show()
    
    return slope_at_phase