# libaries
import os
import pandas as pd
import MySQLdb as msq

# set directory
print("Changing directories...")
os.chdir("../../Personal/Practice/GSOD")

# connect to MySQL -- change to not root in future...
cnx = msq.connect(user='root', passwd='Apr!lf00L$',
                  host='localhost', db='test')

# get csv data and send
df = pd.read_csv("gsod_2018_final.csv")
df.to_sql(con=cnx, name='gsod2018', if_exists='append', flavor='mysql', index=False)
cnx.commit()
print ("Upload completed.")