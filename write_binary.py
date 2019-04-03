import struct
import os
from datetime import datetime

filename = 'MyFile.MDE'

my_hex = struct.pack('<HH', 216,1)
my_null = struct.pack('<H',32767)
my_float = struct.pack('<f',1.91)

date_format = "%d-%m-%Y %H:%M:%S"

time1  = datetime.strptime('01-01-2008 00:00:00', date_format)
time2  = datetime.strptime('02-01-2008 00:30:00', date_format)

diff = time2 - time1

#diff_in_minutes = (diff.days * 1440 + diff.seconds/60)

#print(str(diff_in_minutes) + ' minutes')

if os.path.exists(filename):
    os.remove(filename)

def write_binary(filename,value):
    with open(filename,'ab') as writer:
        writer.write(value)

def write_string(filename,value):
    with open(filename,'a') as writer:
        writer.write(value)  

write_binary('MyFile.MDE', my_hex) 
write_binary('MyFile.MDE', my_float)
write_binary('MyFile.MDE', my_null) 
#write_string('MyFile.MDE','0214000015')