#!/bin/sh
# grab the first line of 1 .op file; > ovewrites file
head -n 1 `ls /home/pi/z_extract/GSOD_daily/g2018_op/*.op | head -1` | paste -sd '\n' > /home/pi/z_extract/GSOD_daily/g2018.csv

# retrieve last line of every .op file and add to csv file; >> appends to end of file (if exists)
tail -n 1 /home/pi/z_extract/GSOD_daily/g2018_op/*.op | paste -sd '\n' >> /home/pi/z_extract/GSOD_daily/g2018.csv

# now remove starting with the 2nd line remove every 3rd line (===>> output file name <<===)
# then remove the blank lines in between - starting with 3rd line, every 2nd line
# then save to new csv file
sed '2~3d' /home/pi/z_extract/GSOD_daily/g2018.csv | sed '3~2d' > /home/pi/z_extract/GSOD_daily/gsod_2018.csv


