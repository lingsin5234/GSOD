#!/bin/sh
# clean up the GSOD_daily folder
rm -r  ~/z_extract/GSOD_daily/g2018_op
rm ~/z_extract/GSOD_daily/g2018.csv
rm ~/z_extract/GSOD_daily/gsod_2018.csv
rm ~/z_extract/GSOD_daily/gsod_2018_final.csv
rm ~/z_extract/GSOD_daily/download.log
echo 'files removed'

# rename the log files
mv ~/z_extract/GSOD_ext.log ~/z_extract/GSOD_ext_$(date +%d-%m-%Y).log
mv ~/z_extract/GSOD_tx.log ~/z_extract/GSOD_tx_$(date +%d-%m-%Y).log
mv ~/z_extract/GSOD_ld.log ~/z_extract/GSOD_ld_$(date +%d-%m-%Y).log
echo 'logs renamed'
