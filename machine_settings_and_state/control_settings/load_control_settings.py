"""
Created on Wed Oct  2 09:40:02 2024

@author: andrea.tancetti
"""

# set AURORA_REPOS variable
#################################################################
import os
import sys
sys.path.append(os.environ['AURORA_REPOS'])

# import aurora repos
#################################################################
import GF_data_tools as gdt     # type: ignore

# import python libraries
#################################################################
import numpy as np
import pandas as pd

# import personal files
#################################################################
import load_save_data.save_data as save_data
import printouts.progress_bar as pb


###############################################################################

def load_control_settings_json(shot_list):
    manifest = 'default'  
    shotlist  = np.sort(shot_list).astype(int)

    ### CREATE ARRAYS TO SAVE DATA ################################################

    # GAS SETTINGS
    gas_type = []#np.zeros(len(shotlist))
    puff_valve_open = np.zeros(len(shotlist))
    puff_width = np.zeros(len(shotlist))
    # CAP BANKS SET POINTS 
    peak_setpoint = np.zeros(len(shotlist))
    pre_form_setpoint = np.zeros(len(shotlist))
    form_setpoint = np.zeros(len(shotlist))
    sust_setpoint = np.zeros(len(shotlist))
    peak_fire = np.zeros(len(shotlist))
    pre_form_fire = np.zeros(len(shotlist))
    # COIL CURRENTS
    A = np.zeros(len(shotlist))
    B = np.zeros(len(shotlist))
    C = np.zeros(len(shotlist))
    D = np.zeros(len(shotlist))
    PFC_1 = np.zeros(len(shotlist))
    PFC_2 = np.zeros(len(shotlist))


    # load and save data
    cur = 1
    tot = len(shot_list)
    for i, shot in enumerate(shotlist):

        try:
            shotlog = gdt.fetch_data.get_shot_config('pi3b', manifest, shot, 'shotlog') # load data from shotlog
            scalars = gdt.fetch_data.get_shot_scalars('pi3b', manifest, shot) # load scalars
            
            peak_setpoint[i] = shotlog['power_supplys']['5']['voltage']/1e3
            pre_form_setpoint[i] = shotlog['power_supplys']['11']['voltage']/1e3
            form_setpoint[i] = shotlog['power_supplys']['1']['voltage']/1e3
            sust_setpoint[i] = shotlog['power_supplys']['3']['voltage']/1e3
            peak_fire[i] = scalars['Pretor_trigger_timing']
            pre_form_fire[i] = scalars['Formation_trigger_timing']


            puff_valve_open[i] = pre_form_fire[i] - shotlog['puff']['form_delay']['delay']
            puff_width[i] = scalars['Puff_width']
                
            A[i] = np.round(scalars['B'][ 'coil_current_at_form']['value'],3)
            # B[i] = np.round(scalars['A'][ 'coil_current_at_form']['value'],3)
            C[i] = np.round(scalars['C'][ 'coil_current_at_form']['value'],3)
            D[i] = np.round(scalars['D'][ 'coil_current_at_form']['value'],3)
            PFC_1[i] = np.round(scalars['E'][ 'coil_current_at_form']['value'],3)
            PFC_2[i] = np.round(scalars['F'][ 'coil_current_at_form']['value'],3)
            
            gas_type.append(shotlog['manifolds']['items'][0]['gas'])
            
            pb.progress_bar_pct_only(cur, tot)
            cur += 1
            
        
        except:
            
            #raise Exception('No data for shot ' + print(shot))
            gas_type.append(np.nan)
            continue
        

        

    #### SAVE DATA IN DICTIONARY FOR CSV ###################################################

    final_dt = {'shot #': shotlist,
                'gas' : gas_type,
                'puff_valve_open': puff_valve_open,
                'puff_width': puff_width,
                'peak_fire_time': peak_fire,
                'pre_form_fire_time': pre_form_fire,
                'peak_kV': peak_setpoint,
                'preform_kV': pre_form_setpoint,
                'form_kV': form_setpoint,
                'sust_kV': sust_setpoint,
                'A':A,
                # 'B':B,
                'C':C,
                'D':D,
                'PFC1':PFC_1,
                'PFC2':PFC_2}
    
    (pd.DataFrame(final_dt)).to_csv("machine_settings_and_state/control_settings/control_settings.csv", index=False)
    
    print(pd.DataFrame(final_dt))
    
    #### SAVE DATA IN DICTIONARY FOR JSON ###################################################
    
    data_dict = {}
    
    for i in range(len(final_dt['shot #'])):
        data_dict[str(final_dt['shot #'][i])] = {
                'gas' : final_dt['gas'][i],
                'puff_valve_open': final_dt['puff_valve_open'][i],
                'puff_width': final_dt['puff_width'][i],
                'peak_fire_time': final_dt['peak_fire_time'][i],
                'pre_form_fire_time': final_dt['pre_form_fire_time'][i],
                'peak_kV': final_dt['peak_kV'][i],
                'preform_kV': final_dt['preform_kV'][i],
                'form_kV': final_dt['form_kV'][i],
                'sust_kV': final_dt['sust_kV'][i],
                'A':final_dt['A'][i],
                # 'B':final_dt['B'][i],
                'C':final_dt['C'][i],
                'D':final_dt['D'][i],
                'PFC1':final_dt['PFC1'][i],
                'PFC2':final_dt['PFC2'][i]
            }
        
        
        
    save_data.save_json("machine_settings_and_state/control_settings/control_settings.json", data_dict)

    return 1