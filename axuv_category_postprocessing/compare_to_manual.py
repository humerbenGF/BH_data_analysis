# import libraries
#################################################################



# import personal files
#################################################################
from load_save_data.load_data import load_json_file
from plots_github.GF_html_plot_viewer.plot_generation_tools.plotly_scatter import make_plotly_multi_scatter



def compare_manual_dome_non_dome_to_parameter_concavity(manual_filename, categorization_metadata_filename, concavity_time):
    # load in data
    manual_cat = load_json_file(manual_filename)
    auto_cat_meta = load_json_file(categorization_metadata_filename)
    
    # set up plotting arrays
    scatter_names = ["Dome Sustain", "Non-Dome Sustain", "Dome Non-Sustain", "Non-Dome Non-Sustain"]
    x_scatter_data = [[], [], [], []]               # dome sustain // non-dome sustain // dome non-sustain // non-dome non-sustain
    y_scatter_data = [[], [], [], []]               # dome sustain // non-dome sustain // dome non-sustain // non-dome non-sustain
    scatter_text_arrays = [[], [], [], []]          # dome sustain // non-dome sustain // dome non-sustain // non-dome non-sustain

    # go through the manual sustain shots
    for sustainment in manual_cat.keys():
        for k in manual_cat[sustainment].keys():
            if k in auto_cat_meta.keys():
                if type(str()) not in [type(auto_cat_meta[k]), type(manual_cat[sustainment][k])] and "first_crash_info" in auto_cat_meta[k].keys():
                    x_data = auto_cat_meta[k][f"{concavity_time}_info"]['time']
                    y_data = auto_cat_meta[k][f"{concavity_time}_info"]['concavity']
                    if sustainment == 'sustain':
                        if manual_cat[sustainment][k][0] == '3':
                            x_scatter_data[0].append(x_data)
                            y_scatter_data[0].append(y_data)
                            scatter_text_arrays[0].append(f"Shot: {k}")
                        else:
                            x_scatter_data[1].append(x_data)
                            y_scatter_data[1].append(y_data)
                            scatter_text_arrays[1].append(f"Shot: {k}")
                    else:
                        if manual_cat[sustainment][k][0] == '3':
                            
                            x_scatter_data[2].append(x_data)
                            y_scatter_data[2].append(y_data)
                            scatter_text_arrays[2].append(f"Shot: {k}")
                        else:
                            x_scatter_data[3].append(x_data)
                            y_scatter_data[3].append(y_data)
                            scatter_text_arrays[3].append(f"Shot: {k}")

    
    # x_line_arrays=[[-0.1, 0.1]], y_line_arrays=[[-0.1, 0.1]]
                            
    make_plotly_multi_scatter(
        x_scatter_arrays=x_scatter_data, y_scatter_arrays=y_scatter_data,
        scatter_names=scatter_names, scatter_colors=['red', 'red', 'blue', 'blue'], scatter_text_arrays=scatter_text_arrays,
        x_line_arrays=[], y_line_arrays=[], line_names=['y=x'], line_colors=['black'],
        title=f"Concavity of {concavity_time} Over {concavity_time} Time", xlabel="time", ylabel='concavity',
        filename=f"plots_github/GF_html_plot_viewer/PI3/axuv_categorization_plots/parameter_space_exploration/{concavity_time}_concavity_time_crash_info.html",
        scatter_markers=['circle', 'x', 'circle', 'x'], show_plot=True)