# import libraries
#################################################################
import numpy as np
import json
import time
import math

# import personal files
#################################################################
import plasma_lifetime.p_cur_calculations as p_cur_calc
import plasma_lifetime.read_aurora as read_aurora



def save_plasma_lifetimes_dict(shots_list):
    lifetimes_dict = make_plasma_lifetimes_dict(shots_list)
    filename = "plasma_lifetime/lifetimes_dict.json"
    
    print("Saving Plasma Lifetime Dict")
    
    with open(filename, 'w') as json_file:
        json.dump(lifetimes_dict, json_file, indent=4)
        
    return 1
    

def make_plasma_lifetimes_dict(shots_list):
    starting_time = time.time()
    try:
        lifetimes_dict = load_json_file("plasma_lifetime/lifetimes_dict.json")
    except:
        lifetimes_dict = {}
    i = 1
    length = len(shots_list)
    for shot in shots_list:
        if str(shot) not in lifetimes_dict.keys():
            print("Calculating Plasma Lifetime for Shot:", shot, "\n------------------------------------------------------------------------")
            try:
                plasma_current_spline_data = read_aurora.read_p_c_spline(shot)
                baseline_time, baseline_index, p_cur_processed_lp1, p_cur_t = p_cur_calc.calc_plasma_cur_baseline(plasma_current_spline_data)
                lifetimes_dict[str(shot)] = baseline_time
                cur_time = time.time()
                elapsed_time = cur_time - starting_time
                print("\t" + str(100*i/length)[:5] + "% complete //", math.ceil((elapsed_time / (i/length) - elapsed_time)/60), "minutes remaining\n")
            except:
                print("\tNo p_cur_spline data available.\n")
                lifetimes_dict[str(shot)] = "no data"
                
        i += 1
        
    print("Plasma Lifetime Calculations Complete\n")

    return lifetimes_dict



def load_json_file(filename):
    """
    Loads a JSON file and returns the data as a Python object.

    Parameters:
    filename (str): The name or path of the JSON file to load.

    Returns:
    dict or list: The data parsed from the JSON file.
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")