import json
import sys
import csv
import pandas as pd
import glob

#sample='/mnt/c/Users/willl/Downloads/data_comp_200827/H73JNBCX3/all_metrics.json'
#sample = sys.argv[1]
output_file = 'metrics.csv'
data_folder_path_lst = glob.glob('/mnt/c/Users/willl/Downloads/data_comp_200827/*')
onprem_csv_path = '/mnt/c/Users/willl/Downloads/20200831_3.csv'

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

# build dataframe of all_sample_barcode_metrics
df_bcm = pd.DataFrame({})
for i in data_folder_path_lst:
    n = data_folder_path_lst.index(i)
    df_bcm1 = pd.read_json(data_folder_path_lst[n] + '/all_sample_barcode_metrics.json', orient='index')
    df_bcm1['fc'] = FCs[n]
    df_bcm1['recommended_name'] = df_bcm1['fc'] + '_' + df_bcm1['barcode']
    df_bcm = pd.concat([df_bcm, df_bcm1])

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
df_final = df.merge(df_bcm, how='left', on='recommended_name', suffixes=('_all_met_json', '_all_sample_bc_metrics_json'))
df_final = df_final.merge(df_dupe, how='left', on='recommended_name')

# onprem data
onprem_df = pd.read_csv(onprem_csv_path)
onprem_df['recommended_name'] = onprem_df['RUN_NAME'] + '_' + onprem_df['BARCODE']
onprem_df['onprem_mapping_efficiency'] = onprem_df['DUPLICATE_CLONES_DENOMINATOR'] / onprem_df['NUM_ELIGIBLE_READS']
onprem_df['onprem_clonality'] = onprem_df['DUPLICATE_CLONES_NUMERATOR'] / onprem_df['DUPLICATE_CLONES_DENOMINATOR']
df_final = df_final.merge(onprem_df, how='left', on='recommended_name')
df_final['match_count_2x'] = df_final['match_count_all_met_json']*2
df_final['calc_num_mapped_clone_reads'] = df_final['match_count_2x'] - df_final['SECONDARY_OR_SUPPLEMENTARY_RDS'] - df_final['UNMAPPED_READS'] - df_final['UNPAIRED_READ_DUPLICATES'] - df_final['READ_PAIR_DUPLICATES']
df_final['calc_mapping_efficiency'] = (df_final['calc_num_mapped_clone_reads'] + df_final['READ_PAIR_DUPLICATES']) / df_final['match_count_2x']

# prep final df and do mapped clone reads calculation
df_final_out = df_final.loc[:,['recommended_name', 'NUM_MAPPED_CLONE_READS', 'NUM_ELIGIBLE_READS', 'DUPLICATE_CLONES_NUMERATOR','DUPLICATE_CLONES_DENOMINATOR',
                               'onprem_mapping_efficiency', 'onprem_clonality','calc_mapping_efficiency', 'calc_num_mapped_clone_reads',
                               'READ_PAIRS_EXAMINED','UNMAPPED_READS', 'PERCENT_DUPLICATION',
                               'contamination_log_likelihood_0', 'contamination_log_likelihood_max',
                               'contamination_snp_count', 'contamination_estimate', 'contamination_log_likelihood_ratio',
                               'SECONDARY_OR_SUPPLEMENTARY_RDS',  'UNPAIRED_READ_DUPLICATES', 'READ_PAIR_DUPLICATES',
                               'RUN_SAMPLE_ID', 'AUTO_COMMENTS', 'USER_COMMENTS',
                               'TARGET_NUM_ALLELES_CV', 'MEDIAN_LR_MAPPED_CLONE_READS',
                               'ACCESSION_ID'
                               ]]

df_final_out.to_csv('/mnt/c/Users/willl/Downloads/test_20200831.csv')

