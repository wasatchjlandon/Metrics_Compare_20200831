import json
import sys
import csv
import pandas as pd
import glob
import numpy as np

#RUN FROM PYTHON SHELL:  exec(open('/home/wlandon/Projects/Metrics_Compare_20200831/parse-metrics_downstream.py').read())

from bs4 import BeautifulSoup

# with open("/mnt/c/Users/willl/Downloads/all_barcodes.html") as fp:
#     soup = BeautifulSoup(fp)

#soup = BeautifulSoup("<html>a web page</html>", 'html.parser')

with open("/mnt/c/Users/willl/Downloads/all_barcodes.html") as fp:
    df = pd.read_html(fp)



# parse_metrics_output_file = '/mnt/c/Users/willl/Downloads/Clonality_MappingEff/parse-metrics_output_20200919.csv'
# df = pd.read_csv(parse_metrics_output_file)
# df['new_mapping_efficiency'] = (df['NUM_MAPPED_CLONE_READS'] + df['READ_PAIR_DUPLICATES']) / (df['match_count']*2)
# df['old_clonality'] = df['DUPLICATE_CLONES_NUMERATOR'] / df['DUPLICATE_CLONES_DENOMINATOR']
# df['old_mapping_efficiency'] = df['DUPLICATE_CLONES_DENOMINATOR'] / df['NUM_ELIGIBLE_READS']
# df['flowcell'] = df['recommended_name'].str[:9]

# df2 = df.loc[:,['match_count', 'mapped_reads', 'PERCENT_DUPLICATION', 'new_mapping_efficiency', 'old_clonality', 'old_mapping_efficiency', 'flowcell',
#                 'NUM_MAPPED_CLONE_READS', 'NUM_ELIGIBLE_READS', 'DUPLICATE_CLONES_NUMERATOR', 'DUPLICATE_CLONES_DENOMINATOR']]

# df2_p = pd.pivot_table(df2, index='flowcell', aggfunc=['mean', 'median', 'min', 'max', np.std])
# df3 = df2[df2['flowcell'] != 'H73KFBCX3']
# df3_corr= df3.corr(method='pearson')

# df2_p.to_csv('/mnt/c/Users/willl/Downloads/test____.csv')
# df3_corr.to_csv('/mnt/c/Users/willl/Downloads/test____1.csv')