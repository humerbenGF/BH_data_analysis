# import GF Data tools
#################################################################
import GF_data_tools as gdt


# import packages
#################################################################
import numpy as np 
import re
import matplotlib.pyplot as plt


# load in q profile
#################################################################
def load_J_profile(shot_number):
    q_options = {'experiment':'pi3b',
                    'manifest': 'default',
                    'shot': shot_number,
                    'layers': 'reconstruction/J*_mean', 
                    'errors':'reconstruction/J*_sigma',
                    'nodisplay': True}
        
    data = gdt.fetch_data.run_query(q_options)
    
    waves = data['waves']
    err = data['errors']
        
    # compute q from reconstruction   
    # quantity_array = list(sorted(data['waves'], key=lambda x: int(re.compile('J([0-9]*)_mean').match(x.meta['wave_label'])[1])))
    quantity_array = data['waves']
    # compute ERROR on q from reconstruction
    err_array = data['errors']
    # err_array = list(sorted(data['errors'], key=lambda x: int(re.compile('J([0-9]*)_sigma').match(x.meta['wave_label'])[1])))
    
    # reverse dimensions of the arrays
    flipped_quantity_array = []
    flipped_err_array = []
    for i in range(len(quantity_array[0])):
        flipped_quantity_array.append([])
        flipped_err_array.append([])
        for j in range(len(quantity_array)-1):
            flipped_quantity_array[i].append(float(quantity_array[j][i]))
            flipped_err_array[i].append(float(err_array[j][i]))

    # reassign the flipped arrays to the original variables 
    quantity_array = flipped_quantity_array
    err_array = flipped_err_array
    
    # make psi array
    psi = np.linspace(5,100,20) / 100
    
    # print(len(psi), len(quantity_array))
    
    plot_J = False
    if plot_J:
        for i in range(len(quantity_array)):
            plt.plot(psi, quantity_array[i])
        plt.title(r"J($\Psi$) For Different Times")
        plt.xlabel(r"$\Psi$")
        plt.ylabel("J [A/m^2]")
        plt.show()
    
    return quantity_array, err_array, psi