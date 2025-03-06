# import personal files
#################################################################
import signal_processing.signal_processing as signal_processing
import plasma_lifetime.p_cur_to_baseline as p_cur_proc
import plasma_lifetime.p_cur_settings as settings

# plasma current baseline calculator
####################################

def calc_plasma_cur_baseline(plasma_current_spline_data):
    '''
    Function that calculates when plasma current returns to its baseline value
    -
    INPUTS:\n
    \t plasma_current_spline_data -> 1-D array containing the timeseries data of the plasma current spline
    OUTPUTS:\n
    \t baseline_time -> the time the current has returned to its baseline value
    \t baseline_index -> the index of baseline_time
    \t p_cur_processed_lp1 -> 1-D array of low passed plasma_current_spline_data
    \t p_cur_t -> 1-D array of the times associated with the plasma_current_spline_data
    '''
    p_cur_spline, p_cur_t = p_cur_proc.make_p_cur_spline_array(plasma_current_spline_data)
    frequency_threshold = settings.low_pass_threshold_plasma_current
    dt = p_cur_t[1] - p_cur_t[0]
    p_cur_processed_lp1 = signal_processing.low_pass(p_cur_spline, dt, frequency_threshold)
    baseline_time, baseline_index = p_cur_proc.plasma_current_to_baseline(p_cur_processed_lp1, p_cur_t)
    
    return baseline_time, baseline_index, p_cur_processed_lp1, p_cur_t



# helper to find index of p_cur_baseline_time
#############################################
def binary_search_p_cur_baseline_time(t, p_cur_baseline_time):
    '''
    Binary Search Function to actually find where the plasma current returns to baseline
    -
    INPUTS:\n
    \t t -> 1-D array of times
    \t p_cur_baseline_time -> the time when the plasma current returns to its baseline value
    OUTPUTS:\n
    \t p_cur_bl_index -> the index of the time when the plasma current returns to baseline
    '''
    prev_guess = 0
    new_guess = int(len(t) / 2)
    end_con = False
    while not end_con:
        d_index = abs(new_guess - prev_guess)
        # case where t_guess is right of the baseline
        if p_cur_baseline_time < t[new_guess]:
            prev_guess = new_guess
            new_guess = prev_guess - int(d_index/2)
            if int(d_index/2) == 0:
                new_guess = prev_guess - 1

        # case where t_guess is left of the baseline
        elif t[new_guess] < p_cur_baseline_time:
            prev_guess = new_guess
            new_guess = prev_guess + (int(d_index/2))
            if int(d_index/2) == 0:
                new_guess = prev_guess + 1
                
        if (t[new_guess] <= p_cur_baseline_time) and new_guess == (len(t) - 1):
            end_con=True
        
        elif ((t[new_guess] <= p_cur_baseline_time) and (t[new_guess + 1] > p_cur_baseline_time)):
            end_con=True
            
    p_cur_bl_index = new_guess

    return p_cur_bl_index