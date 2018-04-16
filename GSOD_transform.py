# libraries
import os
import pandas as pd
import datetime as dtm
import time as tm

# set directory
print("Changing directories...")
os.chdir("..\..\Personal\Practice\GSOD\gsod_2018")

# get date and convert to string
dt = dtm.datetime.now()
print("Today's Date: " + dt.strftime("%Y%m%d") + "...")

# use timestamps
i = 0
time_st = tm.time()

# set header names
print("Adding header names...")
lst = ['Station', 'WBAN', 'YearMoDa', 'Temp', 'Temp_cnt', 'Dewp', 'Dewp_cnt', 'SLP', 'SLP_cnt',
       'STP', 'STP_cnt', 'VISIB', 'Visib_cnt', 'WDSP', 'Wdsp_cnt', 'Max_Wind_Speed', 'Max_tmp',
       'Min_tmp', 'Precip', 'Precip_flg', 'Snow_Depth', 'Disaster']
lst = repr(lst)[1:-1]  # get rid of the [ ]

# add the header
fl = open('..\gsod_2018.csv', 'w')
fl.write(lst + '\n')  # rep returns a string instead of "list"
fl.close()

# loop and add dfs
print("Adding data to the .csv file...")
with open("..\gsod_2018.csv", "a+") as fl:

    # append the dfs
    for filename in os.listdir(os.curdir):
        df = pd.read_fwf(filename, header=0)
        df = df.tail(1)  # grab only the last line!
        df.to_csv(fl, header=False, index=False)
        # print("filename %i" % i)
        i += 1
fl.close()
print("Data Transform Completed.")
print("Execution Time: %s seconds" % (tm.time() - time_st))
