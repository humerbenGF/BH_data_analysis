# import libraries
#################################################################
import matplotlib.pyplot as plt
import pandas as pd
import mpld3
import plotly.tools as tls
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# import personal files
#################################################################
import load_save_data.load_data as load_data_axuv_cat
import thomson.load_thomson as load_thomson
import cursors.scatter_cursors as scatter_cursors


# make scatter plot by category
#################################################################
def make_scatter_by_category():
    '''

    
    # get a list of all the shots that are categorized
    shots_list = get_total_shots_list(rise_data)
    shots_list.sort()
    
    # get a dict of category info
    category_info_dict = {}
    category_pairs_dict = {}
    new_shots_list = []
    for shot in shots_list:
        for r in rise_data.keys():
            for f in fall_data.keys():
                if (shot in rise_data[r]) and (shot in fall_data[f]):
                    category_info_dict[str(shot)] = one_hot_dict[r+f]
                    category_pairs_dict[str(shot)] = r+f
                    new_shots_list.append(shot)
    
    shots_list = new_shots_list[:]
    
    # get a dict of lifetimes
    lifetimes_dict = load_data_axuv_cat.load_json_file("plasma_lifetime/lifetimes_list.json")
    
    # get a dict of shots since lithium
    ss_li_df = load_data_axuv_cat.load_csv_file("shots_since_li/shots_since_li.csv")
    
    shots_since_li_dict = {}
    for shot in shots_list:
        if shot in ss_li_df["Shot ID"]:
            gun = ss_li_df.loc[ss_li_df["Shot ID"] == shot, "Shots Since Li GUN Coat"]
            gun = gun.iloc[0]
            pot = ss_li_df.loc[ss_li_df["Shot ID"] == shot, "Shots Since Li POT Coat"]
            pot = pot.iloc[0]
            shots_since_li_dict[str(shot)] = min([gun, pot])
    
    # get a dict of thomson data
    thomson_temp_dict = load_thomson.make_thomson_dict(600, 5)
    
    
    shots_array = []
    lifetimes_array = []
    categories_array = []
    category_pairs_array = []
    shots_since_li_array = []
    thomson_temp_array = []
    hover_text_array = []
    cat_info_keys = category_info_dict.keys()
    cat_pairs_keys = category_pairs_dict.keys()
    ss_li_keys = shots_since_li_dict.keys()
    thomson_temp_keys = thomson_temp_dict.keys()
    for k in lifetimes_dict.keys():
        if k in cat_info_keys and k in ss_li_keys and lifetimes_dict[k] != '<N/C>' and k in thomson_temp_keys and k in cat_pairs_keys:
            lifetimes_array.append(lifetimes_dict[k])
            categories_array.append(category_info_dict[k])
            shots_since_li_array.append(shots_since_li_dict[k])
            thomson_temp_array.append(thomson_temp_dict[k])
            category_pairs_array.append(training_classifications['rise_classifications'][category_pairs_dict[k][0]] + " | " + training_classifications['fall_classifications'][category_pairs_dict[k][1]])
            hover_text_array.append(category_pairs_array[-1] + "\nShot:" + k)
            shots_array.append(int(k))
    
    '''
    # load in data
    rise_data = load_data_axuv_cat.load_rise_data()
    fall_data = load_data_axuv_cat.load_fall_data()
    training_classifications = load_data_axuv_cat.load_json_file("axuv_categories_analysis/training_classifications.json")
    
    # change dict to one hot for colorbar later
    one_hot_dict = one_hot_categories(rise_data.keys(), fall_data.keys())
    labels = list(one_hot_dict.keys())
    
    scatter_info_dict = prepare_scatter_information_dict()
    
    new_labels = []
    for label in labels:
        new_labels.append(training_classifications['rise_classifications'][label[0]] + " | " + training_classifications['fall_classifications'][label[1]])
    
    fig=plt.figure(figsize=(16,9))
    
    labels = new_labels[:]
    
    
    colormap = plt.cm.jet
    
    norm = plt.Normalize(vmin=min(scatter_info_dict["categories_array"]), vmax=max(scatter_info_dict["categories_array"]))
            
    # Create the scatter plot
    scatter = plt.scatter(scatter_info_dict["lifetimes_array"], scatter_info_dict["thomson_temp_array"], c=scatter_info_dict["categories_array"], cmap=plt.cm.get_cmap('jet', len(labels)))

    # Create a custom legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=label,
                              markerfacecolor=colormap(norm(i)), markersize=10)
                   for i, label in enumerate(labels)]

    # Add the legend to the plot
    plt.legend(handles=legend_elements, title="Categories")
    plt.ylabel("Thomson Temperature at 5ms [eV]")
    plt.xlabel("Plasma Lifetime [s]")
    plt.title("Plasma Temperature Over Lifetime Colored by Category")
    
    # add cursors
    scatter_cursors.add_cursors_to_multishot_scatter(output_dir="preprocessed_data/AXUV-crashes_2024-09-03_1", scatter=scatter, fig=fig, shot_numbers=scatter_info_dict["shots_array"], hover_text_array=scatter_info_dict["hover_text_array"])
    
    plt.show()
            
    return


