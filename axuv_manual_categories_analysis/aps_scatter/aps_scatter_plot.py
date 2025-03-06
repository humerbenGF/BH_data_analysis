import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go



import load_save_data.load_data as load_data
import thomson.load_thomson as load_thomson
import axuv_categories_analysis.scatter as categories_scatter

def aps_scatter_stephen_separated():
    
    scatter_info_dict = categories_scatter.prepare_scatter_information_dict()
    
    labels = ["Dome", "Non-Dome"]
    
    fig=plt.figure(figsize=(10,6))
    
    colormap = plt.cm.bwr
    
    norm = plt.Normalize(0,1)
    
    # Create the scatter plot
    plt.scatter(scatter_info_dict["lifetimes_array"], scatter_info_dict["thomson_temp_array"], c=scatter_info_dict["is_dome_array"], cmap=plt.cm.get_cmap('bwr', len(labels)), alpha=0.3)
    
    lifetimes_dict = load_data.load_json_file("plasma_lifetime/lifetimes_list.json")
    
    thomson_dict = load_thomson.make_thomson_dict(600, 5)
    
    
    # load in stephen's requested shots
    s_data_categories = load_data.load_json_file("axuv_categories_analysis/aps_scatter/aps_classification_data_sustain.json")
    s_data_shots = []
    for sustainment in s_data_categories.keys():
        for shot in s_data_categories[sustainment].keys():
            s_data_shots.append(int(shot))
    
    # Separate into arrays for plotting
    s_data_sustain_array = []
    s_data_non_sustain_array = []
    lifetimes_sustain_array = []
    lifetimes_non_sustain_array = []
    thomson_sustain_array = []
    thomson_non_sustain_array = []
    shots_sustain = []
    shots_non_sustain = []
    is_dome_sustain = []
    is_dome_non_sustain = []
    
    # Get keys to check whether data exists
    sustain_keys = s_data_categories["sustain"].keys()
    non_sustain_keys = s_data_categories["non_sustain"].keys()
    lifetimes_keys = lifetimes_dict.keys()
    thomson_keys = thomson_dict.keys()
    
    for s in s_data_shots:
        if str(s) in sustain_keys and str(s) in lifetimes_keys and str(s) in thomson_keys:
            s_data_sustain_array.append(s_data_categories["sustain"][str(s)])
            lifetimes_sustain_array.append(lifetimes_dict[str(s)])
            thomson_sustain_array.append(thomson_dict[str(s)])
            shots_sustain.append(s)
            if s_data_categories["sustain"][str(s)][0] in [2]:
                is_dome_sustain.append(1)  # Dome
            else:
                is_dome_sustain.append(0)  # Non-dome
            
        elif str(s) in non_sustain_keys and str(s) in lifetimes_keys and str(s) in thomson_keys:
            s_data_non_sustain_array.append(s_data_categories["non_sustain"][str(s)])
            lifetimes_non_sustain_array.append(lifetimes_dict[str(s)])
            thomson_non_sustain_array.append(thomson_dict[str(s)])
            shots_non_sustain.append(s)
            if s_data_categories["non_sustain"][str(s)][0] in [2]:
                is_dome_non_sustain.append(1)  # Dome
            else:
                is_dome_non_sustain.append(0)  # Non-dome
    
    # Color mapping: dome = blue, non-dome = red
    color_map = {0: 'red', 1: 'blue'}


    # Combine arrays for easier iteration
    combined_arrays = [
        (lifetimes_sustain_array, thomson_sustain_array, shots_sustain, is_dome_sustain, "Sustain", "o"),
        (lifetimes_non_sustain_array, thomson_non_sustain_array, shots_non_sustain, is_dome_non_sustain, "Non-Sustain", "x")
    ]

    # Loop over both sustain and non-sustain arrays
    for lifetimes_array, thomson_array, shots_array, is_dome_array, sustain_label, marker in combined_arrays:
        for i, (lifetime, temp, shot, dome_status) in enumerate(zip(lifetimes_array, thomson_array, shots_array, is_dome_array)):
            color = color_map[dome_status]
            plt.scatter(lifetime, temp, color=color, marker=marker, label=f"{'Dome' if dome_status == 1 else 'Non-Dome'}/{sustain_label}" if i == 0 else "")
            plt.text(lifetime, temp, str(shot), fontsize=9, ha='right', va='bottom')  # Label each point with shot number

    # Create custom legend handles
    legend_elements = [
        mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=8, label='Dome/Sustain'),
        mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=8, label='Non-Dome/Sustain'),
        mlines.Line2D([], [], color='blue', marker='x', linestyle='None', markersize=8, label='Dome/Non-Sustain'),
        mlines.Line2D([], [], color='red', marker='x', linestyle='None', markersize=8, label='Non-Dome/Non-Sustain')
    ]

    plt.title("Categorized Thomson Temperature over Plasma Lifetime")
    plt.xlabel("Lifetime [s]")
    plt.ylabel("Thomson Temperature at 5ms [eV]")
    plt.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.show()
    
    
    
