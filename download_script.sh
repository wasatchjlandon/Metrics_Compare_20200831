#!/bin/bash
data_path=dts-spar6525-job19786-HLNHFDRXX_SPAR_EXP6525/200919_A01175_0084_AHLNHFDRXX
dx cd $data_path/analysis/alignments
dx download all_barcodes.html
dx cd ../metrics
dx download all_metrics.json
dx download *_target_read_counts.csv

dx download *dupe_metrics.txt



for i in ${array1[*]}; 
    do
        dx run myelin_dts_workflows:/workflows/seq_pipeline/cdcf82d6/f35acf7a/original_bam_to_final_bam --clone "${array1[t]}" --destination onc_tech_dev_FY21:/Occupancy/dupe_metrics/"HLNHFDRXX" --yes
        t=$t+1
    done

