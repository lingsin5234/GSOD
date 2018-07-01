# libaries
import os
import pandas as pd
import MySQLdb as msq
from sqlalchemy import create_engine

# create engine for mariadb
engine = create_engine("mysql+mysqldb://rasppi:"+'Apr!lf00L$'+"@192.168.1.215/test")

# set directory
print("Changing directories...")
# os.chdir("../../Personal/Practice/GSOD") # work laptop
os.chdir("/home/pi/z_extract/GSOD_daily")

# connect to MySQL -- change to not root in future...
# cnx = msq.connect(user='rasppi', passwd='Apr!lf00L$',
#                   host='192.168.1.215', port=3306, db='test')

# get csv data and send
df = pd.read_csv("gsod_2018_final.csv")
# df.to_sql(con=cnx, name='gsod2018', if_exists='append', flavor='mysql', index=False)
logf = open("download.log", "w")
try:
	df.to_sql(con=engine, name='gsod2018', if_exists='append', index=False)
except Exception as e:
	logf.write('%s' % e)
# cnx.commit()
print ("Upload completed.")
