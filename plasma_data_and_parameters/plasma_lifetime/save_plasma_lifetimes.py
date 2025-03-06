# import libraries
#################################################################
import pandas as pd
import json


# main function
#################################################################
def save_lifetimes_dict():
    lifetime_df = load_csv_file("plasma_lifetime/total_lifetime.csv")

    lifetimes_dict = {}
    for i in range(len(lifetime_df["Shot ID"])):
        if lifetime_df["Total Lifetime (us)"][i][0] == "<":
            lifetimes_dict[str(lifetime_df["Shot ID"][i])] = lifetime_df["Total Lifetime (us)"][i]
        else:
            lifetimes_dict[str(lifetime_df["Shot ID"][i])] = float(lifetime_df["Total Lifetime (us)"][i]) / 10**6

    print("Saving Plasma Lifetime Dict")
    
    filename = "plasma_lifetime/lifetimes_dict.json"
    with open(filename, 'w') as json_file:
        json.dump(lifetimes_dict, json_file, indent=4)

    return



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
        print(f"An error occurred: {e}")