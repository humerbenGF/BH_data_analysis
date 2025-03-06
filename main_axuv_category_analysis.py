# add AURORA_REPOS to path
#################################################################
import os
import sys
sys.path.append(os.environ['AURORA_REPOS'])


# import files from analysis
#################################################################
import axuv_category_postprocessing.compare_to_manual as compare_data_to_manual_cat



if __name__ == '__main__':
    concavity_times = ['first_crash', 'biggest_crash', 'max_signal_amp']
    for i in range(len(concavity_times)):
        compare_data_to_manual_cat.compare_manual_dome_non_dome_to_parameter_concavity("axuv_category_datasets/manual_thomson_classification.json", "axuv_category_datasets/categorization_data.json", concavity_time=concavity_times[i])
    