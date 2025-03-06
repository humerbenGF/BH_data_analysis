import pandas as pd
import json
import numpy as np

import load_save_data.load_data as load_data



def convert_sustainment():
    sustainment_df = load_data.load_csv_file("shot_settings_info/sustainment.csv")
    
    sustainment_dict = {}
    
    for shot in sustainment_df["Shot ID"]:
        value = sustainment_df.loc[sustainment_df['Shot ID'] == shot, 'Sustainment Setpoint (kV)'].values[0]
        # print(value)
        if type(value) == type(""):
            if value[0] != "<":
                sustainment_dict[str(shot)] = float(value)
                continue
        # elif type(value) == type(float()):
        #     sustainment_dict[str(shot)]

            
        sustainment_dict[str(shot)] = 0
            
    with open('shot_settings_info/sustainment.json', 'w') as json_file:
        json.dump(sustainment_dict, json_file, indent=4)
    
    return


def convert_shots_since_li():
    ss_li_df = load_data.load_csv_file("machine_settings_and_state/shots_since_li/shots_since_li.csv")
    
    print(ss_li_df)
    
    ss_li_dict = {}
    
    for shot in ss_li_df["Shot ID"]:
        value = ss_li_df.loc[ss_li_df['Shot ID'] == shot, 'Shots Since Li POT Coat'].values[0]
        # print(value)
        ss_li_dict[str(shot)] = float(value)
            
    with open('machine_settings_and_state/shots_since_li/shots_since_li.json', 'w') as json_file:
        json.dump(ss_li_dict, json_file, indent=4)
    
    return


def convert_timestamps():
    timestamp_df = load_data.load_csv_file("machine_settings_and_state/time_since_last_shot/Timestamps.csv")
    
    print(timestamp_df)
    
    timestamp_dict = {}
    
    for shot in timestamp_df['Shot']:
        deltaT = timestamp_df.loc[timestamp_df['Shot'] == shot, 'Time Since Shot (s)'].values[0]
        timestamp_dict[str(shot)] = {'seconds':deltaT, 'minutes':deltaT/60}
        
    with open('machine_settings_and_state/time_since_last_shot/time_since_last_shot.json', 'w') as json_file:
        json.dump(timestamp_dict, json_file, indent=4)
        
    return


def convert_shots_since():
    ss_li_df = load_data.load_csv_file("machine_settings_and_state/shots_since_li/shots_since.csv")
    
    print(ss_li_df)
    
    ss_dict = {}
    
    for shot in ss_li_df["Shot ID"]:
        ss_li_pot = ss_li_df.loc[ss_li_df['Shot ID'] == shot, 'Shots Since Li POT Coat'].values[0]
        ss_li_gun = ss_li_df.loc[ss_li_df['Shot ID'] == shot, 'Shots Since Li GUN Coat'].values[0]
        ss_air = ss_li_df.loc[ss_li_df['Shot ID'] == shot, 'Shots Since Up To Air'].values[0]
        # print(value)
        ss_dict[str(shot)] = {'ss_li_pot':float(ss_li_pot), 'ss_li_gun':float(ss_li_gun), 'ss_air':float(ss_air)}
            
    with open('machine_settings_and_state/shots_since_li/shots_since.json', 'w') as json_file:
        json.dump(ss_dict, json_file, indent=4)
    
    return