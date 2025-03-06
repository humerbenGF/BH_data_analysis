# import gf data tools
#################################################################
import GF_data_tools as gdt

# import libraries
#################################################################
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import os


# import personal files
#################################################################
import load_save_data.load_data as load_data
import load_save_data.save_data as save_data
import printouts.progress_bar as prog_bar


# import poloidal current data from aurora
#################################################################
def load_data_pol_current_multishot(shot_list):
    if os.path.isfile("plasma_data_and_parameters/poloidal_current/poloidal_current.json"):
        multishot_current = load_data.load_json_file("plasma_data_and_parameters/poloidal_current/poloidal_current.json")
    else:
        multishot_current = {}
        
    i = 1
    n = len(shot_list)
    for shot in shot_list:
        if str(shot) not in multishot_current.keys():
            multishot_current[str(shot)] = load_data_pol_current_singleshot(shot)
        
        save_data.save_json("plasma_data_and_parameters/poloidal_current/poloidal_current.json", multishot_current)
        
        i += 1
        prog_bar.progress_bar_pct_only(i, n)
            
    return


def load_data_pol_current_singleshot(shot_number):
    q_options = {   'experiment':'pi3b',
                    'manifest': 'default',
                    'shot': shot_number,
                    'layers':'reconstruction/Ipol_mean',
                    'errors':'reconstruction/Ipol_sigma',
                    'nodisplay': True}

    try:
        data = gdt.fetch_data.run_query(q_options)
    except:
        return "no_recon_data"
    
    singleshot_current = {}
    singleshot_current['data']  = list(data['waves'][0])
    singleshot_current['errors'] = list(data['errors'][0])

    return singleshot_current