# import libraries
#################################################################
import matplotlib.pyplot as plt
import json


# import personal files
#################################################################
import load_save_data.load_data as load_data
import thomson.load_thomson as load_thomson


# function to make it easy to generate training data
#################################################################
def make_training_data_thompson():
    # load in thomson info
    thomson_dict = load_thomson.make_thomson_dict(600, 5)
    thomson_shots = list(thomson_dict.keys())
    
    # load in sustain info
    sustain_info = load_data.load_json_file("shot_settings_info/sustainment.json")

    i=0
    for s in thomson_shots:
        s = int(s)
        current_training_data_list = make_training_data_list()
        if s not in current_training_data_list:
            # then we analyze and save the shot
            try:
                timeseries_dict = load_data.load_bson_file("preprocessed_data/axuv_timeseries_plotting/" + str(int(s/1000)*1000) + "/" + str(s) + "_ts.bson")
            except:
                i += 1
                continue
            print("GENERATING TRAINING DATA FOR SHOT", s, "//", str(100*i/len(thomson_shots))[:5] + "% complete")
            plt.figure(figsize=(16,9))
            # then open up the plot
            for k in (timeseries_dict.keys()):
                if k not in ["t", "sn024"]:
                    plt.plot(timeseries_dict["t"], timeseries_dict[k], label=k)
            
            plt.title("Photodiode Current Over Time\nShot " + str(s))
            plt.ylabel("Photodiode Current [nA]")
            plt.xlabel("Time [s]")
            plt.legend()
            plt.show()
            
            rise_class = input("\tWhat class is the RISE of the AXUV signal: ")
            fall_class = input("\tWhat class is the FALL of the AXUV signal: ")
            print()
            
            if sustain_info[str(s)] > 0:
                save_training_data(rise_class, fall_class, s, True)
            else:
                save_training_data(rise_class, fall_class, s, False)
            
        i += 1
        
    print("\n\n---------------------------------------------------------------------\n\t\t100% COMPLETE\n---------------------------------------------------------------------")
    
    return 1


# function to save the rise and fall training data
#################################################################

def save_training_data(rise_class, fall_class, shot_number, sustain):
    filename = "axuv_categories_analysis/aps_scatter/thomson_classification.json"
    current_data = load_data.load_json_file(filename)

    if sustain:
        current_data['sustain'][str(shot_number)] = [rise_class, fall_class]
    else:
        current_data['non_sustain'][str(shot_number)] = [rise_class, fall_class]

    with open(filename, 'w') as training_data:
        json.dump(current_data, training_data)
    
    return 1


def make_training_data_list():
    classifications = load_data.load_json_file("axuv_categories_analysis/aps_scatter/thomson_classification.json")
    
    data_list = []
    for sustainment in classifications.keys():
        for s in classifications[sustainment].keys():
            if int(s) not in data_list:
                data_list.append(int(s))
    
    return data_list