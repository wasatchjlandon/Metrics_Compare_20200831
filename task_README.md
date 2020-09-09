# MPD-115

# Add metrics for mapping efficiency and clonality.
 Flowcells analyzed using the on-prem and seq_pipeline systems were identified. Data was extracted and compared. 

## Seq_pipeline data:
To pull data analyzed by seq-pipeline I followed the protocol below:

https://mygn.atlassian.net/l/c/9zTyj70P

The following workflow collects 1 FC of data at a time:

`cd` to `analysis/alignments` of interest.

Collect a list of bam jobs:

` dx describe *.final.bam | grep job- > /mnt/c/Users/jlandon/Downloads/H575JBCX3_final_bam_jobs.txt `

Parsed output with excel and pasted it into: array bash script

Ran python script:


## On-prem data
SQL query:
Pre-biosphere
num_mapped_clone_reads - count of unique trimmed and aligned clone reads with PCR duplicates removed
num_eligible_reads - total count of trimmed, full-length reads used for alignment
duplicate_clones_numerator - count of trimmed and aligned clone reads that were excluded as PCR duplicates
duplicate_clones_denominator - count of all trimmed and aligned clone reads including PCR duplicates
num_mapped_clone_reads + duplicate_clones_numerator = duplicate_clones_denominator
____

Picard metrics MarkDuplicates functions to mark reads as duplicates during analysis to limit certain analyses to unique read