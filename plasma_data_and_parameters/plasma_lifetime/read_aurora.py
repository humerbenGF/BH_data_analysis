# set AURORA_REPOS variable
#################################################################
import os
import sys
sys.path.append(os.environ['AURORA_REPOS'])


# import general fusion files
#################################################################
from GF_data_tools import fetch_data        # type: ignore

# read in plasma current spline data
#################################################################

def read_p_c_spline(shot_number):
    '''
    Function that reads in plasma current spline data for a single PI3 shot
    -
    INPUTS:\n
    \t shot_number -> the shot that you would like the data of\n
    OUTPUTS:\n
    \t current_spline_data -> data in the standard aurora format
    '''
    plasma_current_spline_options = {'experiment': 'pi3b',
        'manifest': 'default',
        'shot': shot_number,
        'layers': 'mirnov_combined/*',
        'nodisplay': True}
    
    current_spline_data = fetch_data.run_query(plasma_current_spline_options)
    
    return current_spline_data