import struct
import math
from datetime import datetime
from datetime import timedelta


class AutoVivication(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


def decode_chars(chars):
    return chars.decode('utf-8')


with open("MV90_MDEF_LT_20190325124256_3820.MDE", "rb") as f:
    a = f.read()

i = 1
recs = []
print(len(a))

while i <= len(a) / 216:
    j = 216 * i
    if j <= 216:
        arr.append(a[0:j])
    i += 1
    l = 216 * i
    arr.append(a[j:l])
    recs.append(arr)
    arr = []

print(recs)
av = AutoVivication()

for rec in recs:
    mychn = {}
    myrdg = {}
    z = 0
    meter = None
    datestart = None
    dateend = None
    chnstat = None
    intstat = None
    for comp in rec:
        n = 24
        if len(comp[0:2]) == 2:
            a = struct.unpack('<H', comp[2:4])[0]
            if a == 1:
                meter = decode_chars(comp[4:24])
                datestart = decode_chars(comp[119:131])
                #print(datestart)
                datestop = decode_chars(comp[131:143])
                #print(datestop)
            elif a == 10:
                chnstat = decode_chars(comp[99:100])
                #print(chnstat)
                intstat = decode_chars(comp[100:101])
                #print(intstat)
                # if chnstat == 'Y' and intstat == 'Y':
                #     n = 48
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

# av = AutoVivication()
# mychn = {}
# myrdg = {}
# z = 0
# datestart = None
# dateend = None
# chnstat = None
# intstat = None
# for comp in arr:
#     n = 24
#     if len(comp[0:2]) == 2:
#         a = struct.unpack('<H', comp[2:4])[0]
#         if a == 1:
#             datestart = decode_chars(comp[119:131])
#             print(datestart)
#             datestop = decode_chars(comp[131:143])
#             print(datestop)
#         elif a == 10:
#             chnstat = decode_chars(comp[99:100])
#             print(chnstat)
#             intstat = decode_chars(comp[100:101])
#             print(intstat)
#             # if chnstat == 'Y' and intstat == 'Y':
#             #     n = 48
#         elif 1001 <= a <= 9998:
#             z = z - 1
#             b = 0
#             while n <= 192:
#                 if(math.isnan(struct.unpack('<f', comp[n:n+4])[0])):
#                     pass
#                 else:
#                     av[z][b]= round(struct.unpack('<f', comp[n:n+4])[0],3)
#                 n += 8
#                 b += 1
#     z += 1

# print(av)
# print(n)