# make scatter of whether a shot is a dome or not
#################################################################
def make_scatter_is_dome():
    scatter_info_dict = prepare_scatter_information_dict()
    
    print("PLOTTING SHOTS RANGE:", min(scatter_info_dict["shots_array"]), "to", max(scatter_info_dict["shots_array"]))
    
    matplotlib=True
    if matplotlib:
        labels = ["Dome", "Non-Dome"]
        
        fig=plt.figure(figsize=(16,9))    
        
        colormap = plt.cm.bwr
        
        norm = plt.Normalize(0,1)
                
        # Create the scatter plot
        scatter = plt.scatter(scatter_info_dict["lifetimes_array"], scatter_info_dict["thomson_temp_array"], c=scatter_info_dict["is_dome_array"], cmap=plt.cm.get_cmap('bwr', len(labels)))

        # Create a custom legend
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=label,
                                markerfacecolor=colormap(norm(i)), markersize=10)
                    for i, label in enumerate(labels)]

        # Add the legend to the plot
        # plt.legend(handles=legend_elements, title="Categories")
        plt.ylabel("Thomson Temperature at 5ms [eV]")
        plt.xlabel("Plasma Lifetime [s]")
        plt.title("Plasma Temperature Over Lifetime Colored by Category")
        
        # add cursors
        scatter_cursors.add_cursors_to_multishot_scatter(output_dir="preprocessed_data/AXUV-crashes_2024-09-03_1", scatter=scatter, fig=fig, shot_numbers=scatter_info_dict["shots_array"], hover_text_array=scatter_info_dict["hover_text_array"])
        
        plt.show()
    
    plotly=False
    if plotly:

        xvals = scatter_info_dict["lifetimes_array"]
        yvals = scatter_info_dict["thomson_temp_array"]
        names = scatter_info_dict["shots_array"]

        df = pd.DataFrame(
            {
                'x': xvals,
                'y': yvals,
                'Shot': names,
                'is_dome': scatter_info_dict["is_dome_array"]
            }
        )
        
        # Define color mapping: 0 -> 'blue', 1 -> 'red'
        df['color'] = df['is_dome'].map({0: 'Dome', 1: 'Non-Dome'})

        # Create scatter plot with color based on 'is_dome' column
        fig = px.scatter(df, 'x', 'y', hover_data=['Shot'], color='color')

        # Update layout, if needed
        fig.update_layout(
            title="Plasma Temperature Over Lifetime Colored by Category",
            xaxis_title="Plasma Lifetime [s]",
            yaxis_title="Thomson Temperature at 5ms [eV]",
        )

        # Save the plot to an interactive HTML file
        fig.write_html("temp_over_lifetime_dome_binary.html")
    
    
            
    return




