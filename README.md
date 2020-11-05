# parse-metrics_no_db_data.py

Installation 
============
(Requires virtualenv (sudo pip install virtualenv). Better done off VPN.)
1. `make venv`
2. `source .venv-metrics/bin/activate`

## Inputs
>* Path to directory with data (see directory/data structure below). 
>* Output file path/name.csv.

###
Example Usage:
```
python parse-metrics_no_db_data.py 
/mnt/c/Users/willl/Downloads/data_comp_200827 
/mnt/c/Users/willl/Downloads/output.csv
```

### Directory structure (avoids renaming files by using a FC directory heirarchy):
```
/mnt/c/Users/willl/Downloads/data_comp_200827/
H575JBCX3  H73JWBCX3  H73KFBCX3  H73KGBCX3  H73KHBCX3
```
Each directory (i.e. H575JBCX3):

```
/mnt/c/Users/willl/Downloads/data_comp_200827/H575JBCX3
201007_A01175_0109_BHNG3VDRXX_1_target_read_counts.csv
201007_A01175_0109_BHNG3VDRXX_2_target_read_counts.csv
201007_A01175_0109_BHNG3VDRXX_3_target_read_counts.csv
201007_A01175_0109_BHNG3VDRXX_4_target_read_counts.csv
all_barcodes.html
all_metrics.json
s_1_AACCGTTCTGAGCTAG.dupe_metrics.txt
s_1_AACGTCTGGCGTCATT.dupe_metrics.txt
s_1_AACTGAGCCCTGATTG.dupe_metrics.txt
s_1_AAGCACTGGTTGACCT.dupe_metrics.txt
s_1_ACAGCTCAGAGCAGTA.dupe_metrics.txt
....
```
