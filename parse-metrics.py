import json
import sys
import csv
import pandas as pd
import glob

data_folder_path = sys.argv[1]
#data_folder_path = '/mnt/c/Users/willl/Downloads/data_comp_200827'
data_folder_path_lst = glob.glob(data_folder_path + '/*')
onprem_csv_path = sys.argv[2]
#onprem_csv_path = '/mnt/c/Users/willl/Downloads/on-prem_run_metrics_data_20200909.csv'
output_file = sys.argv[3]
#output_file = '/mnt/c/Users/willl/Downloads/data_comp_200827/test.csv'
##example usage:  python parse-metrics.py /mnt/c/Users/willl/Downloads/data_comp_200827 /mnt/c/Users/willl/Downloads/on-prem_run_metrics_data_20200909.csv /mnt/c/Users/willl/Downloads/test.csv

#build data frame of all_metrics.json
df = pd.DataFrame({})
FCs = [n[-9:] for n in data_folder_path_lst]
for i in data_folder_path_lst:
    n = data_folder_path_lst.index(i)
    df1 = pd.read_json(data_folder_path_lst[n] + '/all_metrics.json', orient='index')
    df1 = df1.drop(['low_coverage_regions', 'insert_size_histogram'], axis = 1)
    df1['fc'] = FCs[n]
    df1['recommended_name'] = df1['fc'] + '_' + df1['barcode']
    df = pd.concat([df, df1])
df = df.reset_index()
df = df.drop('index', axis=1)

# # build dataframe of all_sample_barcode_metrics - not needed - because all information in sample_barcode_metrics is also in all_metrics.json
# df_bcm = pd.DataFrame({})
# for i in data_folder_path_lst:
#     n = data_folder_path_lst.index(i)
#     df_bcm1 = pd.read_json(data_folder_path_lst[n] + '/all_sample_barcode_metrics.json', orient='index')
#     df_bcm1['fc'] = FCs[n]
#     df_bcm1['recommended_name'] = df_bcm1['fc'] + '_' + df_bcm1['barcode']
#     df_bcm = pd.concat([df_bcm, df_bcm1])
#build dataframe of dupe_metrics

df_dupe = pd.DataFrame({})
for i in data_folder_path_lst:
    n = data_folder_path_lst.index(i)
    files1_lst = glob.glob(i + '/' + '*dupe_metrics.txt')
    for i2 in files1_lst:
        n2 = files1_lst.index(i2)
        df_dupe1 = pd.read_csv(files1_lst[n2], sep='\t', skiprows=6, nrows=1)
        df_dupe1['fc'] = FCs[n]
        df_dupe1['barcode'] = files1_lst[n2][-25:-17]
        df_dupe1['recommended_name'] = df_dupe1['fc'] + '_' + df_dupe1['barcode']
        df_dupe = pd.concat([df_dupe, df_dupe1])

# merge dataframes
#df_final = df.merge(df_bcm, how='left', on='recommended_name', suffixes=('_all_met_json', '_all_sample_bc_metrics_json'))
df_final = df.merge(df_dupe, how='left', on='recommended_name')


# onprem data
onprem_df = pd.read_csv(onprem_csv_path)
onprem_df['recommended_name'] = onprem_df['RUN_NAME'] + '_' + onprem_df['BARCODE']
#onprem_df['onprem_mapping_efficiency'] = onprem_df['DUPLICATE_CLONES_DENOMINATOR'] / onprem_df['NUM_ELIGIBLE_READS']
#onprem_df['onprem_clonality'] = onprem_df['DUPLICATE_CLONES_NUMERATOR'] / onprem_df['DUPLICATE_CLONES_DENOMINATOR']

#Merge cloud and onprem data
df_final = df_final.merge(onprem_df, how='left', on='recommended_name')
# df_final['match_count_2x'] = df_final['match_count']*2
# df_final['calc_num_mapped_clone_reads'] = df_final['match_count_2x'] - df_final['SECONDARY_OR_SUPPLEMENTARY_RDS'] - df_final['UNMAPPED_READS'] - df_final['UNPAIRED_READ_DUPLICATES'] - df_final['READ_PAIR_DUPLICATES']
# df_final['calc_mapping_efficiency'] = (df_final['calc_num_mapped_clone_reads'] + df_final['READ_PAIR_DUPLICATES']) / df_final['match_count_2x']

# prep final df and do mapped clone reads calculation
df_final_out = df_final.loc[:,['match_count', 'sample', 'mapped_reads', 'UNPAIRED_READS_EXAMINED', 'READ_PAIRS_EXAMINED', 'SECONDARY_OR_SUPPLEMENTARY_RDS', 'UNMAPPED_READS',
                               'UNPAIRED_READ_DUPLICATES', 'READ_PAIR_DUPLICATES', 'READ_PAIR_OPTICAL_DUPLICATES', 'PERCENT_DUPLICATION',
                               'recommended_name', 'AVG_NUM_FORWARD_READS', 'AVG_NUM_REVERSE_READS', 'AVG_NUM_CLONE_READS',
                               'NUM_MAPPED_CLONE_READS', 'NUM_MAPPED_FORWARD_READS', 'NUM_MAPPED_REVERSE_READS', 'NUM_ELIGIBLE_READS',
                               'TARGET_NUM_ALLELES_CV', 'DUPLICATE_CLONES_NUMERATOR', 'DUPLICATE_CLONES_DENOMINATOR']]


df_final_out.to_csv(output_file)

