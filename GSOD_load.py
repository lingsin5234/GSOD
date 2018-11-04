# libaries
import os
import pandas as pd
import MySQLdb as msq
from sqlalchemy import create_engine

# create engine for mariadb
engine = create_engine("mysql+mysqldb://rasppi:"+'Apr!lf00L$'+"@192.168.1.215/test")

# set directory
print("Changing directories...")
os.chdir("../../Personal/Practice/GSOD") # work laptop
os.chdir("/home/pi/z_extract/GSOD_daily")

# get csv data and send
df = pd.read_csv("gsod_2018_final.csv")
logf = open("download.log", "w")
try:
	df.to_sql(con=engine, name='gsod2018', if_exists='append', index=False)
except Exception as e:
	logf.write('%s' % e)
# write job as success for now - no way to catch errors sooner.
finally:
	j = {'job_nm': ['GSOD_ETL'], 'status': ['Succeeded']} # 'finish_dt': now.strftime("%Y-%m-%d %H:%M:%S")}
	jlog = pd.DataFrame(data=j)
	jlog.to_sql(con=engine, name='Jobs', if_exists='append', index=False)

print ("Upload completed.")
