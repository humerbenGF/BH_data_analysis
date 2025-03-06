# import functions from AXUV_crash_detection
#################################################################
import AXUV_crash_detection as crash_det


def make_shot_list_edges(min_shot, max_shot):
    L = []
    while min_shot <= max_shot:
        L.append(min_shot)
        min_shot += 1

    return L



if __name__ == '__main__':
    # shots_list = [22180, 21176, 20506, 22289, 21111]
    # shots list for abi
    # shots_list = [21086, 21087, 21088, 21089, 21090, 21091, 21092, 21095, 21096, 21097, 21099, 21100, 21101, 21102, 21103, 21104, 21105, 21106, 21107, 21113, 21114, 21116, 21117, 21118, 21119, 21123, 21127, 21128, 21129, 21130, 21133, 21193, 21194, 21301, 21302, 21303, 21310, 21312, 21313, 21314, 21316, 21317, 21318, 21331, 21356, 21359, 21360, 21361, 21367, 21368, 21369, 21370, 21371, 21373, 21374, 21375, 21376, 21377, 21379, 21380, 21381, 21382, 21383, 21393, 21394, 21396, 21397, 21398, 21399, 21400, 21419, 21420, 21421, 21422, 21423, 21426, 21427, 21428, 21432, 21440, 21442, 21447, 21448, 21449, 21450, 21451, 21460, 21463]
    # stephen shots
    # shots_list = [22228,22229,22230,22232,22233,22286,22292,22481,22497,22626,22631,22656,22657,22662,22663,22664,22665,22666,22669,22670,22678,22680,22695,22696,22697,22698,22699,22708,22712,22713,22714,22715,22716,22717,22718,22726,22727,22728,22729,22730,22733,22734,22735,22736,22737,22743,22745,22746,22747,22751,22752,22753,22754,22755,22787,22804,22805,22807,22808,22809,22824,22973,22990]
    
    # shots_list = make_shot_list_edges(19718, 23016)
    
    # load_axuv_crash_data.load_save_raw_timeseries(shots_list)
    
    # output_dir = "2024-10-10_abi"
    # id_axuv_crashes_conv.id_crashes_multishot_conv(output_dir, shots_list)
    
    # output_dir = "2024-10-02_19718-23016"
    
    # output_dir = '2024-10-25_abi'
    # shots_list = [21366, 22180]
    
    output_dir = "2024-11-26_AXUV_similar"
    shots_list = [21096, 21101]
    
    output_dir = "2024-11-26_AXUV_different"
    shots_list = [20216, 20272, 20528, 20901, 21295, 21343, 21792, 22254, 22255, 22356, 22417]
    
    output_dir = "axuv_crash_datasets/2025-02-14_19718-23064"
    shots_list = make_shot_list_edges(19718, 23064)
    
    
    # crash_det.gen_rawdata(shots_list)
    # crash_det.id_crashes(output_dir, shots_list)
    crash_det.gen_crash_phase(output_dir, shots_list)
    crash_det.proc_hardware_errors(output_dir)