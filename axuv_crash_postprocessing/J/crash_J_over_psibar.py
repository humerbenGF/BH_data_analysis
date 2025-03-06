# import libraries
#################################################################
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap


# import personal files
#################################################################
import load_save_data.load_data as load_data
import plasma_data_and_parameters.J_profile.load_J_profile as load_J


def plot_J_over_psibar_all_crashes(crash_dir, shot_number):
    # check crash directory string
    if crash_dir[-1] != "/":
        crash_dir += "/"
    
    # load data
    crash_info_singleshot = load_data.load_json_file(f"{crash_dir}crash_info_with_hardware_error.json")[str(shot_number)]
    J_data, J_err, psi = load_J.load_J_profile(shot_number)
    lifetime_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
    # filter out which curves are to be used for plotting
    crash_ind = 0
    J_curves = []
    J_curve_labels = []
    for i in range(len(J_data)-1):
        if (i+1) / 1000 < crash_info_singleshot['times'][crash_ind] and crash_info_singleshot['times'][crash_ind] < (i+2) / 1000:
            # append values to arrays
            J_curves.append(J_data[i])
            J_curves.append(J_data[i+1])
            J_curve_labels.append(r"J(Psibar) at t="+f"{i+1}ms // BEFORE a crash at t=" + str(crash_info_singleshot['times'][crash_ind]*1000)[:4]+"ms")
            J_curve_labels.append(r"J(Psibar) at t="+f"{i+2}ms // AFTER a crash at t=" + str(crash_info_singleshot['times'][crash_ind]*1000)[:4]+"ms")
            
            # increment which crash is being considered
            while crash_info_singleshot['times'][crash_ind] < (i+2) / 1000:
                crash_ind += 1
                if len(crash_info_singleshot['times']) == crash_ind:
                    break
                    
            if len(crash_info_singleshot['times']) == crash_ind:
                break


    # setup everything for plotting
        # calculate how many J values are separated by a crash
    num_crashes_avail = int(len(J_curves)/2)
        # Choose a colormap
    colormap = get_cmap("jet")  # You can replace 'viridis' with any Matplotlib colormap
        # Linearly spaced values between 0 and 1 for the colormap
    if num_crashes_avail > 1:
        colors = [colormap(i / (num_crashes_avail - 1)) for i in range(num_crashes_avail)]
    else:
        colors = [colormap(0)]
    
    for i in range(num_crashes_avail):        
        plt.plot(psi, J_curves[2*i], color=colors[i], label=J_curve_labels[2*i], marker='o', linestyle='-', alpha=0.5)
        plt.plot(psi, J_curves[2*i+1], color=colors[i], label=J_curve_labels[2*i+1], marker='x', linestyle='--')
    
    plt.title(r"J($\Psi$) Spanning Crashes " + f"for Shot {shot_number}\nShot Lifetime: {str(lifetime_dict[str(shot_number)]*1000)[:4]}ms")
    plt.xlabel(r"$\Psi$")
    plt.ylabel("J [A/m^2]")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()