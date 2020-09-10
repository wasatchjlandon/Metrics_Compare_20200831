# parse-metrics.py

## Inputs
>* directory structure with data (see below).
>* SHREK sql query results as path to .csv. Define `onprem_csv_path` variable.

### Directory structure (avoids renaming files by using a FC directory heirarchy):
```
/mnt/c/Users/willl/Downloads/data_comp_200827/
H575JBCX3  H73JWBCX3  H73KFBCX3  H73KGBCX3  H73KHBCX3
```
Each directory (i.e. H575JBCX3):

```
/mnt/c/Users/willl/Downloads/data_comp_200827/H575JBCX3
all_metrics.json
all_sample_barcode_metrics.json
s_1_AACACGCT.dupe_metrics.txt
s_1_AACAGGTG.dupe_metrics.txt
s_1_AAGTGCAG.dupe_metrics.txt
s_1_AATTCCGG.dupe_metrics.txt
....
```
