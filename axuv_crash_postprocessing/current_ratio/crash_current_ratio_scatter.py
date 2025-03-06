# import libraries
#################################################################
import matplotlib.pyplot as plt


# import personal files
#################################################################
import load_save_data.load_data as load_data


def scatter_current_ratio_amplitude(crash_dir):
    if crash_dir[-1] != "/":
        crash_dir += "/"
    
    cur_ratios, amplitudes = load_current_ratios_and_amplitudes(crash_dir)
                
    plt.scatter(cur_ratios, amplitudes)
    plt.show()
    
    return
    
    
def hist_current_ratio(crash_dir):
    if crash_dir[-1] != "/":
        crash_dir += "/"
    
    cur_ratios, amplitudes = load_current_ratios_and_amplitudes(crash_dir)
    crash_info = load_data.load_json_file(f"{crash_dir}crash_info_with_hardware_error.json")
    first_shot, last_shot = list(crash_info.keys())[0], list(crash_info.keys())[-1]
    
    plt.figure(figsize=(16,9))
    counts, bins, patches = plt.hist(cur_ratios, bins=80, range=(0, 5))
    ymax = counts.max()
    plt.vlines([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5], ymin=0, ymax=ymax, colors='r', linestyles='dashed')
    plt.title(f"Histogram of Toroidal/Poloidal Ratios at the Time of Crashes\n{len(cur_ratios)} crashes, Shots: [{first_shot}-{last_shot}]")
    plt.xlabel("Toroidal/Poloidal Current Ratio at time of Crash")
    plt.savefig("plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/histogram_current_ratio_at_crash_times.png")
    plt.show()
    
    return


def load_current_ratios_and_amplitudes(crash_dir):
    crash_data = load_data.load_json_file(crash_dir + "crash_info_with_hardware_error.json")
    cur_data = load_data.load_json_file(crash_dir + "crash_info_with_cur_ratio.json")
    
    cur_ratios = []
    amplitudes = []
    
    for k in crash_data.keys():
        if k in cur_data.keys():
            if type(str()) not in [type(crash_data[k]), type(cur_data[k])]:
                for i in range(len(crash_data[k]['times'])):
                    cur_ratios.append(abs(cur_data[k][i]))
                    amplitudes.append(crash_data[k]["rel_amps"][i])
                    
    return cur_ratios, amplitudes