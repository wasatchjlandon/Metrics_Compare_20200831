# Add metrics for mapping efficiency and clonality.
 ## MPD-115
 Ticket:
 >* https://mygn.atlassian.net/browse/MPD-115?atlOrigin=eyJpIjoiYWI4NDY5YTM4Y2U2NGE4NGI1NzQzZWI5MDY3OGQzMWMiLCJwIjoiaiJ9
 
 The goal is to identify metrics that can be used for analogs/substitutes/surrogates of the legacy metrics:  mapping efficiency and clonality .

 Tech dev archive and write-up here (update with techdev path):
>* W:\MGL\Technology Development\PROJECT_DEVEL\Biosphere\20200909 - Clonality and mapping efficiency

### FCs analyzed:

```
spar_dts_regression_2020_07:/prs-fix/
dts-spar6152-job19302-H575JBCX3_SPAR_EXP6152/
dts-spar6152-job19304-H73JWBCX3_SPAR_EXP6152/
dts-spar6152-job19306-H73KFBCX3_SPAR_EXP6152/
dts-spar6152-job19307-H73KGBCX3_SPAR_EXP6152/
dts-spar6152-job19308-H73KHBCX3_SPAR_EXP6152/
```
>* 960 samples.
### Seq_pipeline data:
To pull data analyzed by seq-pipeline I followed Thad's protocol below:
>* https://mygn.atlassian.net/l/c/9zTyj70P

The seq_pipeline branch "collect_mark_duplicates_metrics_thad" was used to generate MarkDuplicates reports (*.dupe_metrics.txt; see link above for details). The branch utilizes a modified seq_pipeline/wdl/tools/bam.wdl that contains additional instructions for the original_bam_to_final_bam process that writes an output file with metrics that are typically not preserved. To run the modified branch a workflow is created using spar. The workflow-FvbXyF006GZ0jxxk6GjG6bj8 was created for this analysis. The jobs that originally created final.bam's of interest can be `dx run` (re-run) with the modified workflow and process step `myelin_dts_workflows:/workflows/seq_pipeline/cdcf82d6/f35acf7a/original_bam_to_final_bam` (see array_dx_custom_wf for specific command and options; see Thad's write-up https://mygn.atlassian.net/l/c/9zTyj70P for more details).  

#### Workflow:  collects 1 FC of data at a time:

`dx cd` to  `analysis/alignments` of interest.

Collect a list of bam jobs for all *final.bam's in directory:

`dx describe *.final.bam | grep job- > /mnt/c/Users/jlandon/Downloads/H575JBCX3_final_bam_jobs.txt `

>* Parse output .txt with excel and paste list of jobs into the input array in array_dx_custom_wf script.
>* Also change target output folder in array_dx_custom_wf script.
>* If the output folder doesn't yet exist it will be created by array_dx_custom_wf



array_dx_custom_wf  (partial code example) - Kicks off DNAnexus runs. (I copied into ~/bin then run as command).

```
#!/bin/bash

# Jobs to run on custom workflow
array1=(
job-Fv7qj6j0J430XZ098vXjFk3b
job-Fv7qgkQ0J43PBQFVJk3YQv9y
...) #tested 192

t=0

for i in ${array1[*]}; 
    do
        dx run myelin_dts_workflows:/workflows/seq_pipeline/cdcf82d6/f35acf7a/original_bam_to_final_bam --clone "${array1[t]}" --destination myRisk_dev:/testing/jwl/"H73KHBCX3" --yes
        t=$t+1
    done
```

It takes about 15 min to run.

Download data files to local; organized in folders named flowcell_ID.

>* Example directory structure (avoids renaming files using FC directory heirarchy):
```
/mnt/c/Users/willl/Downloads/data_comp_200827/
H575JBCX3  H73JWBCX3  H73KFBCX3  H73KGBCX3  H73KHBCX3
```
>* download all_metrics.json's:

`spar_dts_regression_2020_07:/prs-fix/dts-spar6152-job19308-H73KHBCX3_SPAR_EXP6152/200216_D00642_1825_AH73KHBCX3/analysis/metrics/all_metrics.json`

>* download dupe_metrics.txt files:

`dx download *dupe_metrics.txt`


## On-prem data
SQL query:

```
SELECT *
FROM hcp.run_sample rs
    JOIN hcp.run r USING (run_id)
    JOIN hcp.sample s USING (sample_id)
    JOIN hcp.run_sample_summary rss USING (run_sample_id)
 --   JOIN hcp.run_sample_file rsf USING (run_sample_id)
WHERE r.run_name IN 
(
'H575JBCX3',
'H73JNBCX3',
'H73JWBCX3',
'H73KFBCX3',
'H73KGBCX3'
)
ORDER BY s.accession_id,
    r.run_name
;

```

## Data collation

Run python script parse-metrics.py to collate data from the above sources see README.md

