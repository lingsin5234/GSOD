# libraries
import os
import pandas as pd
import datetime as dtm
import time as tm

# set directory
print("Changing directories...")
os.chdir("..\..\Personal\Practice\GSOD\gsod_2018")

# open with fixed width, header in line 0
# fo = open("010010-99999-2018.op")
# df = pd.read_fwf(fo, header=0)
# print(df.iloc[0])  # .iloc selects index [row, column]
# print(list(df))

# get date and convert to string
dt = dtm.datetime.now()
# print(dt.strftime("%Y%m%d"))
# print(type(dt.strftime("%Y%m%d")))  # type str, as expected


# WORKS! uncomment when you need to run it again
# now that i opened one... let's be greedy...
# use timestamps
i = 0
time_st = tm.time()

# lst = repr(list(df))
# lst = lst[1:-1]
lst = ['Station', 'WBAN', 'YearMoDa', 'Temp', 'Temp_cnt', 'Dewp', 'Dewp_cnt', 'SLP', 'SLP_cnt',
       'STP', 'STP_cnt', 'VISIB', 'Visib_cnt', 'WDSP', 'Wdsp_cnt', 'Max_Wind_Speed', 'Max_tmp',
       'Min_tmp', 'Precip', 'Precip_flg', 'Snow_Depth', 'Disaster']
lst = repr(lst)[1:-1]
# print(lst)  # will still put the [ ] there lol.

# add the header
fl = open('..\gsod_2018.csv', 'w')
fl.write(lst + '\n')  # rep returns a string instead of "list"
fl.close()

with open("..\gsod_2018.csv", "a+") as fl:

    # print('open')

    # append the dfs
    for filename in os.listdir(os.curdir):
        df = pd.read_fwf(filename, header=0)
        df = df.tail(1)  # grab only the last line!
        df.to_csv(fl, header=False, index=False)
        # print("filename %i" % i)
        i += 1
fl.close()
print("Execution Time: %s seconds" % (tm.time() - time_st))


# now read the text file as csv
# df = pd.read_csv("..\gsod_2018.txt")
# df.columns = ['Station', 'WBAN', 'YearMoDa', 'Temp', 'Temp_cnt', 'Dewp', 'Dewp_cnt', 'SLP', 'SLP_cnt',
#               'STP', 'STP_cnt', 'VISIB', 'Visib_cnt', 'WDSP', 'Wdsp_cnt', 'Max_Wind_Speed', 'Max_tmp',
#               'Min_tmp', 'Precip', 'Precip_flg', 'Snow_Depth', 'Disaster']
# print(df)




'''
# too greedy lol.
DF = df.iloc[0]
for filename in os.listdir(os.curdir):
    df = pd.read_fwf(filename, header=0)
    DF = DF.append(df)
print("Execution Time: %s seconds" % (tm.time() - time_st))
'''
'''
# read 1 file first
fo = open("010010-99999-2018.op")
lines = fo.readlines()
# print(lines)

# use split - ignores the \n
# lines = fo.read().split(",")

# print array
# print(', '.join(lines))
print(lines[0], lines[1])

print(type(lines))

# read all into 1 line
lines = fo.read()
print([sub.split("\t") for sub in lines])

# convert list to df
import pandas as pd
# df = pd.DataFrame({'line':lines}) # done by line only, does not separate into multiple columns
df = pd.DataFrame([sub.split("\t") for sub in lines])
print(df)

# try csv
import csv
with open("010010-99999-2018.op") as f:
    reader = csv.reader(f, delimiter="\t")
    d = list(reader)
print(d[0])

# there is no separator - it's only spaces. UGH... fixed-width needed
'''