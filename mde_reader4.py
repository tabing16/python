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

arr = []

with open("MV90_MDEF_EXPORT_20180509_150005.MDE", "rb") as f:
    byte = f.read()

rec = 216

while rec <= len(byte):
    print(rec)
    rec += 216
