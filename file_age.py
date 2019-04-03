import time
import os
from _stat import ST_MTIME

now = time.time()

z = 2
fname = os.stat('file_age.py');

#list all file older than z days
if (fname[ST_MTIME]) < now - (z * 86400):
    print ("Older than 2 days") 
else:
    print ("less than 2 days")