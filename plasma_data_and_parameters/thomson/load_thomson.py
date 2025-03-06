import pandas as pd
import numpy as np


def make_thomson_dict(position, time):
    position = str(position)
    
    df_thomson = load_csv_file("thomson/thomson_temps_multitime_R" + position + "mm.csv")
    
    thomson_dict = {}
    for shot in df_thomson['Shot #']:
        for i in range(4):
            thomson_temp = get_thomson_data_from_df(df_thomson, shot, "T" + str(i) + " (eV)")
            thomson_time = get_thomson_data_from_df(df_thomson, shot, "t" + str(i) + " (ms)")
            if thomson_temp != 0 and int(thomson_time) == time and not np.isnan(thomson_temp):
                thomson_dict[str(int(shot))] = thomson_temp
    
    
    return thomson_dict


def get_thomson_data_from_df(df_thomson, shot, column_of_interest):
    try:
        # Filter the dataframe for the specified shot number
        row = df_thomson[df_thomson['Shot #'] == shot]
        
        # Check if row is found
        if not row.empty:
            # Return the value from the specified column
            return row[column_of_interest].values[0]
        else:
            print(f"Shot number {shot} not found in dataframe.")
            return 0
    except KeyError:
        print(f"Column '{column_of_interest}' not found in the dataframe.")
        return 0



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