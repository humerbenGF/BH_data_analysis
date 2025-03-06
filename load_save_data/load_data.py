# import libraries
#################################################################
import json
import pandas as pd
import bson


def load_rise_data():
    filename = "axuv_categories_analysis/axuv_rise_training_data.json"
    data = load_json_file(filename)
    return data

def load_fall_data():
    filename = "axuv_categories_analysis/axuv_fall_training_data.json"
    data = load_json_file(filename)
    return data


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
        
        
def load_csv_file(file_path, encoding='ISO-8859-1'):
    """
    Loads a CSV file into a pandas DataFrame.
    
    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pandas.DataFrame: A DataFrame containing the CSV data.
    """
    try:
        df = pd.read_csv(file_path, encoding=encoding, on_bad_lines='skip')
        print(f"CSV file loaded successfully with {len(df)} rows and {len(df.columns)} columns.")
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print("test")
        print(f"An error occurred: {e}")
        

def load_bson_file(filename):
    """
    Load a BSON file and return its contents as a dictionary.

    Parameters:
    filename (str): The path to the BSON file.

    Returns:
    dict: The contents of the BSON file as a dictionary.
    """
    with open(filename, 'rb') as file:
        data = bson.decode(file.read())
    return data