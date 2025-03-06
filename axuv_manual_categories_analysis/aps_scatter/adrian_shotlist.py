import json
import pandas as pd


def separate_dome_non_dome(data_dict):
    dome_non_dome_data = {"dome":[], "non-dome":[]}
    for sustainment in data_dict.keys():
        for shot in data_dict[sustainment].keys():
            if data_dict[sustainment][shot][0] == '2':
                dome_non_dome_data['dome'].append(int(shot))
            else:
                dome_non_dome_data['non-dome'].append(int(shot))

    return dome_non_dome_data

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
        
def save_json(filename, info_dict):
    # first save the inputs array    
    with open(filename, 'w') as file:
        json.dump(info_dict, file)
        
    return 1
        
        
        
if __name__ == '__main__':
    categorization_info = load_json_file("axuv_categories_analysis/aps_scatter/thomson_classification.json")
    dome_non_dome_data = separate_dome_non_dome(categorization_info)
    save_json("axuv_categories_analysis/aps_scatter/dome_non_dome_manual.json", dome_non_dome_data)