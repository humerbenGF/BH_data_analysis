# import personal files
#################################################################
import plasma_data_and_parameters.internal_inductance.load_internal_inductance as load_int_ind
import plasma_data_and_parameters.particle_inventory.load_part_inventory as load_p_inv
import plasma_data_and_parameters.plasma_lifetime.save_plasma_lifetimes as load_p_lifetime
import plasma_data_and_parameters.poloidal_current.load_poloidal_current as load_pol_cur
import plasma_data_and_parameters.q_profile.load_q_min as load_q_min
import plasma_data_and_parameters.thomson.psi_thomson as psi_thomson
import plasma_data_and_parameters.toroidal_current.load_toroidal_current as load_tor_cur
import plasma_data_and_parameters.toroidal_spline_current.load_toroidal_spline_current as load_tor_spline_cur


# import personal files
#################################################################
def make_shot_list_edges(min_shot, max_shot):
    L = []
    while min_shot <= max_shot:
        L.append(min_shot)
        min_shot += 1

    return L

# main function for administrating data loading
#################################################################
if __name__ == '__main__':
    # generate shot list
    shot_list = make_shot_list_edges(19718, 23016)
    
    # decide what to load
    internal_inductance=    False
    particle_inventory=     True
    plasma_lifetime=        False
    poloidal_current=       False
    q_min=                  False
    thomson_psibar=         False
    toroidal_current=       False
    toroidal_spline_current=False
    
    # internal inductance
    if internal_inductance:
        load_int_ind.load_data_int_inductance_multishot(shot_list)
        
    # particle inventory
    if particle_inventory:
        load_p_inv.load_particle_inventory_multishot(shot_list)
        
    # plasma lifetime
    if plasma_lifetime:
        load_p_lifetime.save_lifetimes_dict()
        
    # poloidal current
    if poloidal_current:
        load_pol_cur.load_data_pol_current_multishot(shot_list)
    
    # q min
    if q_min:
        load_q_min.save_q_min_multishot(shot_list)
        
    # thomson psi
    if thomson_psibar:
        psi_thomson.get_thomson_psibar_values_multishot(shot_list)
        
    # toroidal current
    if toroidal_current:
        load_tor_cur.load_data_tor_current_multishot(shot_list)
        
    # toroidal spline current
    if toroidal_spline_current:
        load_tor_spline_cur.load_data_tor_spline_current_multishot(shot_list)