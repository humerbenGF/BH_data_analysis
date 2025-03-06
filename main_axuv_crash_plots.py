import axuv_crash_postprocessing.crash_scatter as crash_scatter
import axuv_crash_postprocessing.crash_histogram as histogram
import axuv_crash_postprocessing.thomson.crash_thomson_scatter as thomson
import axuv_crash_postprocessing.current_ratio.crash_current_ratio_scatter as cur_ratio
import axuv_crash_postprocessing.particle_inventory.crash_particle_inventory_scatter as part_invent
import axuv_crash_postprocessing.axuv_Te.crash_axuv_Te_scatter as axuv_Te_scatter
import axuv_crash_postprocessing.kinetic_energy.kinetic_energy_scatter as KE_scatter
import axuv_crash_postprocessing.q.crash_q_scatter as q_scatter
import axuv_crash_postprocessing.li1.plot_dq_dp_colored_by_li1 as q_scatter_li1
import axuv_crash_postprocessing.thomson.crash_thomson_core_vs_edge as thomson_core_edge
import axuv_crash_postprocessing.J.crash_J_scatter as J_scatter
import axuv_crash_postprocessing.thomson.gen_thomson_psibar_slope as gen_thomson_psibar_slope
import axuv_crash_postprocessing.ss_li.plot_dq_dp_colored_by_ssli as q_scatter_ssli


