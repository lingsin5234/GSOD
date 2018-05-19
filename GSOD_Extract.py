# python, download and extract the GSOD daily updated 2018 tar file

# import libraries
from ftplib import FTP
import os
import tarfile as tf
import gzip as gz
import shutil as sl
import time as tm

# directories
ddir = '/home/pi/z_extract/GSOD_daily'
os.chdir(ddir)
ftp = FTP('ftp.ncdc.noaa.gov')

# login to ftp
print('Logging in...')
ftp.login('ftp', 'sinto52@hotmail.com')

# change ftp directory
print('Changing directory...')
ftp.cwd('/pub/data/gsod/2018')

# retrieve and print filenames
print('Retrieving filenames...')
ftp.retrlines('LIST')

# grab the 2018 tar file
print('Downloading gsod_2018.tar file...')
file = open(os.curdir + '/gsod_2018.tar', 'wb')
ftp.retrbinary('RETR gsod_2018.tar', file.write)

# close ftp and file
file.close()
ftp.close()

# download complete
print('Downloaded Successfully.')

# create new directory for extracting files
print('Extracting to new directory...')
os.mkdir('g2018')
os.mkdir('g2018_op')

# extract tar file into the new directory
TF = tf.open('gsod_2018.tar')
tm.sleep(5)  # 5 second of time to open the file properly
TF.extractall('g2018')

# extract all the .gz files into the op_files folder
print('Extracting individual gzip files...')
os.chdir('g2018')
i = 0
for filename in os.listdir():

    # check for non .gz file
    fl_nm = os.path.abspath(filename)  # get absolute path, need to add op_files to the path
    if str.find(fl_nm, '.op.gz') > -1:

        # extract gz file to op_files folder
        f = gz.open(filename, 'rb')
        fl_con = repr(f.read())
        fl_nm = str.replace(fl_nm, '.gz', '')  # remove .gz from original file name
        fl_nm = str.replace(fl_nm, 'g2018', 'g2018_op')  # add op_files folder to the path
        nf = open(fl_nm, 'w')
        nf.write(fl_con)
        f.close()
        nf.close()
        i += 1
        print('Extracted File # %i' % i)

# print when completed successfully
print('Extraction completed successfully.')

# remove .tar and .gz files
print('Removing temp folder and files...')
os.chdir("..")
sl.rmtree('g2018')  # os.rmdir('g2018'), does not work, need to remove entire tree
os.remove('gsod_2018.tar')
print('Removal Complete.')
print('ETL scripts: Extract stage complete.\n...\nPlease proceed to Transform stage')
