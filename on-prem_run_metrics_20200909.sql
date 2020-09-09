Select *
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