# import libraries
#################################################################
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from scipy.stats import gaussian_kde



# import personal files
#################################################################
import load_save_data.load_data as load_data


def make_KDE_time_nth_crash_sustain_non_sustain(output_dir, crash_n=1, savefig=True):
    # Check output dir
    if output_dir[-1] != "/":
        output_dir += "/"
        
    crash_info = load_data.load_json_file(output_dir + "crash_info.json")
    sustainment_dict = load_data.load_json_file("machine_settings_and_state/sustainment/sustainment.json")
    
    ci_keys = list(crash_info.keys())
    
    times_crashes_list_sustain = []
    times_crashes_list_non_sustain = []
    for k in crash_info.keys():
        if type(crash_info[k]) != type(str()) and type(sustainment_dict[k]) != type(str()):
            if sustainment_dict[k] > 0:
                if len(crash_info[k]['times']) <= 10:
                    for i in range(len(crash_info[k]['times'])):
                        if i+1 == crash_n:
                            times_crashes_list_sustain.append(crash_info[k]['times'][i])
            else:
                if len(crash_info[k]['times']) <= 10:
                    for i in range(len(crash_info[k]['times'])):
                        if i+1 == crash_n:
                            times_crashes_list_non_sustain.append(crash_info[k]['times'][i])
                            
    # Create a figure
    plt.figure(figsize=(16,9))

    # Generate KDE for both datasets
    kde_sustain = gaussian_kde(times_crashes_list_sustain, bw_method=0.3)  # Adjust bandwidth as needed
    kde_non_sustain = gaussian_kde(times_crashes_list_non_sustain, bw_method=0.3)

    # Define a range for the KDE curves
    x_values = np.linspace(
        min(min(times_crashes_list_sustain), min(times_crashes_list_non_sustain)),
        max(max(times_crashes_list_sustain), max(times_crashes_list_non_sustain)),
        500  # Number of points in the smooth curve
    )

    # Evaluate the KDE on the defined range
    y_sustain = kde_sustain(x_values)
    y_non_sustain = kde_non_sustain(x_values)

    # Plot KDE curves
    plt.plot(x_values, y_sustain, color='r', label="Sustain Shots", lw=2)
    plt.plot(x_values, y_non_sustain, color='b', label="Non-Sustain Shots", lw=2)

    # Add labels and title
    plt.xlabel('Time of Crash')
    plt.ylabel('Density')
    plt.title(f'Kernel Density Estimation of Times of Crash {crash_n} for ' +
            str(len(times_crashes_list_sustain) + len(times_crashes_list_non_sustain)) +
            ' Crashes\nIn Shot Range [' + ci_keys[0] + "," + ci_keys[-1] + ']')

    plt.grid(True)
    plt.legend()
               
               
    # Show the plot
    if savefig:
        plt.savefig(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/histograms/time_crash{crash_n}_KDE_sustain_non_sustain.png")
    else:
        plt.show()             
             
    return         


def make_hist_time_nth_crash_sustain_non_sustain(output_dir, crash_n=1, savefig=True):
    # Check output dir
    if output_dir[-1] != "/":
        output_dir += "/"
        
    crash_info = load_data.load_json_file(output_dir + "crash_info.json")
    sustainment_dict = load_data.load_json_file("machine_settings_and_state/sustainment/sustainment.json")
    
    ci_keys = list(crash_info.keys())
    
    times_crashes_list_sustain = []
    times_crashes_list_non_sustain = []
    for k in crash_info.keys():
        if type(crash_info[k]) != type(str()) and type(sustainment_dict[k]) != type(str()):
            if sustainment_dict[k] > 0:
                if len(crash_info[k]['times']) <= 10:
                    for i in range(len(crash_info[k]['times'])):
                        if i+1 == crash_n:
                            times_crashes_list_sustain.append(crash_info[k]['times'][i])
            else:
                if len(crash_info[k]['times']) <= 10:
                    for i in range(len(crash_info[k]['times'])):
                        if i+1 == crash_n:
                            times_crashes_list_non_sustain.append(crash_info[k]['times'][i])

    
    # make histogram out of data
    plt.figure(figsize=(16,9))

    # Define common bin edges
    num_bins = 20
    bin_edges = np.linspace(min(min(times_crashes_list_sustain), min(times_crashes_list_non_sustain)), max(max(times_crashes_list_sustain), max(times_crashes_list_non_sustain)), num_bins + 1)

    # Compute histogram counts
    hist_sustain, _ = np.histogram(times_crashes_list_sustain, bins=bin_edges)
    hist_non_sustain, _ = np.histogram(times_crashes_list_non_sustain, bins=bin_edges)

    # Compute bin centers
    bin_width = np.diff(bin_edges)[0]
    bin_centers = bin_edges[:-1] + bin_width / 2

    # Shift bars for side-by-side display
    shift = bin_width * 0.3  # Adjust spacing

    plt.bar(bin_centers - shift, hist_sustain, width=bin_width * 0.4, color='r', label="Sustain Shots", alpha=0.7)
    plt.bar(bin_centers + shift, hist_non_sustain, width=bin_width * 0.4, color='b', label="Non-Sustain Shots", alpha=0.7)

    
    # Add labels and title
    plt.xlabel('Time of Crash')
    plt.ylabel('Number of Crashes')
    plt.title(f'Histogram of Times of Crash {crash_n} For ' + str(len(times_crashes_list_sustain)+len(times_crashes_list_non_sustain)) + ' Crashes\nIn Shot Range [' + ci_keys[0] + "," + ci_keys[-1] + ']')
    plt.grid(True)
    plt.legend()
    
    # Show the plot
    if savefig:
        plt.savefig(f"plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/histograms/time_crash{crash_n}_hist_sustain_non_sustain.png")
    else:
        plt.show()


def make_hist_times_crashes_sustain_non_sustain(output_dir, savefig=True):
    # Check output dir
    if output_dir[-1] != "/":
        output_dir += "/"
        
    crash_info = load_data.load_json_file(output_dir + "crash_info.json")
    sustainment_dict = load_data.load_json_file("machine_settings_and_state/sustainment/sustainment.json")
    
    ci_keys = list(crash_info.keys())
    
    times_crashes_list_sustain = []
    times_crashes_list_non_sustain = []
    for k in crash_info.keys():
        if type(crash_info[k]) != type(str()) and type(sustainment_dict[k]) != type(str()):
            if sustainment_dict[k] > 0:
                if len(crash_info[k]['times']) <= 10:
                    for i in range(len(crash_info[k]['times'])):
                        times_crashes_list_sustain.append(crash_info[k]['times'][i])
            else:
                if len(crash_info[k]['times']) <= 10:
                    for i in range(len(crash_info[k]['times'])):
                        times_crashes_list_non_sustain.append(crash_info[k]['times'][i])

    
    # make histogram out of data
    plt.figure(figsize=(16,9))

    # Define common bin edges
    num_bins = 20
    bin_edges = np.linspace(min(min(times_crashes_list_sustain), min(times_crashes_list_non_sustain)), max(max(times_crashes_list_sustain), max(times_crashes_list_non_sustain)), num_bins + 1)

    # Compute histogram counts
    hist_sustain, _ = np.histogram(times_crashes_list_sustain, bins=bin_edges)
    hist_non_sustain, _ = np.histogram(times_crashes_list_non_sustain, bins=bin_edges)

    # Compute bin centers
    bin_width = np.diff(bin_edges)[0]
    bin_centers = bin_edges[:-1] + bin_width / 2

    # Shift bars for side-by-side display
    shift = bin_width * 0.3  # Adjust spacing

    plt.bar(bin_centers - shift, hist_sustain, width=bin_width * 0.4, color='r', label="Sustain Shots", alpha=0.7)
    plt.bar(bin_centers + shift, hist_non_sustain, width=bin_width * 0.4, color='b', label="Non-Sustain Shots", alpha=0.7)

    
    # Add labels and title
    plt.xlabel('Time of Crash')
    plt.ylabel('Number of Crashes')
    plt.title('Histogram of Times of Crashes For ' + str(len(times_crashes_list_sustain)+len(times_crashes_list_non_sustain)) + ' Crashes\nIn Shot Range [' + ci_keys[0] + "," + ci_keys[-1] + ']')
    plt.grid(True)
    plt.legend()
    
    # Show the plot
    if savefig:
        plt.savefig("plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/histograms/times_crashes_hist_sustain_non_sustain.png")
    else:
        plt.show()



def make_hist_num_crashes_sustain_non_sustain(output_dir, savefig=True):
    # Check output dir
    if output_dir[-1] != "/":
        output_dir += "/"
        
    crash_info = load_data.load_json_file(output_dir + "crash_info.json")
    sustainment_dict = load_data.load_json_file("machine_settings_and_state/sustainment/sustainment.json")
    
    ci_keys = list(crash_info.keys())
    
    num_crashes_list_sustain = []
    num_crashes_list_non_sustain = []
    for k in crash_info.keys():
        if type(crash_info[k]) != type(str()) and type(sustainment_dict[k]) != type(str()):
            if sustainment_dict[k] > 0:
                if len(crash_info[k]['times']) <= 10:
                    num_crashes_list_sustain.append(len(crash_info[k]['times']))
                else:
                    num_crashes_list_sustain.append(10)
            else:
                if len(crash_info[k]['times']) <= 10:
                    num_crashes_list_non_sustain.append(len(crash_info[k]['times']))
                else:
                    num_crashes_list_non_sustain.append(10)
        
    # Define the bin edges. The last bin is for values >= 10
    bins_sustain = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    bins_non_sustain = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5]

    plt.figure(figsize=(16,9))

    # Create the histogram with modified bins
    plt.hist(num_crashes_list_sustain,     bins=bins_sustain,     width=0.35, color='r', label="Sustain",     alpha=0.7, align='mid', edgecolor='k')
    plt.hist(num_crashes_list_non_sustain, bins=bins_non_sustain, width=0.35, color='b', label="Non-Sustain", alpha=0.7, align='mid', edgecolor='k')
    

    # Set custom labels for the bins, including the "10+" bin
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10+'])
    
    # Add labels and title
    plt.xlabel('Number of Crashes')
    plt.ylabel('Number of Shots')
    plt.title('Histogram of Number of Crashes For ' + str(len(num_crashes_list_sustain)+len(num_crashes_list_non_sustain)) + ' Shots\nIn Range [' + ci_keys[0] + "," + ci_keys[-1] + ']')
    plt.legend()
    
    # Show the plot
    if savefig:
        plt.savefig("plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/histograms/num_crashes_hist_sustain_non_sustain.png")
    else:
        plt.show()




