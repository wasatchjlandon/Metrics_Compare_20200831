# parse-metrics.py

Installation 
============
(Requires virtualenv (sudo pip install virtualenv). Better done off VPN.)
1. `make venv`
2. `source .venv-metrics/bin/activate`

## Inputs
>* Path to directory with data (see directory/data structure below).
>* SHREK sql query results as path to .csv. 
>* Output file path/name.csv.

###
Example Usage:
```
python parse-metrics.py /mnt/c/Users/willl/Downloads/data_comp_200827 /mnt/c/Users/willl/Downloads/on-prem_run_metrics_data_20200909.csv /mnt/c/Users/willl/Downloads/output.csv
```

### Directory structure (avoids renaming files by using a FC directory heirarchy):
```
/mnt/c/Users/willl/Downloads/data_comp_200827/
H575JBCX3  H73JWBCX3  H73KFBCX3  H73KGBCX3  H73KHBCX3
```
Each directory (i.e. H575JBCX3):

```
/mnt/c/Users/willl/Downloads/data_comp_200827/H575JBCX3
all_metrics.json
s_1_AACACGCT.dupe_metrics.txt
s_1_AACAGGTG.dupe_metrics.txt
s_1_AAGTGCAG.dupe_metrics.txt
s_1_AATTCCGG.dupe_metrics.txt
....
```
