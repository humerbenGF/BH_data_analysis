# import packages
#################################################################
import numpy as np 
import matplotlib.pyplot as plt
import os
import pandas as pd


# import personal files
#################################################################
import crash_search.crash_search as crash_search


if __name__ == '__main__':
    # abi example shots
    example_shots = [21096, 21101]
    crash_dir = "2024-10-10_19718-23016"
    search_parameters = ["num_crashes", "max_crash_amp", "max_crash_amp_norm", "time_largest_crash", "first_crash_amp", "first_crash_amp_norm", "first_crash_time"]
    search_parameter_tolerances = [2, 10**-6, 0.1, 0.010, 10**-5, 0.3, 0.001]
    crash_search.search_based_on_example_shots(example_shots, crash_dir, search_parameters, search_parameter_tolerances)