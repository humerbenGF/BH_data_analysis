# import libraries
#################################################################
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import mpld3
import plotly.express as px
import pandas as pd



# import personal files
#################################################################
import load_save_data.load_data as load_data
import cursors.scatter_cursors as scatter_cursors
import cursors.add_click_action as scatter_click



def scatter_shots_since_li_num_crashes(output_dir, saveplot=True):
    if output_dir[-1] != "/":
        output_dir += "/"

    scatter_data = get_scatter_data(output_dir=output_dir)
    
    lifetimes_array = []
    n_crashes_array = []
    shots_since_li = []
    shots_list_strings = []
    labels_list = []
    for k in scatter_data["lifetimes"].keys():
        if k in scatter_data["crash_info"].keys() and type(scatter_data["crash_info"][k]) != type(str()) and type(scatter_data["lifetimes"][k]) != type(str()) and k in scatter_data['shots_since_li'].keys():
            lifetimes_array.append(scatter_data["lifetimes"][k])
            n_crashes_array.append(len(scatter_data["crash_info"][k]["times"]))
            shots_since_li.append(scatter_data['shots_since_li'][k])
            shots_list_strings.append(k)
            labels_list.append(f"{k}: {n_crashes_array[-1]} crashes")
    

    
    if saveplot:
        data = pd.DataFrame({
            "Plasma Lifetime [s]": lifetimes_array,
            "Shots Since Lithium Coat": shots_since_li,
            "Number of Crashes": n_crashes_array,
            "shots list":shots_list_strings
        })

        # Create the scatter plot
        fig = px.scatter(
            data,
            x="Plasma Lifetime [s]",
            y="Shots Since Lithium Coat",
            color="Number of Crashes",
            color_continuous_scale="Jet",
            log_y=True,
            title="Shots Since Lithium Coat over Plasma Lifetime",
            labels={
                "Shot Number": "shots list",
                "Plasma Lifetime [s]": "Plasma Lifetime [s]",
                "Shots Since Lithium Coat": "Shots Since Lithium Coat",
                "Number of Crashes": "Number of Crashes"
            }
        )

        # Adjust layout for better display
        fig.update_layout(
            coloraxis_colorbar=dict(title="Number of Crashes"),
            title_x=0.5,  # Center the title
            template="plotly_white",
        )

        # Save the plot as an interactive HTML file
        fig.write_html("plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/shots_since_li_lifetime_num_crashes.html")

    else:
        # Create the plot
        fig, ax = plt.subplots(figsize=(16, 9))
        scatter = ax.scatter(
            lifetimes_array, 
            shots_since_li, 
            c=n_crashes_array, 
            cmap="jet", 
            s=10
        )

        ax.set_yscale('log')
        ax.set_ylabel("Shots Since Lithium Coat")
        ax.set_xlabel("Plasma Lifetime [s]")
        ax.set_title(f"Shots Since Lithium Coat over Plasma Lifetime\n{len(lifetimes_array)} Shots")
        fig.colorbar(scatter, label="Number of Crashes")
        scatter_cursors.add_cursors_to_scatter(scatter, shots_list_strings)
        scatter_click.add_click_action_timeseries_plots(output_dir, scatter, fig, shots_list_strings)
        plt.show()

    
    return
    
    
    

