# import libraries
import scipy.fft as fft
import matplotlib.pyplot as plt
import numpy as np



def rfft(y, dt, plot_freq_domain=False):
    '''
    Real FFT Function
    -
    INPUTS:\n
    \t y -> initial 1-D array of values that are in the time domain\n
    \t dt -> time between the entries of y\n
    OUTPUTS:\n
    \t yf -> amplitudes of different frequencies of fourier transform\n
    \t xf -> frequencies represented by the fourier transform\n
    '''
    y = np.array(y)
    yf = fft.rfft(y)
    yf = np.array(yf)
    xf = fft.rfftfreq(len(y), dt)
    
    if plot_freq_domain:
        plt.plot(xf, abs(yf))
        plt.show()
        
    return yf, xf


def irfft(y_fourier, N):
    '''
    Inverse Real FFT Function
    -
    INPUTS:\n
    \t y_fourier -> initial 1-D array of values representing the amplitudes of modes in the frequency domain\n
    \t N -> number of points originally represented by the function in the time domain (ex. x = irfft( rfft(x), len(x))
    OUTPUTS:\n
    \t yf -> the new function values in the time domain
    '''
    y = fft.irfft(y_fourier, n=N)
    return y