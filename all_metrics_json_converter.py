import json
import sys
import csv
import pandas as pd
import glob


data_path = '/mnt/c/Users/willl/Downloads/RT_FC'
data_folder_path_lst = glob.glob(data_path + '/*')
output_file = '/mnt/c/Users/willl/Downloads/HNGJJDRXX_all_metrics_json_converted.csv'

df_json = pd.DataFrame({})
for i in data_folder_path_lst:
    n = data_folder_path_lst.index(i)
    df1_json = pd.read_json(data_folder_path_lst[n] + '/all_metrics.json', orient='index')
    df1_json = df1_json.drop(['low_coverage_regions', 'insert_size_histogram'], axis = 1)
    df_json = pd.concat([df_json, df1_json])
df_json = df_json.reset_index()
df_json = df_json.drop('index', axis=1)

df_json.to_csv(output_file)