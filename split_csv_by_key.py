import csv
import os
import math
from itertools import groupby
import re

pattern = re.compile(r"[0-9]")

for key, rows in groupby(csv.reader(open(os.path.join('csv', 'mtr_data5.csv'))),
                                                     lambda row: row[1]):
    if not pattern.match(key):
        for row in rows:
            header = ",".join(row)
        continue
    else:
        with open(os.path.join("csv", "%s.csv" % key), "w") as output:
            output.write(header+"\n")    
            for row in rows:
                output.write(",".join(row) + "\n")