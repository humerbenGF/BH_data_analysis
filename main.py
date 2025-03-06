# import personal files
#################################################################
import axuv_crash_postprocessing.q.crash_q_over_psibar as crash_q_psi
import axuv_crash_postprocessing.J.crash_J_over_psibar as crash_J_psi
import axuv_crash_postprocessing.thomson.crash_thomson_core_vs_edge as crash_thomson
import timeseries_plots.axuv_ts.axuv_raw_ts as axuv_ts_plot

def make_shot_list_edges(min_shot, max_shot):
    L = []
    while min_shot <= max_shot:
        L.append(min_shot)
        min_shot += 1

    return L


if __name__ == '__main__':
    crash_data_dir = "axuv_crash_data/2024-10-10_19718-23016"
    # crash_q_psi.plot_q_over_psibar_all_crashes(crash_data_dir, 20317)
    # crash_J_psi.plot_J_over_psibar_all_crashes("2024-10-10_19718-23016", 21441)
    # crash_thomson.plot_multitime_thomson_core_edge_singleshot(crash_data_dir, 22221)
    # crash_thomson.plot_multishot_core_edge_slopes(crash_data_dir, 'best_fit')
    # crash_thomson.plot_multishot_core_edge_slopes_sustain_non_sustain(crash_data_dir, 'best_fit', False, True, True)
    axuv_ts_plot.plot_axuv_ts(20427, ['sn024'])