def scatter_lifetime_amp_largest_crash(output_dir, savefig=True):
    if output_dir[-1] != "/":
        output_dir += "/"
    
    scatter_data = get_scatter_data(output_dir=output_dir)
    
    lifetimes_array = []
    nth_crashes_amps = []
    shots_since_li = []
    shots_list_strings = []
    for k in scatter_data["lifetimes"].keys():
        if k in scatter_data["crash_info"].keys() and type(scatter_data["crash_info"][k]) != type(str()) and type(scatter_data["lifetimes"][k]) != type(str()) and k in scatter_data['shots_since_li'].keys():
            if len(scatter_data["crash_info"][k]["amps"]) > 0:
                lifetimes_array.append(scatter_data["lifetimes"][k])
                shots_since_li.append(scatter_data['shots_since_li'][k])
                nth_crashes_amps.append(max(scatter_data["crash_info"][k]["amps"]))
                shots_list_strings.append(k)
    
    
    
    
    if savefig:
        # Create a DataFrame
        data = pd.DataFrame({
            "Plasma Lifetime [s]": lifetimes_array,
            "Amplitude of Largest Crash [A]": nth_crashes_amps,
            "Shots Since Li Pot Coat": shots_since_li,
            "shots list": shots_list_strings
        })

        # Create the scatter plot
        fig = px.scatter(
            data,
            x="Plasma Lifetime [s]",
            y="Amplitude of Largest Crash [A]",
            color="Shots Since Li Pot Coat",
            color_continuous_scale="Jet",
            log_y=True,  # Logarithmic y-axis
            title="Amplitude of Largest AXUV Crash over Plasma Lifetime",
            labels={
                "Shot": "shots list",
                "Plasma Lifetime [s]": "Plasma Lifetime [s]",
                "Amplitude of Largest Crash [A]": "Amplitude of Largest Crash [A]",
                "Shots Since Li Pot Coat": "Shots Since Li Pot Coat"
            }
        )

        # Customize layout
        fig.update_layout(
            coloraxis_colorbar=dict(title="Shots Since Li Pot Coat"),
            title_x=0.5,  # Center the title
            template="plotly_white",
            width=1200,  # Equivalent to figsize=(16, 9)
            height=675
        )

        # Save the plot as an interactive HTML file
        fig.write_html("plots_github/GF_html_plot_viewer/PI3/axuv_crash_analysis_plots/scatter_lifetime_nth_crash_amp_shots_since_li.html")
    else:
        fig, ax = plt.subplots(figsize=(16,9))
        scatter = plt.scatter(lifetimes_array, nth_crashes_amps, c=shots_since_li, cmap="jet", norm=LogNorm(), s=10)
        plt.yscale('log')
        plt.ylabel("Amplitude of Largest Crash [A]")
        plt.xlabel("Plasma Lifetime [s]")
        plt.title("Amplitude of Largest AXUV Crash over Plasma Lifetime")
        plt.colorbar(label="Shots Since Li Pot Coat")
        
        scatter_cursors.add_cursors_to_scatter(scatter, shots_list_strings)
        scatter_click.add_click_action_timeseries_plots(output_dir, scatter, fig, shots_list_strings)
        plt.show()
    
    return


def scatter_lifetime_time_largest_crash(output_dir):
    scatter_data = get_scatter_data(output_dir=output_dir)
    
    lifetimes_array = []
    tallest_crash_times = []
    for k in scatter_data["lifetimes"].keys():
        if k in scatter_data["crash_info"].keys() and type(scatter_data["crash_info"][k]) != type(str()) and type(scatter_data["lifetimes"][k]) != type(str()):
            if len(scatter_data["crash_info"][k]["times"]) > 0:
                lifetimes_array.append(scatter_data["lifetimes"][k])
                i = scatter_data["crash_info"][k]["amps"].index(max(scatter_data["crash_info"][k]["amps"]))
                tallest_crash_times.append(scatter_data["crash_info"][k]["times"][i])
    
    plt.scatter(lifetimes_array, tallest_crash_times)
    plt.plot([0, min(max(lifetimes_array), max(tallest_crash_times))], [0, min(max(lifetimes_array), max(tallest_crash_times))], 'k', linewidth=1.0)
    plt.show()
    
    return





def get_scatter_data(output_dir):
    # check output dir
    if output_dir[-1] != "/":
        output_dir += "/"
        
    # machine settings
        # get shots since Li coating
    shots_since_li = load_data.load_json_file("machine_settings_and_state/shots_since_li/shots_since_li.json")
    
    # plasma results
        # get lifetimes data
    lifetimes_data = load_data.load_json_file("plasma_data_and_parameters/plasma_lifetime/lifetimes_dict.json")
    
        # get crash related information
    crash_info = load_data.load_json_file(output_dir + "crash_info_with_hardware_error.json")
    

    
    # make dictionary of relevant data
    scatter_data = {"lifetimes": lifetimes_data, "crash_info": crash_info, "shots_since_li": shots_since_li}
    
    return scatter_data
    
    
    