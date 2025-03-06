# import libraries
#################################################################
import matplotlib.pyplot as plt
import numpy as np


# import personal files
#################################################################
# import thomson.load_thomson as load_thomson
# import shot_settings_info.convert_csv_to_json as convert_to_json
# import axuv_categories_analysis.aps_scatter.make_training_data_thomson as gen_thomson_categories
import axuv_crash_postprocessing.crash_scatter as crash_scatter
import machine_settings_and_state.convert_csv_to_json as convert_to_json
import machine_settings_and_state.control_settings.load_control_settings as control_settings
import plasma_data_and_parameters.thomson.psi_thomson as psi_thomson
import plasma_data_and_parameters.internal_inductance.load_internal_inductance as load_inductance
import plasma_data_and_parameters.poloidal_current.load_poloidal_current as load_pol_cur
import plasma_data_and_parameters.toroidal_current.load_toroidal_current as load_tor_cur
import plasma_data_and_parameters.toroidal_spline_current.load_toroidal_spline_current as load_tor_spline_cur
import axuv_crash_postprocessing.current_ratio.calculate_current_ratio_crashes as crash_current_ratio
import plasma_data_and_parameters.particle_inventory.load_part_inventory as lpi
import axuv_crash_postprocessing.thomson.crash_thomson_load_data as load_thomson
import axuv_crash_postprocessing.thomson.crash_thomson_data_filters as thomson_filter
import axuv_crash_postprocessing.li1.plot_dli1_over_li1 as plot_li1

def make_shot_list_edges(min_shot, max_shot):
    L = []
    while min_shot <= max_shot:
        L.append(min_shot)
        min_shot += 1

    return L



if __name__ == '__main__':
    # convert_to_json.convert_sustainment()
    # gen_thomson_categories.make_training_data_thompson()
    # crash_scatter.scatter_lifetime_num_crashes("2024-09-30_19718-23016")
    # crash_scatter.scatter_shots_since_li_num_crashes("2024-09-30_19718-23016")
    # crash_scatter.scatter_lifetime_amp_largest_crash("2024-10-02_19718-23016")
    # convert_to_json.convert_shots_since_li()
    # convert_to_json.convert_timestamps()
    # convert_to_json.convert_shots_since()
    
    
    shots_list = make_shot_list_edges(19718, 23016)
    crash_dir = "2024-10-10_19718-23016"
    # control_settings.load_control_settings_json(shots_list)
    # control_settings.load_control_settings_json([20681])
    # psi_thomson.get_thomson_psibar_values_multishot(shots_list)
    # load_thomson.load_thomson_phase_data_by_shot(crash_dir, True, True, True, True, True)
    
    # load_inductance.load_data_int_inductance_multishot(shots_list)
    # load_pol_cur.load_data_pol_current_multishot(shots_list)
    # load_tor_cur.load_data_tor_current_multishot(shots_list)
    # load_tor_spline_cur.load_data_tor_spline_current_multishot(shots_list)
    # crash_current_ratio.calculate_current_ratio_crashes(crash_dir)
    
    # data = load_inductance.load_data_int_inductance_singleshot(21087)
    # x = np.linspace(1/1000, len(data['data'])/1000, len(data['data']))
    # print(x)
    # print(data)
    
    # plt.plot(x, data['data'])
    # # plt.errorbar(x, data['data'], yerr=data['errors'])
    # plt.show()
    
    # lpi.load_particle_inventory_multishot(shots_list)
    
    # data_dict_by_shot = load_thomson.load_thomson_phase_data_by_shot(crash_dir, True, True, True, True)
    # thomson_filter.get_slope_at_phase_by_shot(data_dict_by_shot, '600', 0.4, True)
    crash_dir = "axuv_crash_datasets/2025-02-14_19718-23064"
    min, max = 0.4, 1.5
    spread = 0.2
    num_slices = 0
    for i in range(num_slices):
        li1_min = min + i/(num_slices+2)*(max-min)
        li1_max=li1_min+spread
        plot_li1.plot_dli1_li1_2D_density_only_crashes(crash_dir, li1_min, li1_max)
    
    plot_li1.plot_dli1_li1_2D_density_only_crashes(crash_dir, kde=False)