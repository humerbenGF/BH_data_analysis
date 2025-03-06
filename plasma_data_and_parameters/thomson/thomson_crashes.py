# import libraries
#################################################################
import matplotlib.pyplot as plt
import numpy as np


# import personal files
#################################################################
import load_save.load_data as load_data
import load_save.load_postproc_results as load_postproc
import read_rawdata.read_csv as read_csv
import post_proc_axuv_crash.scatter_cursors as scatter_cursors


# calculate coincident crashes with AXUV signals
#################################################################
def calculate_coincident_crashes_thomson(output_dir, shot_list=[], normalize_time=True):
    # reformat output directory
    if output_dir[-1] != "/":
        output_dir += "/"
    # check if shot list is provided
    if shot_list == []:
        shot_list = load_data.load_shots_list(output_dir)
    
    # load in all crash info
    crash_info_multishot = load_postproc.load_combined_crash_info_multishot(shot_list, output_dir, False)
    crash_info_multishot_keys = list(crash_info_multishot.keys())
    
    # load in thomson data
    thomson_600 = read_csv.read_csv("thomson/thomson_temps_multitime_R600mm.csv")
    thomson_730 = read_csv.read_csv("thomson/thomson_temps_multitime_R730mm.csv")
    thomson_900 = read_csv.read_csv("thomson/thomson_temps_multitime_R900mm.csv")
    
    coincident_crashes_dictionary = {}

    for shot in thomson_600["Shot #"]:
        # set up shot info
        shot_index = thomson_600.index[thomson_600["Shot #"] == shot].tolist()[0]
        shot_int = int(shot)
        
        # coincident crashes dictionary set up
        coincident_crashes_dictionary[str(shot_int)] = {"thomson_600":[], "thomson_730":[], "thomson_900":[]}
        
        if (str(shot_int) in crash_info_multishot_keys):        #  and (shot in thomson_600["Shot #"])
            crash_times = crash_info_multishot[str(shot_int)]['times_list']
            
            thomson_times_list = []
            times_only_list = []
            for i in range(4):
                time = thomson_600["t" + str(i) + " (ms)"][shot_index]
                if (time not in times_only_list):
                    thomson_times_list.append([time/1000, i])
                    times_only_list.append(time/1000)
            
            if len(thomson_times_list) > 1:
                for j in range(len(thomson_times_list) - 1):
                    for i in range(len(crash_times)):
                        if (crash_times[i] < thomson_times_list[j+1][0]) and (crash_times[i] > thomson_times_list[j][0]):
                            # now know that there will be at least one viable datapoint
                            if i < (len(crash_times) - 1):
                                if (crash_times[i+1] < thomson_times_list[j+1][0]) and (crash_times[i+1] > thomson_times_list[j][0]):
                                    continue

                            dt_crash = thomson_times_list[j+1][0] - crash_times[i]
                            if i == (len(crash_times) - 1):
                                dt_crash_phase = 2*np.pi*(thomson_times_list[j+1][0] - crash_times[i]) / crash_times[i]
                            else:
                                dt_crash_phase = 2*np.pi*(thomson_times_list[j+1][0] - crash_times[i]) / (crash_times[i+1] - crash_times[i])
                            dT_temp_600 = thomson_600["T" + str(thomson_times_list[j+1][1]) + " (eV)"][shot_index]# - thomson_600["T" + str(thomson_times_list[j][1]) + " (eV)"][shot_index]
                            dT_temp_730 = thomson_730["T" + str(thomson_times_list[j+1][1]) + " (eV)"][shot_index]# - thomson_730["T" + str(thomson_times_list[j][1]) + " (eV)"][shot_index]
                            dT_temp_900 = thomson_900["T" + str(thomson_times_list[j+1][1]) + " (eV)"][shot_index]# - thomson_900["T" + str(thomson_times_list[j][1]) + " (eV)"][shot_index]
                            
                            if normalize_time:
                                coincident_crashes_dictionary[str(shot_int)]["thomson_600"].append([dT_temp_600, dt_crash_phase])
                                coincident_crashes_dictionary[str(shot_int)]["thomson_730"].append([dT_temp_730, dt_crash_phase])
                                coincident_crashes_dictionary[str(shot_int)]["thomson_900"].append([dT_temp_900, dt_crash_phase])
                            
                            
                            elif not normalize_time:
                                coincident_crashes_dictionary[str(shot_int)]["thomson_600"].append([dT_temp_600, dt_crash])
                                coincident_crashes_dictionary[str(shot_int)]["thomson_730"].append([dT_temp_730, dt_crash])
                                coincident_crashes_dictionary[str(shot_int)]["thomson_900"].append([dT_temp_900, dt_crash])


    return coincident_crashes_dictionary


