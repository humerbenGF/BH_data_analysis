# import personal files
#################################################################
from load_save_data.load_data import load_json_file
from SVD_bprobes import svd_multishot
from SVD.plot_SVD_axuv_ts import plot_axuv_SVD


if __name__ == '__main__':
    output_dir = "2024-11-26_SVD_similar"
    shots = [21096, 21101]
    
    # svd_multishot(shots, output_dir, True)
    # svd_multishot(shots, output_dir, False)

    output_dir = "2024-11-26_SVD_different"
    shots = [20216, 20272, 20528, 20901, 21295, 21343, 21792, 22254, 22255, 22356, 22417]

    # svd_multishot(shots, output_dir, True)
    # svd_multishot(shots, output_dir, False)
    
    plot_axuv_SVD(22255, output_dir)   