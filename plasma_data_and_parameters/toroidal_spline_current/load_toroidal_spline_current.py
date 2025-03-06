# import gf data tools
#################################################################
import GF_data_tools as gdt

# import libraries
#################################################################
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import os


# import personal files
#################################################################
import load_save_data.load_data as load_data
import load_save_data.save_data as save_data
import printouts.progress_bar as prog_bar


# import poloidal current data from aurora
#################################################################
def load_data_tor_spline_current_multishot(shot_list):
    i = 1
    n = len(shot_list)
    for shot in shot_list:
        if not os.path.isfile("plasma_data_and_parameters/toroidal_spline_current/toroidal_current_data/current_spline_" +str(shot)+ ".json"):
            current_data = load_data_tor_spline_current_singleshot(shot)
            save_data.save_json("plasma_data_and_parameters/toroidal_spline_current/toroidal_current_data/current_spline_" +str(shot)+ ".json", current_data)
        
        i += 1
        prog_bar.progress_bar_pct_only(i, n)
        
    return


def load_data_tor_spline_current_singleshot(shot_number):
    q_options = {   'experiment':'pi3b',
                    'manifest': 'default',
                    'shot': shot_number,
                    'layers':'mirnov_combined/plasma_current_spline',
                    'errors':'mirnov_combined/plasma_current_spline_std',
                    'nodisplay': True
                }

    try:
        data = gdt.fetch_data.run_query(q_options)
    except:
        return "no_recon_data"
    
    waves_list = gdt.plotting.collect_waves(data)[0]
    scalars = data['scalars']
    t_lims = gdt.plotting.calc_xlims(waves_list, scalars)
    t = np.linspace(t_lims[0], t_lims[1], len(data['waves'][0]))
    
    singleshot_current = {}
    singleshot_current['data'] = list(data['waves'][0])
    singleshot_current['time'] = list(t)
    singleshot_current['errors'] = list(data['errors'][0])

    return singleshot_current