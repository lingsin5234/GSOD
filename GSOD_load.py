# libaries
import os
import mysql

# set directory
print("Changing directories...")
os.chdir("..\..\Personal\Projects\GSOD")

# connect to MySQL -- change to not root in future...
cnx = mysql (user='root', password='Apr!lf00L$',
                   host='127.0.0.1',
                   database='test')
