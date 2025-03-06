# import libraries
import numpy as np
import random as rnd
import matplotlib.pyplot as plt

# import personal files
import signal_processing.fast_fourier as fft

# fft signal processing file
#################################################################

def frequency_exclusion(data, dt, n_freq=5):
    '''
    Frequency Domain Exclusion function
    -
    INPUTS:\n
    data -> initial 1-D array of values that are in the time domain\n
    dt -> time between the entries of data\n
    n_freq -> (set to 5 by default) the number of frequencies to include in the processed version of the data\n
    OUTPUTS:\n
    y -> the new function values in the time domain
    '''
    # get fft of data array
    yf, xf = fft.rfft(data, dt)
    # sort and then reverse the indices list to get a highest to lowest amplitude version
    y_indices = np.argsort(yf)
    y_indices_sorted = np.flip(y_indices)
    y_indices_safe = y_indices_sorted[:n_freq]
    # filter out all the undesired frequencies
    for i in range(len(yf)):
        if i not in y_indices_safe:
            yf[i] = 0
    # invert the fourier transform
    y = fft.irfft(yf, len(data))
    
    return y


# low pass / high pass filters
#################################################################

# low pass
def low_pass(data, dt, f_threshold, plot_freq_domain=False):
    '''
    Low pass filter function
    -
    INPUTS:\n
    data -> initial 1-D array of values that are in the time domain\n
    dt -> time between the entries of data\n
    OUTPUTS:\n
    y -> the new function values in the time domain
    '''
    # get fft of data array
    yf, xf = fft.rfft(data, dt, plot_freq_domain=plot_freq_domain)
    # filter out all the undesired frequencies
    for i in range(len(yf)):
        if xf[i] > f_threshold:
            yf[i] = 0
    # invert the fourier transform
    y = fft.irfft(yf, len(data))
    
    return y


# high pass
def high_pass(data, dt, f_threshold):
    '''
    High pass filter function
    -
    INPUTS:\n
    data -> initial 1-D array of values that are in the time domain\n
    dt -> time between the entries of data\n
    OUTPUTS:\n
    y -> the new function values in the time domain
    '''
    # get fft of data array
    yf, xf = fft.rfft(data, dt)
    # filter out all the undesired frequencies
    for i in range(len(yf)):
        if xf[i] < f_threshold:
            yf[i] = 0
    # invert the fourier transform
    y = fft.irfft(yf, len(data))
    
    return y    