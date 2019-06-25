import struct
import math
import os
from datetime import datetime
from datetime import timedelta
import re


class AutoVivication(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


def decode_chars(chars):
    return chars.decode('utf-8')


def convert_dt(chars):
    dt = re.findall(r'^(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})$',chars)
    return dt[0][2]+"-"+dt[0][1]+"-"+dt[0][0]+" "+dt[0][3]+":"+dt[0][4]

mv90filename = "MV90_MDEF_LT_20190325124256_3820.MDE"

with open(os.path.join("mde", mv90filename), "rb") as f:
    a = f.read()

i = 1
recs = []
#print(len(a))
arr = []
while i <= len(a) / 216:
    j = 216 * i
    if j <= 216:
        arr.append(a[0:j])
    i += 1
    l = 216 * i
    arr.append(a[j:l])
    recs.append(arr)
    arr = []

#print(recs)
av = AutoVivication()

for rec in recs:
    mychn = {}
    myrdg = {}
    z = 0
   
   
    for comp in rec:
        n = 24
        if len(comp[0:2]) == 2:
            a = struct.unpack('<H', comp[2:4])[0]
            if a == 1:
                meter = decode_chars(comp[4:24])[0:10]
                datestart = decode_chars(comp[119:131])
                datestop = decode_chars(comp[131:143])
            elif a == 10:
                # chnstat = decode_chars(comp[99:100])
                # intstat = decode_chars(comp[100:101])
                int_per_hour = decode_chars(comp[177:179])
                chan_number = decode_chars(comp[93:95])
                datetime_strp = "%d-%m-%Y %H:%M"
                datestart_strp = datetime.strptime(convert_dt(datestart), datetime_strp)
                if int_per_hour == '02':
                    datestart_strp = datestart_strp + timedelta(minutes=29)
                elif int_per_hour == '04':
                    datestart_strp = datestart_strp + timedelta(minutes=14)

                datestart_strf = datetime.strftime(datestart_strp,datetime_strp)

                print(f"Meter : {meter}, Channel: {chan_number}, DateStart: {datestart_strf}, DateStop: {convert_dt(datestop)}, Interval Per Hour: {int_per_hour}")             
            elif 1001 <= a <= 9998:
                z = z - 1
                b = 0
                while n <= 192:
                    if(math.isnan(struct.unpack('<f', comp[n:n+4])[0])):
                        pass
                    else:
                        av[z][b] = round(struct.unpack('<f', comp[n:n+4])[0],3)
                    n += 8
                    b += 1
            
        z += 1
        