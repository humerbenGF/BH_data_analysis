# import libraries
#################################################################
import matplotlib.pyplot as plt
import bson


# import personal files
#################################################################

def plot_axuv_timeseries(shotno):
    filename = 'preprocessed_data/axuv_timeseries_plotting/' + str(int(shotno/1000)*1000) + "/" + str(shotno) + "_ts.bson"
    
    data_dict = load_bson(filename)   
    
    for k in data_dict:
        if k not in ["sn024", "t"]:
            plt.plot(data_dict["t"], data_dict[k])
            
    plt.title("Shot " + str(shotno))
    plt.show()
    
    return


def load_bson(filename):
    """
    Loads a BSON file and returns the data as a dictionary.
    
    Parameters:
        filename (str): The path to the BSON file.
    
    Returns:
        dict: The data from the BSON file.
    """
    with open(filename, 'rb') as file:
        data = bson.decode(file.read())
    return data