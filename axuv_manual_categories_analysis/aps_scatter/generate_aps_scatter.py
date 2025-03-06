import axuv_categories_analysis.aps_scatter.plot_axuv_timeseries as plot_timeseries
import axuv_categories_analysis.aps_scatter.aps_scatter_plot as aps_scatter
import axuv_categories_analysis.aps_scatter.aps_timeseries as aps_timeseries



if __name__ == "__main__":
    # sustain_shots = [22700, 22677, 22719, 22738, 22703, 22603]
    # non_sustain_shots = [22657, 22680, 22694, 22695, 22696, 22697, 22714, 22718, 22745, 22805]

    # for shot in non_sustain_shots:
    #     plot_timeseries.plot_axuv_timeseries(shot)
    
    # aps_scatter.aps_scatter_poster(make_html_plot=True, showfig=False)
    # aps_timeseries.plot_timeseries_average(normalize=False, lifetime_stretching=True, threshold=0.3, plot_averages=False, shots_of_interest=[22703, 22719, 22603, 22677, 20342, 20506, 20522])
    # aps_timeseries.plot_timeseries_average(normalize=False, lifetime_stretching=True, threshold=0.3, plot_averages=False)
    shots_of_interest_list = [22703, 22719, 22738, 22714, 22696, 22718, 22745, 22657, 22697, 22677, 22603, 22694, 22805, 20506, 20342, 21284, 20604, 20579, 20662]
    # aps_timeseries.plot_timeseries_average(normalize=True, lifetime_stretching=True, threshold=0.3, plot_averages=False, shots_of_interest=shots_of_interest_list)
    aps_timeseries.plot_timeseries_average(normalize=True, lifetime_stretching=True, threshold=0.3, plot_averages=False, shots_of_interest=[20506, 20604, 20579, 22714, 22718, 22696])