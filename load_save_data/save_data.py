# import libraries
#################################################################
import json

def save_json(filename, info_dict):
    # first save the inputs array    
    with open(filename, 'w') as file:
        json.dump(info_dict, file)
        
    return 1