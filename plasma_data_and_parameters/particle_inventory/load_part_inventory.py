# import GF Data tools
#################################################################
import GF_data_tools as gdt

# import packages
#################################################################
import numpy as np 
import re
import matplotlib.pyplot as plt
import os

# import personal files
#################################################################
import load_save_data.load_data as load_data
import load_save_data.save_data as save_data
import printouts.progress_bar as prog_bar


# import particle inventory data from aurora
#################################################################
def load_particle_inventory_multishot(shot_list):
    if os.path.isfile("plasma_data_and_parameters/particle_inventory/particle_inventory.json"):
        multishot_pi = load_data.load_json_file("plasma_data_and_parameters/particle_inventory/particle_inventory.json")
    else:
        multishot_pi = {}
        
    i = 1
    n = len(shot_list)
    for shot in shot_list:
        if str(shot) not in multishot_pi.keys():
            multishot_pi[str(shot)] = load_particle_inventory_singleshot(shot)
        
        save_data.save_json("plasma_data_and_parameters/particle_inventory/particle_inventory.json", multishot_pi)
        
        i += 1
        prog_bar.progress_bar_pct_only(i, n)
            
    return


def load_particle_inventory_singleshot(shot_number):
    q_options = {'experiment':'pi3b',
                    'manifest': 'default',
                    'shot': shot_number,
                    'layers':'reconstruction/ParticleInventory_mean', 
                    'errors':'reconstruction/ParticleInventory_sigma',
                    'nodisplay': True}

    try:
        data = gdt.fetch_data.run_query(q_options)
    except:
        return "no_recon_data"
    
    singleshot_pi = {}
    singleshot_pi['data']  = list(data['waves'][0])
    singleshot_pi['errors'] = list(data['errors'][0])

    return singleshot_pi