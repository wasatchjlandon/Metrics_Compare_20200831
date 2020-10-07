import json
import sys
import csv
import pandas as pd
import glob

# function to get unique values 
def unique(list1): 
    # intilize a null list 
    unique_list = [] 
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x)
    return(unique_list)

#data_folder_path = sys.argv[1]
data_folder_path = '/mnt/c/Users/willl/Downloads/data_comp_200827'
data_folder_path_lst = glob.glob(data_folder_path + '/*')
#onprem_csv_path = sys.argv[2]
onprem_csv_path = '/mnt/c/Users/willl/Downloads/on-prem_run_metrics_data_20200909.csv'
#output_file = sys.argv[3]
output_file = '/mnt/c/Users/willl/Downloads/data_comp_200827/test20201006.csv'
##example usage:  python parse-metrics.py /mnt/c/Users/willl/Downloads/data_comp_200827 /mnt/c/Users/willl/Downloads/on-prem_run_metrics_data_20200909.csv /mnt/c/Users/willl/Downloads/test.csv
## exec(open('/home/wlandon/Projects/Metrics_Compare_20200831/parse-metrics.py').read())

#build data frame of *target_read_counts.csv - 1 per index set 
# Example: hiseq *_1_target_read_counts.csv is index set B
#          hiseq *_2_target_read_counts.csv is index set A
df = pd.DataFrame({})
FCs = [n[-9:] for n in data_folder_path_lst]
for i in data_folder_path_lst:
    n = data_folder_path_lst.index(i)
    data_subfolder_path_lst = glob.glob(data_folder_path_lst[n] + '/' + '*_target_read_counts.csv')
    for f in data_subfolder_path_lst:
        n2 = data_subfolder_path_lst.index(f)
        df1 = pd.read_csv(data_subfolder_path_lst[n2])
        df1 = df1.set_index('Unnamed: 0')
        df1 = df1.transpose()
        df1 = df1.reset_index()
        df1['barcode'] = df1['index'].str[4:]
        df1['recommended_name'] = FCs[n] + '_' + df1['barcode']
        df = pd.concat([df, df1])

#Calculate sum_target_reads. Reduce df to ['recommended_name', 'sum_target_reads'] 
df['sum_target_reads'] = df.sum(axis=1, skipna=True, numeric_only=True)
df = df.loc[:,['recommended_name', 'sum_target_reads']]

#make df of all_barcodes.htlm files
df_all = pd.DataFrame({})
for i in data_folder_path_lst:
    n = data_folder_path_lst.index(i)
    with open(data_folder_path_lst[n] + "/" + "all_barcodes.html") as fp:
        df1_lst = pd.read_html(fp)
    df1_all = df1_lst[2]
    df1_all['recommended_name'] = FCs[n] + '_' + df1_all['Barcode sequence']
    df_all = pd.concat([df_all, df1_all])
    df_all = df_all[df_all['Barcode sequence'] != 'unknown']

#sum lane 1 and 2 results
df_all = df_all.loc[:, ['Lane', 'PF Clusters', 'Yield (Mbases)', '% PFClusters', '% >= Q30bases', 'Mean QualityScore', 'recommended_name']]
aggregation_functions = {'Lane':'mean', 'PF Clusters':'sum', 'Yield (Mbases)':'sum', '% PFClusters':'mean', '% >= Q30bases':'mean', 'Mean QualityScore':'mean'}
df_all = df_all.groupby('recommended_name').aggregate(aggregation_functions)
df_all = df_all.reset_index()

#build dataframe of dupe_metrics
df_dupe = pd.DataFrame({})
for i in data_folder_path_lst:
    n = data_folder_path_lst.index(i)
    files1_lst = glob.glob(i + '/' + '*dupe_metrics.txt')
    for i2 in files1_lst:
        n2 = files1_lst.index(i2)
        df_dupe1 = pd.read_csv(files1_lst[n2], sep='\t', skiprows=6, nrows=1)
        df_dupe1['fc'] = FCs[n]
        df_dupe1['barcode'] = files1_lst[n2].split('/')[-1].split('.')[-3].split('_')[-1]
        df_dupe1['recommended_name'] = df_dupe1['fc'] + '_' + df_dupe1['barcode']
        df_dupe = pd.concat([df_dupe, df_dupe1])

# merge dataframes
df_final = df_all.merge(df, how='left', on='recommended_name')
df_final = df_final.merge(df_dupe, how='left', on='recommended_name')


# # onprem data
onprem_df = pd.read_csv(onprem_csv_path)
onprem_df['recommended_name'] = onprem_df['RUN_NAME'] + '_' + onprem_df['BARCODE']
onprem_df['old_mapping_efficiency'] = onprem_df['DUPLICATE_CLONES_DENOMINATOR'] / onprem_df['NUM_ELIGIBLE_READS']
onprem_df['old_clonality'] = onprem_df['DUPLICATE_CLONES_NUMERATOR'] / onprem_df['DUPLICATE_CLONES_DENOMINATOR']

#Merge cloud and onprem data
df_final = df_final.merge(onprem_df, how='left', on='recommended_name')
# df_final['match_count_2x'] = df_final['match_count']*2
# df_final['calc_num_mapped_clone_reads'] = df_final['match_count_2x'] - df_final['SECONDARY_OR_SUPPLEMENTARY_RDS'] - df_final['UNMAPPED_READS'] - df_final['UNPAIRED_READ_DUPLICATES'] - df_final['READ_PAIR_DUPLICATES']
# df_final['calc_mapping_efficiency'] = (df_final['calc_num_mapped_clone_reads'] + df_final['READ_PAIR_DUPLICATES']) / df_final['match_count_2x']

# prep final df and do mapped clone reads calculation
df_final_out = df_final.loc[:,['recommended_name', 'PF Clusters', 'Yield (Mbases)', '% PFClusters', '% >= Q30bases', 'Mean QualityScore', 'sum_target_reads', 'UNPAIRED_READS_EXAMINED',
                               'READ_PAIRS_EXAMINED', 'SECONDARY_OR_SUPPLEMENTARY_RDS', 'UNMAPPED_READS', 'UNPAIRED_READ_DUPLICATES', 'READ_PAIR_DUPLICATES', 
                               'READ_PAIR_OPTICAL_DUPLICATES', 'PERCENT_DUPLICATION', 'AUTO_COMMENTS', 'USER_COMMENTS', 'SEQ_STATUS', 'LR_STATUS', 'NUM_MAPPED_CLONE_READS','NUM_ELIGIBLE_READS', 
                               'TARGET_NUM_ALLELES_CV', 'DUPLICATE_CLONES_NUMERATOR', 'DUPLICATE_CLONES_DENOMINATOR', 'old_mapping_efficiency', 'old_clonality' ]]
df_final_out.to_csv(output_file)