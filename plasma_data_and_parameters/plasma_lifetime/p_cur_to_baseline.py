# import libraries
#################################################################
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import math


# set AURORA_REPOS variable
#################################################################
import os
import sys
sys.path.append(os.environ['AURORA_REPOS'])


# import general fusion files
#################################################################
from GF_data_tools import plotting          # type: ignore


# import personal files
#################################################################
import plasma_lifetime.p_cur_settings as settings


#############################################################################################################################################################################################
# plasma current spline processing
#############################################################################################################################################################################################

# baseline current calculator
#############################

def plasma_current_to_baseline(p_cur_processed_lp1, t):
    '''
    Function that loads in axuv timeseries
    -
    INPUTS:\n
    \t p_cur_processed_lp1 -> plasma current data that has been passed through a low pass filter
    \t t -> time array associated with the
    OUTPUTS:\n
    \t baseline_time -> time that the plasma current returns to its baseline value
    \t baseline_index -> index of the time array where the current returns to its baseline value
    '''
    # calculate how many entries to ignore at the end of the array
    end_cutoff = -1 * math.floor(len(p_cur_processed_lp1) / 10)
    
    # set up edge values array
        # max point
    maximum = max(p_cur_processed_lp1)
    max_index = list(p_cur_processed_lp1).index(maximum)
        # right side of tail
    right = np.mean(p_cur_processed_lp1[end_cutoff:])
    std_right = np.std(p_cur_processed_lp1[-10:])
    right_index = -1
        # initialize the array itself
    edges_array = [maximum, max_index, right, right_index]
    
    # get local minima of the whole array
    minima = sig.argrelmin(p_cur_processed_lp1)[0]
    
    # setup temp variables for loop
    temp_index = max_index
    temp_s = 10000
    # iterate through and get the maximum value of the slope
    for min in range(len(minima)):
        cur_s = get_S(edges_array, minima[min], p_cur_processed_lp1[minima[min]])
        if cur_s < temp_s and cur_s < 0 and p_cur_processed_lp1[minima[min]] < 0.2 * p_cur_processed_lp1[max_index] and minima[min] < (len(p_cur_processed_lp1) + end_cutoff):
            temp_index = minima[min]
            temp_s = cur_s
            
    # use this approximated value of where the current reaches its baseline value to get the actual value


    
    baseline_time = t[temp_index]
    baseline_index = temp_index
    
    return baseline_time, baseline_index

#helper for parameter S
#######################
def get_S(edges_array, index, height):
    '''
    Function that calculates the slope parameter for a given index
    -
    INPUTS:\n
    \t edges_array -> array of information required for the slope parameter
    \t index -> index where the slope parameter is being calculated
    \t height -> height of the potential 
    OUTPUTS:\n
    \t slope -> slope parameter
    '''
    slope = (height - edges_array[0]) / (index - edges_array[1])
    return slope


# helper to make data into array
################################

def make_p_cur_spline_array(data):
    '''
    Function that turns aurora formatted data into plasma current spline array data
    -
    INPUTS:\n
    \t data -> data in the aurora format
    OUTPUTS:\n
    \t p_cur_spline -> plasma current spline data in an array format
    \t t -> times associated with the p_cur_spline data
    '''
    # get current data
    p_cur_spline = data['waves'][settings.current_data_index]
    # get time data
    waves_list = plotting.collect_waves(data)[0]
    scalars = data['scalars']
    t_lims = plotting.calc_xlims(waves_list, scalars)
    t = np.linspace(t_lims[0], t_lims[1], len(data['waves'][settings.current_data_index]))
    
    return p_cur_spline, t