def make_hist_num_crashes(output_dir, savefig=True):
    # Check output dir
    if output_dir[-1] != "/":
        output_dir += "/"
        
    crash_info = load_data.load_json_file(output_dir + "crash_info.json")
    ci_keys = list(crash_info.keys())
    
    num_crashes_list = []
    for k in crash_info.keys():
        if type(crash_info[k]) != type(str()):
            if len(crash_info[k]['times']) <= 10:
                num_crashes_list.append(len(crash_info[k]['times']))
            else:
                num_crashes_list.append(10)
        
    # Define the bin edges. The last bin is for values >= 10
    bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    plt.figure(figsize=(16,9))

    # Create the histogram with modified bins
    plt.hist(num_crashes_list, bins=bins, edgecolor='black', align='left', density=True)

    # Set custom labels for the bins, including the "10+" bin
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10+'])
    
    # Add labels and title
    plt.xlabel('Number of Crashes')
    plt.ylabel('Probability')
    plt.title('Histogram of Number of Crashes For ' + str(len(num_crashes_list)) + ' Shots\nIn Range [' + ci_keys[0] + "," + ci_keys[-1] + ']')
    
    # Show the plot
    if savefig:
        plt.savefig("plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/histograms/num_crashes_hist.png")
    else:
        plt.show()