def prepare_scatter_information_dict():
    # load in data
    rise_data = load_data_axuv_cat.load_rise_data()
    fall_data = load_data_axuv_cat.load_fall_data()
    
    # change dict to one hot for colorbar later
    one_hot_dict = one_hot_categories(rise_data.keys(), fall_data.keys())
    labels = list(one_hot_dict.keys())
    
    # get a list of all the shots that are categorized
    shots_list = get_total_shots_list(rise_data)
    shots_list.sort()
    
    # get a dict of category info
    category_info_dict = {}
    category_pairs_dict = {}
    new_shots_list = []
    for shot in shots_list:
        for r in rise_data.keys():
            for f in fall_data.keys():
                if (shot in rise_data[r]) and (shot in fall_data[f]):
                    category_info_dict[str(shot)] = one_hot_dict[r+f]
                    category_pairs_dict[str(shot)] = r+f
                    new_shots_list.append(shot)
    
    shots_list = new_shots_list[:]
    
    # get a dict of lifetimes
    lifetimes_dict = load_data_axuv_cat.load_json_file("plasma_lifetime/lifetimes_list.json")
    
    # get a dict of shots since lithium
    ss_li_df = load_data_axuv_cat.load_csv_file("shots_since_li/shots_since_li.csv")
    
    shots_since_li_dict = {}
    for shot in shots_list:
        if shot in ss_li_df["Shot ID"]:
            gun = ss_li_df.loc[ss_li_df["Shot ID"] == shot, "Shots Since Li GUN Coat"]
            gun = gun.iloc[0]
            pot = ss_li_df.loc[ss_li_df["Shot ID"] == shot, "Shots Since Li POT Coat"]
            pot = pot.iloc[0]
            shots_since_li_dict[str(shot)] = min([gun, pot])
    
    # get a dict of thomson data
    thomson_temp_dict = load_thomson.make_thomson_dict(600, 5)
    
    training_classifications = load_data_axuv_cat.load_json_file("axuv_categories_analysis/training_classifications.json")
    
    is_dome = []
    shots_array = []
    lifetimes_array = []
    categories_array = []
    category_pairs_array = []
    shots_since_li_array = []
    thomson_temp_array = []
    hover_text_array = []
    cat_info_keys = category_info_dict.keys()
    cat_pairs_keys = category_pairs_dict.keys()
    ss_li_keys = shots_since_li_dict.keys()
    thomson_temp_keys = thomson_temp_dict.keys()
    for k in lifetimes_dict.keys():
        if k in cat_info_keys and k in ss_li_keys and lifetimes_dict[k] != '<N/C>' and k in thomson_temp_keys and k in cat_pairs_keys:
            lifetimes_array.append(lifetimes_dict[k])
            categories_array.append(category_info_dict[k])
            shots_since_li_array.append(shots_since_li_dict[k])
            thomson_temp_array.append(thomson_temp_dict[k])
            category_pairs_array.append(training_classifications['rise_classifications'][category_pairs_dict[k][0]] + " | " + training_classifications['fall_classifications'][category_pairs_dict[k][1]])
            hover_text_array.append(category_pairs_array[-1] + "\nShot:" + k)
            shots_array.append(int(k))
            if category_pairs_dict[k][0] in ['2']:
                is_dome.append(0)
            else:
                is_dome.append(1)

    scatter_info_dict = {
        "shots_array":shots_array,
        "categories_array":categories_array,
        "category_pairs_array":category_pairs_array,
        "is_dome_array":is_dome,
        "lifetimes_array":lifetimes_array,
        "shots_since_li_array":shots_since_li_array,
        "thomson_temp_array":thomson_temp_array,
        "hover_text_array":hover_text_array
    }

    return scatter_info_dict
















def get_total_shots_list(rise_data):
    all_shots = []
    for k in rise_data.keys():
        for s in rise_data[k]:
            if s not in all_shots:
                all_shots.append(s)
                
    return all_shots
    
    
    
def one_hot_categories(rise_keys, fall_keys):
    one_hot_dict = {}
    i = 0
    for r in rise_keys:
        for f in fall_keys:
            if (f == '4' and r != '4') or (r == '4' and f != '4'):
                continue
            else:
                one_hot_dict[r+f] = i
                i += 1

    return one_hot_dict