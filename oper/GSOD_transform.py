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
# os.chdir("../../Personal/Practice/GSOD") # work laptop
os.chdir("/home/pi/z_extract/GSOD_daily/")

# read file and fix unnamed columns
# fl = pd.read_csv("gsod_2018.csv") # work laptop
fl = pd.read_fwf("gsod_2018.csv")
fl.columns = ['STATION', 'WBAN', 'YEARMODA', 'TEMP_AVG', 'TEMP_CNT', 
'DEWP_AVG', 'DEWP_CNT', 'SLP_AVG', 'SLP_CNT', 'STP_AVG', 'STP_CNT', 
'VISIB_AVG', 'VISIB_CNT', 'WDSP_AVG', 'WDSP_CNT', 'MAX_WIND_SPD', 'GUST',
'TEMP_MAX', 'TEMP_MIN', 'PRCP_TOT', 'SNOW_DEPTH', 'DISASTER']

# insert separate columns for the temp and precip flags
idx = fl.columns.get_loc("TEMP_MAX") + 1
fl.insert(loc=idx, column='T_MAX_FLG', value=0)
idx = fl.columns.get_loc("TEMP_MIN") + 1
fl.insert(loc=idx, column='T_MIN_FLG', value=0)
idx = fl.columns.get_loc("PRCP_TOT") + 1
fl.insert(loc=idx, column='PRCP_FLG', value=0)

# change the flag if there is a * in the value
fl.loc[fl['TEMP_MAX'].str.contains('\*'), 'T_MAX_FLG'] = 1
fl.loc[fl['TEMP_MIN'].str.contains('\*'), 'T_MIN_FLG'] = 1
fl.loc[fl['PRCP_TOT'].str.contains("A|B|C|D|E|F|G|H|I"), 'PRCP_FLG'] = fl['PRCP_TOT'].str.extract("(A|B|C|D|E|F|G|H|I)")

# take the respective flags out
fl['TEMP_MAX'].replace("\*", "", regex=True, inplace=True)
fl['TEMP_MIN'].replace("\*", "", regex=True, inplace=True)
fl['PRCP_TOT'].replace("A|B|C|D|E|F|G|H|I", "", regex=True, inplace=True)

# write to csv file
fl.to_csv("gsod_2018_final.csv", sep=',', index=False)
print("Data Transform Completed.")
print("Total Execution Time: %s seconds" % (tm.time() - time_st))
