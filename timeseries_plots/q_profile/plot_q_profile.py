# import packages
#################################################################
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import mplcursors


# import personal files
#################################################################
import plasma_data_and_parameters.q_profile.load_q_profile as load_q



def plot_q_profile(shotno, final_time=-1):
    '''
    final time is in ms
    '''
    quantity_array, err_array, psi = load_q.load_q_profile(shot_number=shotno)
    if final_time > 0:
        quantity_array = quantity_array[:final_time]
        err_array = err_array[:final_time]
    
    num_lines = len(quantity_array)
    
    # Create a colormap
    colormap = cm.get_cmap('gist_rainbow')
    colors = colormap(np.linspace(0, 1, num_lines))
    
    fig, ax = plt.subplots()
    lines = []  # Store the lines for mplcursors
    for i in range(len(quantity_array)):
        labelstring = str(i+1) + "ms"
        line, = ax.plot(psi, quantity_array[i], color=colors[i])
        ax.errorbar(psi, quantity_array[i], yerr=err_array[i], fmt="o", color=colors[i], label=labelstring)
        lines.append((line, i))  # Append the line and its index
    
    ax.set_title("Spatial Variance of Safety Factor\nShot " + str(shotno))
    ax.set_ylabel("q")
    ax.set_xlabel("Psi")
    ax.legend(ncol=int(num_lines/6))
    
    # Add interactive cursor
    cursor = mplcursors.cursor([line for line, _ in lines], hover=True)
    
    @cursor.connect("add")
    def on_add(sel):
        # Find the line and its index
        for line, curve_index in lines:
            if sel.artist == line:
                x, y = sel.target
                sel.annotation.set(text=f"t: {curve_index+1}ms\nPsi: {x:.2f}\nq: {y:.2f}")
                break
    
    plt.show()

    return