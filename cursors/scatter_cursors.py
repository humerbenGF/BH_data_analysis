# import packages
#################################################################
import os
import mplcursors
import subprocess
import warnings


# import personal files
#################################################################


# plot individual quantities
# import post_proc_axuv_crash.post_proc_plot_misc_timeseries as plot_misc_timeseries
import timeseries_plots.q_profile.plot_q_profile as plot_q


# add cursors to scatter plot
#################################################################
def add_cursors_to_multishot_scatter(output_dir, scatter, fig, shot_numbers, hover_text_array, click_timeseries_plots_list=[]):
    # 
    if output_dir[-1] != "/":
        output_dir += "/"
    
    # filter out matplotlib warning messages

    warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
    
    
    # Enable interactive annotation
    cursor = mplcursors.cursor(scatter, hover=True)

    # Define the annotation content
    @cursor.connect("add")
    def on_add(sel):
        index = sel.index
        sel.annotation.set(text=hover_text_array[index], position=(0, 10), anncoords="offset points")
        sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)

    # Define the click event
    def on_pick(event):
        ind = event.ind[0]
        if click_timeseries_plots_list == [] or "crashes_timeseries" in click_timeseries_plots_list or "all" in click_timeseries_plots_list:
            folder_path = output_dir + "postproc_plots/" + str(int(int(shot_numbers[ind])/1000)*1000) + "/axuv_timeseries_crashes/"
            file_path = folder_path + str(shot_numbers[ind]) + '_timeseries_crashes' + '.png'  # Example file path, modify as needed
            print(f"Opening file: {file_path}")
            # Ensure the file exists for demonstration purposes
            if not os.path.exists(file_path):
                print("FILE DOES NOT EXIST")

            subprocess.Popen(['start', file_path], shell=True)
        
        # if "inductance_recon" in click_timeseries_plots_list or "all" in click_timeseries_plots_list:
        #     folder_path = output_dir + "postproc_plots/" + str(int(int(shot_numbers[ind])/1000)*1000) + "/inductance_recon_timeseries/"
        #     file_path = folder_path + str(shot_numbers[ind]) + '_inductance_recon' + '.png'  # Example file path, modify as needed
        #     # Ensure the file exists for demonstration purposes
        #     if not os.path.exists(file_path):
        #         print("Generating Inductance Timeseries Plot")
        #         plot_misc_timeseries.plot_recon_inductance_timeseries(int(shot_numbers[ind]), output_dir)

            print(f"Opening file: {file_path}")
            subprocess.Popen(['start', file_path], shell=True)
            
        if "q_profile" in click_timeseries_plots_list or "all" in click_timeseries_plots_list:
            print("trying q profile")
            folder_path = output_dir + "postproc_plots/" + str(int(int(shot_numbers[ind])/1000)*1000) + "/q_profiles/"
            file_path = folder_path + str(shot_numbers[ind]) + 'q_profile' + '.png'  # Example file path, modify as needed
            # Ensure the file exists for demonstration purposes
            if not os.path.exists(file_path):
                print("Generating q Profile Plot")
                plot_q.plot_q_profile(int(shot_numbers[ind]))
            
    

    # Connect the pick event handler
    fig.canvas.mpl_connect('pick_event', on_pick)

    # Make the scatter plot pickable
    scatter.set_picker(True)
        
    return


def add_cursors_to_scatter(scatter, hover_text_array):
    # Enable interactive annotation
    cursor = mplcursors.cursor(scatter, hover=True)

    # Define the annotation content
    @cursor.connect("add")
    def on_add(sel):
        index = sel.index
        sel.annotation.set(text=hover_text_array[index], position=(0, 10), anncoords="offset points")
        sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)
        
    return