if __name__ == '__main__':
    output_dir = "axuv_crash_datasets/2025-02-14_19718-23064"
    
    # histograms
    ##################################################################################################################################
    # histogram.make_hist_num_crashes(output_dir)
    # histogram.make_hist_num_crashes_sustain_non_sustain(output_dir, savefig=True)
    # histogram.make_hist_times_crashes_sustain_non_sustain(output_dir, True)
    # histogram.make_hist_time_nth_crash_sustain_non_sustain(output_dir, 1, True)
    # histogram.make_KDE_time_nth_crash_sustain_non_sustain(output_dir, 1, True)
    
    # old analysis
    ##################################################################################################################################
    # crash_scatter.scatter_shots_since_li_num_crashes(output_dir)
    # crash_scatter.scatter_lifetime_amp_largest_crash(output_dir)
    # cur_ratio.scatter_current_ratio_amplitude(output_dir)
    # cur_ratio.hist_current_ratio(output_dir)
    
    # thomson
    ##################################################################################################################################
    # thomson.thomson_phase_plot(output_dir)
    # thomson.plot_psi_phase_900(output_dir, '730', False, True)
    # thomson.plot_temp_phase_for_shotlist(output_dir, '600', True)
    
    # thomson.plot_temp_phase_for_shotlist_cut_between_crashes_plotly(output_dir, '600')
    # thomson.plot_temp_phase_for_shotlist_cut_between_crashes_plotly(output_dir, '730')
    # thomson.plot_temp_phase_for_shotlist_cut_between_crashes_plotly(output_dir, '900')
    
    # thomson.plot_temp_phase_for_shotlist_spanning_crashes_plotly(output_dir, '600')
    # thomson.plot_temp_phase_for_shotlist_spanning_crashes_plotly(output_dir, '730')
    # thomson.plot_temp_phase_for_shotlist_spanning_crashes_plotly(output_dir, '900')
    
    # thomson.plot_temp_phase_for_shotlist_going_over_crashes_plotly(output_dir, '600', Tmin=0, multitime_only=True)
    # thomson.plot_temp_phase_for_shotlist_going_over_crashes_plotly(output_dir, '730', Tmin=0, multitime_only=True)
    # thomson.plot_temp_phase_for_shotlist_going_over_crashes_plotly(output_dir, '900', Tmin=0, multitime_only=True)
    
    # thomson.reconstruct_temp_change_over_phase(output_dir, '600', 250, 20, min_num_crashes=2, matplotlib=False, plotly=True)
    # thomson.reconstruct_temp_change_over_phase(output_dir, '730', 250, 20, min_num_crashes=2, matplotlib=False, plotly=True)
    # thomson.reconstruct_temp_change_over_phase(output_dir, '900', 250, 20, min_num_crashes=2, matplotlib=False, plotly=True)
        
    # for i in range(7):
    #     print(f"GENERATING PLOTS FOR {i} CRASHES")
    #     thomson.reconstruct_temp_change_over_phase_single_num_crashes(output_dir, '600', 250, 20, num_crashes=i, matplotlib=False, plotly=True)
    #     thomson.reconstruct_temp_change_over_phase_single_num_crashes(output_dir, '730', 250, 20, num_crashes=i, matplotlib=False, plotly=True)
    #     thomson.reconstruct_temp_change_over_phase_single_num_crashes(output_dir, '900', 250, 20, num_crashes=i, matplotlib=False, plotly=True)
    #     print()
    # thomson.reconstruct_temp_change_over_phase_single_num_crashes(output_dir, '600', 250, 20, num_crashes=3, matplotlib=False, plotly=True, show_plotly=True)


    # thomson core edge
    ##################################################################################################################################
    # thomson_core_edge.scatter_core_edge_temp(output_dir)
    # thomson_core_edge.scatter_core_edge_slope_over_phase(output_dir, 50)

    
    # particle inventory
    ##################################################################################################################################
    # part_invent.particle_inventory_over_phase_scatter(output_dir, 0.1, matplotlib=False, plotly=True)
    # for i in range(7):
    #     part_invent.particle_inventory_over_phase_scatter_single_num_crashes(output_dir, 0.1, i, 5*10**21, matplotlib=False, plotly=True)
    # for i in range(7):
    #     part_invent.particle_inventory_over_normalized_time_scatter_single_num_crashes(output_dir, 0.05, i, 5*10**21, matplotlib=False, plotly=True)
    # for i in range(7):
    #     part_invent.reconstruct_particle_inventory_over_phase_single_num_crashes(output_dir, 250, 20, num_crashes=i, matplotlib=False, plotly=True)
    # part_invent.reconstruct_particle_inventory_over_phase_single_num_crashes(output_dir, 250, 20, num_crashes=2, matplotlib=False, plotly=True)
    
    # axuv Te
    ##################################################################################################################################
    # axuv_Te_scatter.dT_crash_amp_over_crashes(output_dir, 0)
    
    # energy content
    ##################################################################################################################################
    # for i in range(7):
    #     KE_scatter.reconstruct_plasma_kinetic_energy_over_phase_single_num_crashes(output_dir, '600', 250, num_crashes=i, matplotlib=False, plotly=True, show_plotly=False)
    #     KE_scatter.reconstruct_plasma_kinetic_energy_over_phase_single_num_crashes(output_dir, '730', 250, num_crashes=i, matplotlib=False, plotly=True, show_plotly=False)
    #     KE_scatter.reconstruct_plasma_kinetic_energy_over_phase_single_num_crashes(output_dir, '900', 250, num_crashes=i, matplotlib=False, plotly=True, show_plotly=False)
    
    
    # sustain and non-sustain thomson
    ##################################################################################################################################
    # thomson.reconstruct_temp_change_over_phase_crash_range_sustain_non_sustain(output_dir, '600', 50, min_crashes=2, max_crashes=8, matplotlib=False, plotly=True, scatter_plotly=True)
    # thomson.reconstruct_temp_change_over_phase_crash_range_sustain_non_sustain(output_dir, '730', 50, min_crashes=2, max_crashes=8, matplotlib=False, plotly=True, scatter_plotly=True)
    # thomson.reconstruct_temp_change_over_phase_crash_range_sustain_non_sustain(output_dir, '900', 50, min_crashes=2, max_crashes=8, matplotlib=False, plotly=True, scatter_plotly=True)
    
    
    # q at a single point for each time in reconstruction
    ##################################################################################################################################
    for i in ['min', '95', '00']:
        # q_scatter.reconstruct_q_change_over_phase_crash_range_sustain_non_sustain(output_dir, 50, i, 2, 5, False, True, True)
        # q_scatter.reconstruct_q_change_over_norm_time_crash_range_sustain_non_sustain(output_dir, 50, i, 2, 5, False, True, True)
        # q_scatter.reconstruct_q_change_over_phase_without_last_half_cycle_crash_range_sustain_non_sustain(output_dir, 50, i, 2, 5, False, True, True)
        # for j in range(6):
        #     q_scatter.reconstruct_q_change_over_phase_without_last_half_cycle_num_crashes_sustain_non_sustain(output_dir, 50, j, i, False)
        # q_scatter_li1.q_change_over_phase_colored_by_li1_sustain_only(output_dir, 50, 2, 10, i, True)
        q_scatter_ssli.q_change_over_phase_colored_by_ssli_sustain_only(output_dir, 50, 2, 10, i, True)
        
    # q_scatter.reconstruct_q_change_over_phase_crash_range_sustain_non_sustain(output_dir, 50, '00', 2, 5, False, True, True)
    # q_scatter.reconstruct_q_change_over_norm_time_crash_range_sustain_non_sustain(output_dir, 50, '95', 2, 5, True)
    
    
    # J at a single point for each time in reconstruction
    ##################################################################################################################################
    # for i in ['min', 'max', '05']:
    #     J_scatter.reconstruct_J_change_over_phase_without_last_half_cycle_nums_crashes_sustain_non_sustain(output_dir, 50, [0,1,2,3,4,5], J_psibar=i, show_plotly=True)
    
    # thomson psibar profile
    ##################################################################################################################################
    # gen_thomson_psibar_slope.generate_thomson_psibar_slope_multishot(output_dir)
    # for i in ['600_730', '600_900', '730_900', 'best_fit']:
    #     thomson_core_edge.plot_multishot_core_edge_slopes_sustain_non_sustain(output_dir, slope_type=i, matplotlib=False, plotly=True, show_plotly=True)