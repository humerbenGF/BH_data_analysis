# add AURORA_REPOS to path
#################################################################
import os
import sys
sys.path.append(os.environ['AURORA_REPOS'])


# import functions from AXUV_crash_detection
#################################################################
from AXUV_crash_detection import id_axuv_crashes                # type: ignore
from AXUV_crash_detection import load_axuv_crash_data           # type: ignore
from AXUV_crash_detection import axuv_crash_shot_info           # type: ignore
from AXUV_crash_detection import axuv_crash_postprocessing      # type: ignore



if __name__ == '__main__':
    output_dir = "preprocessed_data/AXUV-crashes_2024-09-03_1"
    shot_list = load_axuv_crash_data.load_shots_list(output_dir)
    axuv_crash_postprocessing.group_crashes_multishot(shot_list, output_dir)