def aps_scatter_poster(make_html_plot=True, showfig=True):
    thomson_dict = load_thomson.make_thomson_dict(600, 5)
    lifetimes_dict = load_data.load_json_file("plasma_lifetime/lifetimes_list.json")
    categories_dict = load_data.load_json_file("axuv_categories_analysis/aps_scatter/thomson_classification.json")
    combined_categories_dict = make_combined_categories_dict()
    xiande_exclusion_shots = make_xiande_exclusion_shots()
    
    # start by filtering the arrays based on what values are present in all the arrays
    thomson_dict_keys = thomson_dict.keys()
    lifetimes_dict_keys = lifetimes_dict.keys()
    thomson_dict_filtered = {}
    lifetimes_dict_filtered = {}
    combined_categories_dict_filtered = {}
    
    for k in combined_categories_dict.keys():
        if (k in thomson_dict_keys) and (k in lifetimes_dict_keys) and (int(k) not in xiande_exclusion_shots) and (type(lifetimes_dict[k]) != type(str())):
            thomson_dict_filtered[k] = thomson_dict[k]
            lifetimes_dict_filtered[k] = lifetimes_dict[k]
            combined_categories_dict_filtered[k] = combined_categories_dict[k]
        else:
            if k in categories_dict['sustain'].keys():
                categories_dict['sustain'] = delete_key(categories_dict['sustain'], k)
            elif k in categories_dict['non_sustain'].keys():
                categories_dict['non_sustain'] = delete_key(categories_dict['non_sustain'], k)
            
                
    lifetimes_dict = lifetimes_dict_filtered
    thomson_dict = thomson_dict_filtered
    combined_categories_dict = combined_categories_dict_filtered
    
    # turn lifetimes into ms
    for k in lifetimes_dict.keys():
        lifetimes_dict[k] = lifetimes_dict[k] * 1000
    
    # get information for adding text to graph
    shot_list = []
    lifetimes_list = []
    thomson_list = []
    for k in lifetimes_dict.keys():
        shot_list.append(k)
        lifetimes_list.append(lifetimes_dict[k])
        thomson_list.append(thomson_dict[k])
    
    
    # turn this data into plottable arrays
    lifetimes_list_dome_sustain = []
    lifetimes_list_dome_non_sustain = []
    lifetimes_list_non_dome_sustain = []
    lifetimes_list_non_dome_non_sustain = []
    
    thomson_list_dome_sustain = []
    thomson_list_dome_non_sustain = []
    thomson_list_non_dome_sustain = []
    thomson_list_non_dome_non_sustain = []
    
    shot_list_dome_sustain = []
    shot_list_dome_non_sustain = []
    shot_list_non_dome_sustain = []
    shot_list_non_dome_non_sustain = []
    
    dome_classifications_array = ["2"]
    for k in combined_categories_dict.keys():
        # separate into sustain/non-sustain
        if k in categories_dict['sustain']:
            if categories_dict['sustain'][k][0] in dome_classifications_array:
                lifetimes_list_dome_sustain.append(lifetimes_dict[k])
                thomson_list_dome_sustain.append(thomson_dict[k])
                shot_list_dome_sustain.append(int(k))
            else:
                lifetimes_list_non_dome_sustain.append(lifetimes_dict[k])
                thomson_list_non_dome_sustain.append(thomson_dict[k])
                shot_list_non_dome_sustain.append(int(k))
        elif k in categories_dict['non_sustain']:
            if categories_dict['non_sustain'][k][0] in dome_classifications_array:
                lifetimes_list_dome_non_sustain.append(lifetimes_dict[k])
                thomson_list_dome_non_sustain.append(thomson_dict[k])
                shot_list_dome_non_sustain.append(int(k))
            else:
                lifetimes_list_non_dome_non_sustain.append(lifetimes_dict[k])
                thomson_list_non_dome_non_sustain.append(thomson_dict[k])
                shot_list_non_dome_non_sustain.append(int(k))
    
    
    plt.rcParams['font.size'] = 16  # Change all font sizes
    plt.rcParams['axes.titlesize'] = 20  # Title font size
    plt.rcParams['axes.labelsize'] = 18  # Axis label font size
    plt.rcParams['xtick.labelsize'] = 14  # X tick label size
    plt.rcParams['ytick.labelsize'] = 14  # Y tick label size
    plt.rcParams['legend.fontsize'] = 13  # Legend font size
    
    
    plt.figure(figsize=(12.7,7))
    
    # Add labels to each point
    for i in range(len(lifetimes_list)):
        plt.text(lifetimes_list[i], thomson_list[i], shot_list[i], fontsize=12, ha='right')
    
    size = 70
    a_o = 0.8
    a_x = 1.0
    # plot all four combinations
        # dome sustain
    plt.scatter(lifetimes_list_dome_sustain, thomson_list_dome_sustain, color="red", marker="o", label="AXUV Dome & Sustain", alpha=a_o, s=size)
        # non-dome sustain
    plt.scatter(lifetimes_list_non_dome_sustain, thomson_list_non_dome_sustain, color="red", marker="x", label="AXUV Non-Dome & Sustain", alpha=a_x, s=size)
        # dome / non-sustain
    plt.scatter(lifetimes_list_dome_non_sustain, thomson_list_dome_non_sustain, color="blue", marker="o", label="AXUV Dome & Non-Sustain", alpha=a_o, s=size)
        # non-dome / non-sustain
    plt.scatter(lifetimes_list_non_dome_non_sustain, thomson_list_non_dome_non_sustain, color="blue", marker="x", label="AXUV Non-Dome & Non-Sustain", alpha=a_x, s=size)
    
    # add in plot details
    plt.legend(loc='upper left')
    plt.title("Shot Categorization by AXUV Shape and Sustain Setting\nElectron Temperature vs Plasma Lifetime")
    plt.xlabel("Total Plasma Lifetime [ms]")
    plt.ylabel("Thomson Temperature at 5ms [eV]")
    plt.savefig("test.png", dpi=400)
    if showfig:
        plt.show()
    
    # make interactive html plot
    if make_html_plot:
        # dome sustain
        df_dome_sustain = pd.DataFrame(
            {
                'x': lifetimes_list_dome_sustain,
                'y': thomson_list_dome_sustain,
                'Shot': shot_list_dome_sustain,
            }
        )
        
        # non-dome sustain
        df_non_dome_sustain = pd.DataFrame(
            {
                'x': lifetimes_list_non_dome_sustain,
                'y': thomson_list_non_dome_sustain,
                'Shot': shot_list_non_dome_sustain,
            }
        )
        
        # dome non-sustain
        df_dome_non_sustain = pd.DataFrame(
            {
                'x': lifetimes_list_dome_non_sustain,
                'y': thomson_list_dome_non_sustain,
                'Shot': shot_list_dome_non_sustain,
            }
        )
        
        # non-dome non-sustain
        df_non_dome_non_sustain = pd.DataFrame(
            {
                'x': lifetimes_list_non_dome_non_sustain,
                'y': thomson_list_non_dome_non_sustain,
                'Shot': shot_list_non_dome_non_sustain,
            }
        )
        


        # Initialize a figure
        fig = go.Figure()

        # Add dome/sustain scatter
        fig.add_trace(go.Scatter(
            x=df_dome_sustain['x'], 
            y=df_dome_sustain['y'],
            mode='markers',
            marker=dict(symbol='circle', color='red'),
            hovertext=df_dome_sustain['Shot'],
            name='Dome Sustain'  # Label for the legend
        ))

        # Add non-dome/sustain scatter
        fig.add_trace(go.Scatter(
            x=df_non_dome_sustain['x'], 
            y=df_non_dome_sustain['y'],
            mode='markers',
            marker=dict(symbol='x', color='red'),
            hovertext=df_non_dome_sustain['Shot'],
            name='Non-Dome Sustain'  # Label for the legend
        ))

        # Add dome/non-sustain scatter
        fig.add_trace(go.Scatter(
            x=df_dome_non_sustain['x'], 
            y=df_dome_non_sustain['y'],
            mode='markers',
            marker=dict(symbol='circle', color='blue'),
            hovertext=df_dome_non_sustain['Shot'],
            name='Dome Non-Sustain'  # Label for the legend
        ))

        # Add non-dome/non-sustain scatter
        fig.add_trace(go.Scatter(
            x=df_non_dome_non_sustain['x'], 
            y=df_non_dome_non_sustain['y'],
            mode='markers',
            marker=dict(symbol='x', color='blue'),
            hovertext=df_non_dome_non_sustain['Shot'],
            name='Non-Dome Non-Sustain'  # Label for the legend
        ))

        # Update layout, if needed
        fig.update_layout(
            title="Plasma Temperature Over Lifetime",
            xaxis_title="Total Plasma Lifetime [ms]",
            yaxis_title="Thomson Temperature at 5ms [eV]",
        )

        # Save the plot to an interactive HTML file
        fig.write_html("temp_over_lifetime_dome_binary.html")
    
    return


def make_combined_categories_dict():
    categories_dict = load_data.load_json_file("axuv_categories_analysis/aps_scatter/thomson_classification.json")
    
    combined_categories_dict = {}
    for sustainment in categories_dict.keys():
        for s in categories_dict[sustainment].keys():
            combined_categories_dict[s] = categories_dict[sustainment][s]
            
    return combined_categories_dict


def delete_key(d, k):
    if k in d:
        del d[k]
    return d


def make_xiande_exclusion_shots():
    exclusion_array = [20081, 20083, 20084, 20297, 20346]
    exclusion_array = list_from_range(20740, 20882)
    exclusion_array += list_from_range(21482, 21522)
    
    return exclusion_array


def list_from_range(starting_shot, ending_shot):
    L = []
    cur_shot = starting_shot
    while cur_shot <= ending_shot:
        L.append(cur_shot)
        cur_shot += 1
    
    return L