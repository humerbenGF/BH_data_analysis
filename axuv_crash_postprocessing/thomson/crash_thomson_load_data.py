# import libraries
#################################################################
import numpy as np
import os

# import personal files
#################################################################
import load_save_data.load_data as load_data
import load_save_data.save_data as save_data
from axuv_crash_postprocessing.thomson.crash_thomson_scatter_helpers import convert_times_to_phases
import printouts.progress_bar as pb



def load_thomson_phase_data_plottable(data_dir, crash_data, thomson_data, psibar_data):
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
    
    # load in crash info
    if crash_data:
        crash_info = load_data.load_json_file(data_dir + "crash_info_with_hardware_error.json")
    
    # load in thomson data
    if thomson_data:
        thomson_data_600 = load_data.load_csv_file("plasma_data_and_parameters/thomson/thomson_temps_multitime_R600mm.csv")
        thomson_data_600.set_index('Shot #', inplace=True)
        thomson_data_730 = load_data.load_csv_file("plasma_data_and_parameters/thomson/thomson_temps_multitime_R730mm.csv")
        thomson_data_730.set_index('Shot #', inplace=True)
        thomson_data_900 = load_data.load_csv_file("plasma_data_and_parameters/thomson/thomson_temps_multitime_R900mm.csv")
        thomson_data_900.set_index('Shot #', inplace=True)
        
    # load in the thomson psibar values
    if psibar_data:
        thomson_psibar = load_data.load_json_file("plasma_data_and_parameters/thomson/thomson_psibar.json")
        

    shot_list_flt = []
    shot_list_int = []
    for shot in crash_info.keys():
        check_all_data = True
        if crash_data:
            if type(crash_info[shot]) == type(str()):
                check_all_data = False
        if thomson_data:
            if (float(shot) not in thomson_data_600.index.to_numpy()) or (float(shot) not in thomson_data_730.index.to_numpy()) or (float(shot) not in thomson_data_900.index.to_numpy()):
                check_all_data = False
        if psibar_data:
            if shot in thomson_psibar.keys():
                if type(thomson_psibar[shot]) == type(str()):
                    check_all_data = False
                # elif len(thomson_psibar[shot]['ThomsonR899']) < 10:
                #     check_all_data = False
            else:
                check_all_data = False


                
        if check_all_data:
            shot_list_flt.append(float(shot))
            shot_list_int.append(int(shot))
    
    
    
    
    # append data dict with your loaded data
    data_dict = {}
    if crash_data:
        data_dict["crash_info"] = crash_info
    if thomson_data:
        data_dict["thomson_600"] = thomson_data_600
        data_dict["thomson_730"] = thomson_data_730
        data_dict["thomson_900"] = thomson_data_900
    if psibar_data:
        data_dict["thomson_psibar"] = thomson_psibar
        
    data_dict["shot_list_flt"] = shot_list_flt
    data_dict["shot_list_int"] = shot_list_int
    
    return data_dict


def load_thomson_phase_data_by_shot(data_dir, crash_data=False, thomson_data=False, psibar_data=False, thomson_phase=False, reprocess=False):
    if not reprocess:
        filename="plasma_data_and_parameters/thomson/thomson_data_by_shot.json"
        if os.path.isfile(filename):
            return load_data.load_json_file(filename)
            
        
    
    # check data dir formatting
    if data_dir[-1] != "/":
        data_dir += "/"
        
    # thomson
    data_dict_plottable = load_thomson_phase_data_plottable(data_dir, crash_data, thomson_data, psibar_data)
    shot_list_int = data_dict_plottable['shot_list_int']
    
    print("\nLOADING SHOT BY SHOT DATA")
    
    i = 1
    n=len(shot_list_int)
    # set up dict by shot
    data_dict_by_shot = {}
    for s in shot_list_int:
        data_dict_by_shot[str(s)] = {}
        if crash_data:
            data_dict_by_shot[str(s)]["crash_info"] = data_dict_plottable["crash_info"][str(s)]
        if thomson_data:
            data_dict_by_shot[str(s)]["thomson_600_times"], data_dict_by_shot[str(s)]["thomson_600_temps"] = save_thomson_singleshot_singlesensor('600', data_dict_plottable, s)
            data_dict_by_shot[str(s)]["thomson_730_times"], data_dict_by_shot[str(s)]["thomson_730_temps"] = save_thomson_singleshot_singlesensor('730', data_dict_plottable, s)
            data_dict_by_shot[str(s)]["thomson_900_times"], data_dict_by_shot[str(s)]["thomson_900_temps"] = save_thomson_singleshot_singlesensor('900', data_dict_plottable, s)
        if psibar_data:
            data_dict_by_shot[str(s)]["thomson_600_psibars"] = data_dict_plottable["thomson_psibar"][str(s)]["ThomsonR600"]
            data_dict_by_shot[str(s)]["thomson_730_psibars"] = data_dict_plottable["thomson_psibar"][str(s)]["ThomsonR747"]
            data_dict_by_shot[str(s)]["thomson_900_psibars"] = data_dict_plottable["thomson_psibar"][str(s)]["ThomsonR899"]
        if thomson_phase:
            data_dict_by_shot[str(s)]["thomson_600_phases"] = convert_times_to_phases(s, data_dir, data_dict_by_shot[str(s)]["thomson_600_times"])
            data_dict_by_shot[str(s)]["thomson_730_phases"] = convert_times_to_phases(s, data_dir, data_dict_by_shot[str(s)]["thomson_730_times"])
            data_dict_by_shot[str(s)]["thomson_900_phases"] = convert_times_to_phases(s, data_dir, data_dict_by_shot[str(s)]["thomson_900_times"])
    
        pb.progress_bar_pct_only(i, n)
        i += 1
        
    save_data.save_json("plasma_data_and_parameters/thomson/thomson_data_by_shot.json", data_dict_by_shot)
    
        
    return data_dict_by_shot

            
            
            
            
def save_thomson_singleshot_singlesensor(thomson_location, data_dict_plottable, shot):
    thomson_data = data_dict_plottable[f"thomson_{thomson_location}"].loc[float(shot)]
    
    times = []
    temps = []
    
    i = 0
    while f"T{i} (eV)" in thomson_data.keys():
        if thomson_data[f"t{i} (ms)"] < 30 and not np.isnan(thomson_data[f"T{i} (eV)"]):
            times.append(thomson_data[f"t{i} (ms)"] / 1000)
            temps.append(thomson_data[f"T{i} (eV)"])
        i += 1
        
    return times, temps