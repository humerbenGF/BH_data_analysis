# import functions from gf data tools
#################################################################
import GF_data_tools as gdt


# import libraries
#################################################################
import numpy as np
import re
import os


# import personal files
#################################################################
import load_save_data.load_data as load
import load_save_data.save_data as save
import printouts.progress_bar as progress_bar


# load in psibar
#################################################################
def get_thomson_psibar_values_multishot(shot_list):
    # load existing thomson psibar
    if os.path.isfile('plasma_data_and_parameters/thomson/thomson_psibar.json'):
        thomson_psibar = load.load_json_file('plasma_data_and_parameters/thomson/thomson_psibar.json')
    else:
        thomson_psibar = {}
    
    # load thomson data
    thomson_600 = load.load_csv_file('plasma_data_and_parameters/thomson/thomson_temps_multitime_R600mm.csv')
    thomson_730 = load.load_csv_file('plasma_data_and_parameters/thomson/thomson_temps_multitime_R730mm.csv')
    thomson_900 = load.load_csv_file('plasma_data_and_parameters/thomson/thomson_temps_multitime_R900mm.csv')
    
    i=1
    n=len(shot_list)
    for shot in shot_list:
        if (shot in list(thomson_600['Shot #'])) and (shot in list(thomson_730['Shot #'])) and (shot in list(thomson_900['Shot #'])) and (str(shot) not in thomson_psibar.keys()):
            try:
                thomson_psibar[str(shot)] = get_thomson_pisbar_values_singleshot(shot)
            except:
                thomson_psibar[str(shot)] = 'no_recon_data'
        
        save.save_json('plasma_data_and_parameters/thomson/thomson_psibar.json', thomson_psibar)

        progress_bar.progress_bar_pct_only(i, n)
        i += 1
        
    return
    

def get_thomson_pisbar_values_singleshot(shot_number):
    q_options = {   'experiment':'pi3b',
                    'manifest': 'default',
                    'shot': shot_number,
                    'layers':'reconstruction/ThomsonR*_mean', 
                    'errors':'reconstruction/ThomsonR*_sigma',
                    'nodisplay': True}

    data = gdt.fetch_data.run_query(q_options)
    
    waves = data['waves']
    
    psibar_values = {}
    for w in range(len(waves)):
        psibar_values[waves[w].meta['wave_label'][:11]] = list(waves[w])
    
    return psibar_values