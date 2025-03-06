# import personal files
#################################################################
import plasma_data_and_parameters.J_profile.load_J_profile as load_J
import plasma_data_and_parameters.J_profile.load_J_min as load_J_min
import plasma_data_and_parameters.J_profile.load_J_max as load_J_max
import plasma_data_and_parameters.J_profile.load_J_05 as load_J_05


def make_shot_list_edges(min_shot, max_shot):
    L = []
    while min_shot <= max_shot:
        L.append(min_shot)
        min_shot += 1

    return L


if __name__ == '__main__':
    # shot = 21326
    shots_list = make_shot_list_edges(19718, 23016)
    crash_dir = "2024-10-10_19718-23016"
    # load_J_min.save_J_min_multishot(shots_list)
    # load_J_max.save_J_max_multishot(shots_list)
    load_J_05.save_J_05_multishot(shots_list)
    # load_J_max.save_J_max_multishot([19976])
    # J_profile_multitime, J_profile_multitime_errors, J_profile_multitime_psibar = load_J.load_J_profile(19976)
    # print(J_profile_multitime)