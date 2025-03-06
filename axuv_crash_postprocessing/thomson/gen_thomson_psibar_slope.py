# import libraries
#################################################################
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.integrate import cumtrapz
import numpy as np
import mpld3
import plotly.graph_objects as go
import os


# import personal files
#################################################################
import load_save_data.load_data as load_data
import load_save_data.save_data as save_data
import cursors.scatter_cursors as cursor
import cursors.add_click_action as click
import printouts.progress_bar as prog_bar
from axuv_crash_postprocessing.thomson.crash_thomson_scatter_helpers import *
from axuv_crash_postprocessing.thomson.crash_thomson_load_data import load_thomson_phase_data_by_shot
import axuv_crash_postprocessing.thomson.crash_thomson_data_filters as filter






def generate_thomson_psibar_slope_multishot(crash_data_dir):
    # load in data
    filename = "plasma_data_and_parameters/thomson/thomson_psibar_slopes.json"
    data_dict_by_shot = load_thomson_phase_data_by_shot(crash_data_dir, True, True, True, True)
    if os.path.isfile(filename):
        thomson_slopes_dict = load_data.load_json_file(filename)
    else:
        thomson_slopes_dict = {}

    print("GENERATING AND SAVING SLOPE DATA")
    cur = 1
    tot = len(data_dict_by_shot)
    for k in data_dict_by_shot.keys():
        if k not in thomson_slopes_dict.keys():
            slope_600_730_arr, slope_600_900_arr, slope_730_900_arr, slope_best_fit, times, phases = generate_thomson_psibar_slope_singleshot(data_dict_by_shot[k])
            thomson_slopes_dict[k] = {"slope_600_730_arr":slope_600_730_arr, "slope_600_900_arr":slope_600_900_arr, "slope_730_900_arr":slope_730_900_arr, "slope_best_fit":slope_best_fit, "times":times, "phases":phases}

        save_data.save_json(filename, thomson_slopes_dict)

        prog_bar.progress_bar_pct_only(cur, tot)
        cur += 1



    return


def generate_thomson_psibar_slope_singleshot(singleshot_data):
    # set up arrays to accept slopes
    slope_600_730_arr = []
    slope_600_900_arr = []
    slope_730_900_arr = []
    slope_best_fit    = []
    
    # set up arrays to accept x axis arrays
    times = []
    phases = []
    
    for i in range(min(len(singleshot_data['thomson_600_times']), len(singleshot_data['thomson_730_times']), len(singleshot_data['thomson_900_times']))):
        slope_600_730_arr.append((singleshot_data['thomson_600_temps'][i] - singleshot_data['thomson_730_temps'][i]) / (singleshot_data['thomson_600_psibars'][i] - singleshot_data['thomson_730_psibars'][i]))
        slope_600_900_arr.append((singleshot_data['thomson_600_temps'][i] - singleshot_data['thomson_900_temps'][i]) / (singleshot_data['thomson_600_psibars'][i] - singleshot_data['thomson_900_psibars'][i]))
        slope_730_900_arr.append((singleshot_data['thomson_730_temps'][i] - singleshot_data['thomson_900_temps'][i]) / (singleshot_data['thomson_730_psibars'][i] - singleshot_data['thomson_900_psibars'][i]))
        slope_best_fit.append(list(get_thomson_best_fit_slope(singleshot_data, i)))
        times.append(singleshot_data['thomson_600_times'][i])
        phases.append(singleshot_data['thomson_600_phases'][i])
    
    
    return slope_600_730_arr, slope_600_900_arr, slope_730_900_arr, slope_best_fit, times, phases


def get_thomson_best_fit_slope(singleshot_data, index):
    """
    Computes the best-fit slope (m) from a linear fit of Thomson temperature data 
    against corresponding psibar values for a given shot index.

    Parameters:
    ----------
    singleshot_data : dict
        Dictionary containing Thomson temperature and psibar values at different locations.
    index : int
        The index corresponding to the shot data to be used.

    Returns:
    -------
    float
        The slope (m) of the best-fit line.
    """
    # Extract y-values (Thomson temperatures) and x-values (psibar)
    thomson = np.array([singleshot_data['thomson_600_temps'][index], singleshot_data['thomson_730_temps'][index], singleshot_data['thomson_900_temps'][index]])
    
    psibar = np.array([singleshot_data['thomson_600_psibars'][index], singleshot_data['thomson_730_psibars'][index], singleshot_data['thomson_900_psibars'][index]])

    # Perform a linear fit: np.polyfit returns [m, b] where y = mx + b
    slope, intercept = np.polyfit(psibar, thomson, 1)

    return slope, intercept