# use coincident crashes to create the scatter plot
#################################################################
def coincident_crashes_thomson_scatter_plot(output_dir, shot_list=[], normalize_time=True, plot_individual_scatter=False, plot_ratio=False):
    coincident_crashes_thomson_dict = calculate_coincident_crashes_thomson(output_dir, shot_list, normalize_time=normalize_time)
    
    # set up arrays
    thomson_600_temp = []
    thomson_600_time = []
    thomson_730_temp = []
    thomson_730_time = []
    thomson_900_temp = []
    thomson_900_time = []
    
    thomson_all_temp = []
    thomson_all_time = []
    
    true_shot_list = []
    
    coincident_crashes_shotlist = list(coincident_crashes_thomson_dict.keys())
    for k in coincident_crashes_thomson_dict.keys():
        # thomson at 600mm
        for i in range(len(coincident_crashes_thomson_dict[k]['thomson_600'])):
            thomson_600_temp.append(coincident_crashes_thomson_dict[k]['thomson_600'][i][0])
            thomson_600_time.append(coincident_crashes_thomson_dict[k]['thomson_600'][i][1])
            thomson_all_temp.append(coincident_crashes_thomson_dict[k]['thomson_600'][i][0])
            thomson_all_time.append(coincident_crashes_thomson_dict[k]['thomson_600'][i][1])
        # thomson at 730mm
        for i in range(len(coincident_crashes_thomson_dict[k]['thomson_730'])):
            thomson_730_temp.append(coincident_crashes_thomson_dict[k]['thomson_730'][i][0])
            thomson_730_time.append(coincident_crashes_thomson_dict[k]['thomson_730'][i][1])
            thomson_all_temp.append(coincident_crashes_thomson_dict[k]['thomson_730'][i][0])
            thomson_all_time.append(coincident_crashes_thomson_dict[k]['thomson_730'][i][1])
        # thomson at 900mm
        for i in range(len(coincident_crashes_thomson_dict[k]['thomson_900'])):
            thomson_900_temp.append(coincident_crashes_thomson_dict[k]['thomson_900'][i][0])
            thomson_900_time.append(coincident_crashes_thomson_dict[k]['thomson_900'][i][1])
            thomson_all_temp.append(coincident_crashes_thomson_dict[k]['thomson_900'][i][0])
            thomson_all_time.append(coincident_crashes_thomson_dict[k]['thomson_900'][i][1])
        

    i=0    
    j=0
    k=0
    thomson_combined = []
    thomson_combined_time = []
    while max([i, j, k]) < max([len(thomson_900_time), len(thomson_730_time), len(thomson_600_time)]):
        if thomson_900_time[i] == thomson_600_time[k] and thomson_600_time[k] == thomson_730_time[j]:
            thomson_combined.append(2 * thomson_900_temp[i] / ((thomson_600_temp[k] + thomson_730_temp[j])))
            thomson_combined_time.append(thomson_900_time[i])
            i += 1
            j += 1
            k += 1
            
        elif (thomson_900_time[i] < thomson_600_time[k]) or (thomson_900_time[i] < thomson_730_time[j]):
            i += 1
        elif (thomson_730_time[j] < thomson_600_time[k]) or (thomson_730_time[j] < thomson_900_time[i]):
            j += 1
        elif (thomson_600_time[k] < thomson_900_time[i]) or (thomson_600_time[k] < thomson_730_time[j]):
            k += 1
            
            
    if plot_individual_scatter:
        plt.scatter(thomson_600_time, thomson_600_temp, label="Thomson R600")
        plt.scatter(thomson_730_time, thomson_730_temp, label="Thomson R730")
        plt.scatter(thomson_900_time, thomson_900_temp, label="Thomson R900")
        
        
        poly_order = 1
        print("ALL TIME", (thomson_all_time))
        print("ALL TEMP", (thomson_all_temp))
        x, y = pop_nan(thomson_all_time, thomson_all_temp)
        fit_and_plot_polynomial(x, y, poly_order)
        
    if not normalize_time and not plot_ratio:
        # add features to the plot
        plt.title("Thomson Temperature Deviation over Time Since Most Recent Crash\nDataset Size: " + str(len(thomson_600_time)))
        plt.xlabel("Time Since Most Recent Crash [s]")
        plt.ylabel("Temperature Difference From Most recent Thomson Measurement [K]")
        plt.legend()
        plt.show()
    
    elif normalize_time and not plot_ratio:
        # add features to the plot
        plt.title("Thomson Temperature Deviation over Time Since Most Recent Crash\nDataset Size: " + str(len(thomson_600_time)))
        plt.xlabel("Phase Since Most Recent Crash [2*pi is one period]")
        plt.ylabel("Temperature Difference From Most recent Thomson Measurement [K]")
        plt.legend()
        plt.show()
        
    elif normalize_time and plot_ratio:
        print("NAN", np.isnan(thomson_combined).any())
        print("INF", np.isinf(thomson_combined).any())
        
        
        scatter = plt.scatter(thomson_combined_time, thomson_combined, label="Core to External Temperature Ratio")
        # scatter_cursors.add_cursors_to_multishot_scatter(output_dir, scatter, fig, shot_numbers=true_shot_list, )
        x, y = pop_nan(thomson_combined_time, thomson_combined)
        fit_and_plot_polynomial(x, y, 1)
        plt.title("Ratio of Core to Edge Plasma Temperatures over Phase\nDataset Size: " + str(len(thomson_combined_time)))
        plt.xlabel("Phase Since Most Recent Crash [2*pi is one period]")
        plt.ylabel("Ratio of Core to Edge Plasma Temperatures (2 * R900 / (R600 + R730))")
        plt.legend()
        plt.show()


    return




def fit_and_plot_polynomial(x, y, n):
    # Fit a polynomial of order n to the points
    coefficients = np.polyfit(x, y, n)
    polynomial = np.poly1d(coefficients)
    
    # Generate x values for plotting the polynomial
    x_plot = np.linspace(min(x), max(x), 500)
    y_plot = polynomial(x_plot)

    # Plot the polynomial
    plt.plot(x_plot, y_plot, label=f'Polynomial of Order {n}', color='r')
    
    return


def pop_nan(x, y):
    """
    Removes NaN values from both x and y, ensuring their dimensions remain the same.
    
    Parameters:
    x (numpy array): Array containing x values.
    y (numpy array): Array containing y values.
    
    Returns:
    x_clean (numpy array): x values with NaNs removed.
    y_clean (numpy array): y values with NaNs removed.
    """
    x = np.array(x)
    y = np.array(y)
    
    mask = ~np.isnan(x) & ~np.isnan(y)
    x_clean = x[mask]
    y_clean = y[mask]
    
    return x_clean, y_clean