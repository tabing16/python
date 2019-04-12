from datetime import datetime
from datetime import timedelta
from math import ceil
import struct
import os
import argparse

rec_length = 216
meter_rec = 1
channel_rec = 10
interval_rec = 1000
trailer_rec = 9999

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--reg", nargs='+', type=str, action='append', required=True,
                    help="channel number and unit of measure")
parser.add_argument("-m", "--meter", nargs='+', type=str, required=True)
parser.add_argument("-f", "--from", nargs='+', type=str, required=True, help="start period of the reading")
parser.add_argument("-t", "--to", nargs='+', type=str, required=True, help="end period of the reading")

args = parser.parse_args()

dt_start = "01-01-2018 00:15"
dt_end = "01-01-2019 00:00"
datetime_strp = "%d-%m-%Y %H:%M"
datetime_strf = "%Y%m%d%H%M"

# 4 bytes interval readings, 2 bytes channel stat, 2 bytes interval stat. Total = 8
field_length = 8
period = 15
reading_per_day = 1440/period  # 1440 minutes per day

dt_start_strp = datetime.strptime(dt_start, datetime_strp)
dt_end_strp = datetime.strptime(dt_end, datetime_strp)

dt_start_strf = datetime.strftime(dt_start_strp, datetime_strf)
dt_end_strf = datetime.strftime(dt_end_strp, datetime_strf)

diff = dt_end_strp - dt_start_strp

day_count = ceil((diff.days + 0.5))

interval_count = reading_per_day * day_count

reading_row_count = int((interval_count * field_length)/192)  # 192 bytes of reading per record

i = 1

dt = dt_start_strp

for channels in len(args.reg):
    print(channels)

# while i <= int(reading_row_count):
#     print(interval_rec + i)
#     j = 1
#     while j <= 192/field_length:
#         if dt > dt_end_strp:
#             print('32767' + ' - ' + str(dt))
#         else:
#             print(str(j) + ' - ' + str(dt))
#         j += 1
#         dt += timedelta(minutes=period)
#     i += 1


def write_string(val, length):
    return val.ljust(length)


def write_date_string(dt,frm):
    return datetime.strftime(dt, frm)


def write_int(val):
    return struct.pack('<H', val)


def write_float(val):
    return struct.pack('<f', val)


