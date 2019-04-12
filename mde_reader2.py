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

with open("MV90_MDEF_LT_20190325124256_3820.MDE","rb") as f:
    a = f.read()

i = 1
arr = []
while i <= len(a)/216:
    j = 216 * i
    if j <= 216:
        arr.append(a[0:j])
    k = j
    i += 1
    l = 216 * i
    arr.append(a[k:l])


av = AutoVivication()
mychn = {}
myrdg = {}
z = 0
for comp in arr:
    n = 24
    if len(comp[0:2]) == 2:
        a = struct.unpack('<H', comp[2:4])[0]

        if a == 1:
            pass#z = 0
            # print("Meter Header")
            # print("Meter Number " + decode_chars(comp[4:24]).strip())
            # print("Timestart: " + decode_chars(comp[119:131]))
            # print("Timestop: " + decode_chars(comp[131:143]))
        elif a == 10:
            pass
            # print("Channel Header")
            # mychn[z] = decode_chars(comp[93:95])
            # print('Channel C: ' + str(z))
            # print("Channel Number: " + decode_chars(comp[93:95]))
            # print("Interval Per Hour: " + decode_chars(comp[177:179]))
        elif a == 9999:
            pass
            # z = 0
            # print("Trailer Data")
        else:
            z = z - 1
            print("Interval Data")
            while n <= 192:
                if(math.isnan(struct.unpack('<f', comp[n:n+4])[0])):
                    pass
                else:
                    av[z][n]= struct.unpack('<f', comp[n:n+4])[0]
                    print('Reading C: ' + str(z))
                    # print(struct.unpack('<f', comp[n:n+4])[0])
                    # print(struct.unpack('<H', comp[n+4:n+6])[0])
                    # print(struct.unpack('<H', comp[n+6:n+8])[0])
                n += 8
    z += 1

print(av)