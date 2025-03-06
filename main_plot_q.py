# import personal files
#################################################################
import plasma_data_and_parameters.q_profile.load_q_min as load_q_min
import timeseries_plots.axuv_ts_q_min.plot_axuv_q_min_ts as plot_axuv_q
import timeseries_plots.current_timeseries.plot_current_timeseries as plot_current_q
import axuv_crash_postprocessing.q.crash_q_scatter as crash_q_scatter
import axuv_crash_postprocessing.q.crash_q_over_psibar as crash_q_psi
import axuv_crash_postprocessing.q.crash_q_dq_over_t_since_crash as crash_q_scatter_t_since_crash


def make_shot_list_edges(min_shot, max_shot):
    L = []
    while min_shot <= max_shot:
        L.append(min_shot)
        min_shot += 1

    return L


if __name__ == '__main__':
    shot = 21326
    crash_dir = "2024-10-10_19718-23016"
    # load_q_min.load_q_min_array(21326)
    # plot_current_q.plot_current_ratio_axuv_timeseries_q(shot)
    # plot_axuv_q.plot_axuv_q_min(shot)
    # plot_axuv_q.plot_q_min_current(shot)
    
    
    # shots_list = make_shot_list_edges(19718, 23016)
    # load_q_min.save_q_min_multishot(shots_list)
    
    # crash_q_scatter.plot_q_scatter_crashes("2024-10-10_19718-23016", min_lifetime=0.02, only_largest_crash=False, end_exclusion=10, plot_means=True, matplotlib=False, plotly=True)
    crash_q_psi.plot_q_over_psibar_all_crashes(crash_dir, 20681)
    # crash_q_scatter_t_since_crash.plot_dq_over_t_since_crash(crash_dir, 'min', 1, 2, 20)