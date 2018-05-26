# libraries
import os
import pandas as pd
import datetime as dtm
import time as tm

# get date and convert to string
dt = dtm.datetime.now()
print("Today's Date: " + dt.strftime("%Y%m%d") + "...")

# use timestamps
i = 0
time_st = tm.time()

# set directory
print("Changing directories...")
os.chdir("/home/pi/z_extract/GSOD_daily/")

# read file and fix unnamed columns
fl = pd.read_fwf("gsod_2018.csv")
fl.columns = ['STATION', 'WBAN', 'YEARMODA', 'TEMP_AVG', 'TEMP_CNT', 
'DEWP_AVG', 'DEWP_CNT', 'SLP_AVG', 'SLP_CNT', 'STP_AVG', 'STP_CNT', 
'VISIB_AVG', 'VISIB_CNT', 'WDSP_AVG', 'WDSP_CNT', 'MXSPD', 'GUST',
'TEMP_MAX', 'TEMP_MIN', 'PRCP_TOT', 'SNDP', 'FRSHTT']

# write to csv file
fl.to_csv("gsod_2018_final.csv", sep=',', index=False)
print("Data Transform Completed.")
print("Total Execution Time: %s seconds" % (tm.time() - time_st))
