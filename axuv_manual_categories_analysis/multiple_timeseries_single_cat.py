# import libraries
#################################################################
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import json
import bson


def plot_multiple_timeseries(rise_category, fall_category, sensor, normalize=False):
    # generate the list of shots that fall into the correct category
    shots_list = make_shots_list(fall_category, rise_category)
    
    multishot_data = []
    for shot in shots_list:
        filename = shot_number_to_filename(shot)
        data = load_bson_file(filename)
        multishot_data.append(data)
        
    if normalize:
        multishot_data = normalize_multiple_timeseries(multishot_data)
    
    
    # set up the plot
    lines = []
    fig, ax = plt.subplots()
    for s in range(len(multishot_data)):
        for k in multishot_data[s].keys():
            if k == sensor:
                line, = ax.plot(multishot_data[s]["t"], multishot_data[s][sensor])
                lines.append((line, s))


    cursor = mplcursors.cursor([line for line, _ in lines], hover=True)

    @cursor.connect("add")
    def on_add(sel):
        # Find the line and its index
        for line, curve_index in lines:
            if sel.artist == line:
                x, y = sel.target
                sel.annotation.set(text=f"Shot: {shots_list[curve_index]}")
                break


    plt.show()

    return
    
    

    
def make_shots_list(fall_category, rise_category):
    if fall_category != "all":
        fall_data = load_json_file("axuv_categories_analysis/axuv_fall_training_data.json")[str(fall_category)]
    if rise_category != "all":
        rise_data = load_json_file("axuv_categories_analysis/axuv_rise_training_data.json")[str(rise_category)]
        
    if rise_category == fall_category == "all":
        print("Rise and fall categories cannot both be all.")
        
    if fall_category == "all":
        shots_list = rise_data
    elif rise_category == "all":
        shots_list = fall_data
    else:
        shots_list = []
        for i in range(len(rise_data)):
            if rise_data[i] in fall_data:
                shots_list.append(rise_data[i])
    
    return shots_list






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
        

    
def load_bson_file(filename):
    """
    Loads a BSON file and returns the data as a Python object.

    Parameters:
    filename (str): The name or path of the BSON file to load.

    Returns:
    dict or list: The data parsed from the BSON file.
    """
    try:
        with open(filename, 'rb') as file:
            data = bson.decode(file.read())
        return data
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except bson.errors.InvalidBSON:
        print(f"Error: The file '{filename}' is not a valid BSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        

def shot_number_to_filename(shot_number):
    return "preprocessed_data/timeseries_plotting/" + str(int(shot_number/1000) * 1000) + "/" + str(shot_number) + "_ts.bson"



def normalize_multiple_timeseries(timeseries_data):
    for i in range(len(timeseries_data)):
        for k in timeseries_data[i].keys():
            if k != "t":
                max_val = max(timeseries_data[i][k])
                for j in range(len(timeseries_data[i][k])):
                    timeseries_data[i][k][j] = timeseries_data[i][k][j] / max_val
    
    return timeseries_data