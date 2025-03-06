# import libraries
#################################################################
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap


# import personal files
#################################################################
import load_save_data.load_data as load_data
import plasma_data_and_parameters.q_profile.load_q_profile as load_q


def plot_q_over_psibar_all_crashes(crash_dir, shot_number):
    # check crash directory string
    if crash_dir[-1] != "/":
        crash_dir += "/"
    
    # load data
    crash_info_singleshot = load_data.load_json_file(f"{crash_dir}crash_info_with_hardware_error.json")[str(shot_number)]
    q_data, q_err, psi = load_q.load_q_profile(shot_number)
    lifetime_dict = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")

    # filter out which curves are to be used for plotting
    crash_ind = 0
    q_curves = []
    q_curve_labels = []
    for i in range(len(q_data)-1):
        if (i+1) / 1000 < crash_info_singleshot['times'][crash_ind] and crash_info_singleshot['times'][crash_ind] < (i+2) / 1000:
            # append values to arrays
            q_curves.append(q_data[i])
            q_curves.append(q_data[i+1])
            q_curve_labels.append(r"q(Psibar) at t="+f"{i+1}ms // BEFORE a crash at t=" + str(crash_info_singleshot['times'][crash_ind]*1000)[:4]+"ms")
            q_curve_labels.append(r"q(Psibar) at t="+f"{i+2}ms // AFTER a crash at t=" + str(crash_info_singleshot['times'][crash_ind]*1000)[:4]+"ms")
            
            # increment which crash is being considered
            while crash_info_singleshot['times'][crash_ind] < (i+2) / 1000:
                crash_ind += 1
                if len(crash_info_singleshot['times']) == crash_ind:
                    break
                    
            if len(crash_info_singleshot['times']) == crash_ind:
                break


    # setup everything for plotting
        # calculate how many q values are separated by a crash
    num_crashes_avail = int(len(q_curves)/2)
        # Choose a colormap
    colormap = get_cmap("jet")  # You can replace 'viridis' with any Matplotlib colormap
        # Linearly spaced values between 0 and 1 for the colormap
    colors = [colormap(i / (num_crashes_avail - 1)) for i in range(num_crashes_avail)]

    
    for i in range(num_crashes_avail):        
        plt.plot(psi, q_curves[2*i], color=colors[i], label=q_curve_labels[2*i], marker='o', linestyle='-', alpha=0.5)
        plt.plot(psi, q_curves[2*i+1], color=colors[i], label=q_curve_labels[2*i+1], marker='x', linestyle='--')
    
    plt.title(r"q($\Psi$) Spanning Crashes " + f"for Shot {shot_number}\nShot Lifetime: {str(lifetime_dict[str(shot_number)]*1000)[:4]}ms")
    plt.xlabel(r"$\Psi$")
    plt.ylabel("q")
    plt.grid(True)
    plt.legend()
    plt.show()