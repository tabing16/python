import struct

# class AutoVivication(dict):

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
    # print ('j: ' + str(j))
    k = j
    i += 1
    l = 216 * i
    arr.append(a[k:l])
    # print ('k: ' + str(k))
    # print ('l: ' + str(l))

for comp in arr:
    # a = binascii.hexlify(comp[0:2]).decode('utf-8')
    if len(comp[0:2]) == 2:
        #a = struct.unpack('<H', binascii.unhexlify(binascii.hexlify(comp[0:2])))
        a = struct.unpack('<H', comp[2:4])[0]
        if a == 1:
            print("Meter Header")
            # print("Meter Number " + comp[4:24].decode('utf-8').strip())
            print("Meter Number " + decode_chars(comp[4:24]).strip())
        elif a == 10:
            print("Channel Header")
            # print("Channel Number: " + comp[93:95].decode('utf-8'))
            # print("Interval Per Hour: " + comp[177:179].decode('utf-8'))
            print("Channel Number: " + decode_chars(comp[93:95]))
            print("Interval Per Hour: " + decode_chars(comp[177:179]))
        elif a == 9999:
            print("Trailer Data")
        else:
            print("Interval Data")


#print(struct.unpack('H', arr[4][2:4]))

# mystr = a[0]
# print (len(mystr))
# print(str)
# print(struct.unpack('<H',mystr[0:2])[0])
# print(struct.unpack('<H',mystr[2:4])[0])
# print(str(mystr[4:23], 'utf-8'))
