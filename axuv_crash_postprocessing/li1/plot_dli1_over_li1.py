# import libraries
#################################################################
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# import personal files
#################################################################
import load_save_data.load_data as load


def plot_dli1_li1_2D_density_only_crashes(crash_dir, li1_min=-1000, li1_max=1000, kde=True):
    if crash_dir[-1] != "/":
        crash_dir += "/"
        
    li1_multishot = load.load_json_file("plasma_data_and_parameters/internal_inductance/internal_inductance.json")
    crash_data_multishot = load.load_json_file(f"{crash_dir}crash_info_with_hardware_error.json")
    
    li1, dli1 = [], []
    for shot in crash_data_multishot.keys():
        if shot in li1_multishot.keys():
            if type(str()) not in [type(li1_multishot[shot]), type(crash_data_multishot[shot])]:
                for time in crash_data_multishot[shot]['times']:
                    t1, t2 = int(time*1000)/1000, (int(time*1000) + 1)/1000
                    if len(li1_multishot[shot]['data']) >= int(t2*1000):
                        l1, l2 = li1_multishot[shot]['data'][int(t1*1000)-1], li1_multishot[shot]['data'][int(t2*1000)-1]
                        if l1 < 1.5 and l2 < 1.5:
                            li1_temp = ((l2-l1)/(t2-t1) * (time-t1) + l1)
                            if li1_min < li1_temp and li1_temp < li1_max:
                                li1.append(li1_temp)
                                dli1.append(l2-l1)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    li1=np.array(li1)
    dli1=np.array(dli1)

    # KDE plot with full color extension
    if kde:
        sns.kdeplot(
            x=li1, y=dli1, 
            fill=True, 
            cmap='viridis',
            cut=5,  # Extends KDE outside data range
            clip=((li1.min()-1, li1.max()+1), (dli1.min()-1, dli1.max()+1))  # Ensures full coverage
        )
    else:
        plt.hist2d(li1, dli1, bins=20, cmap="plasma")

    # Add colorbar manually
    cbar = fig.colorbar(ax.collections[0], ax=ax)
    cbar.set_label("Density")

    plt.xlabel("li1")
    plt.ylabel(r"$\Delta$ li1")
    plt.title(r"2D Density Plot (KDE) of li1 over $\Delta$ li1"+f"\nMin: {li1_min}, Max: {li1_max}")
    plt.tight_layout()
    plt.xlim(0.4, 1.5)
    plt.ylim(-0.5, 0.5)

    plt.show()