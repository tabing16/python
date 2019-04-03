arr = []

with open('MV90_MDEF_MDEGEN_20190313105530_14094.MDE',"rb") as f:
    for line in f:
        arr.append(line)#print(line)

for item in arr:
    print(item)