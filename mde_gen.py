from math import ceil
from datetime import datetime
from datetime import timedelta
import struct
import argparse
import re
import os
import random


def write_binary(filename, value):
    with open(filename, 'ab') as writer:
        writer.write(value)


def write_string(filename, value):
    with open(filename, 'a') as writer:
        writer.write(value)


def put_string(filename, val, length, mode=1):
    # Mode 1 is for string. Mode 2 is for integer
    if mode == 1:
        write_string(filename, val.ljust(length, " "))
    elif mode == 2:
        write_string(filename, str(val).rjust(length, "0"))


def put_bint(filename, val):
    write_binary(filename, struct.pack('<H', val))


def put_bfloat(filename, val):
    write_binary(filename, struct.pack('<f', val))


def dt_regex_validation(s, pat=re.compile(r"\d{2}\-\d{2}\-\d{4}\s+\d{2}:\d{2}")):
    if not pat.match(s):
        raise argparse.ArgumentTypeError
    return s


def translate_uom(str_val):
    uom_dict = {'KWH': '01', 'KVARH': '03', 'KVAH': '04'}
    for key, value in uom_dict.items():
        if key == str_val.upper():
            return value


def determine_dir(chn, uom):
    if uom.upper() == "KWH" and chn in ("01", "02", "04"):
        return "D"
    else:
        return "R"


def gen_rand(high, low):
    return random.randint(high, low) * 0.001


rec_length = 216
meter_rec = 1
channel_rec = 10
interval_rec = 1000
trailer_rec = 9999
rec_count = 0

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--reg", nargs='+', type=str, action='append', required=True
                    , help="channel number and unit of measure. in format 01:kwh")
parser.add_argument("-n", "--nmi", nargs='+', type=str, required=True, help="NMI Number")
parser.add_argument("-m", "--meter", nargs='+', type=str, required=True, help="Meter Number")
parser.add_argument("-s", "--start", nargs='+', required=True, type=dt_regex_validation
                    , help="start period of the reading. in format DD-MM-YYYY For example: 01-03-2019 00:15")
parser.add_argument("-e", "--end", nargs='+', required=True, type=dt_regex_validation, 
                        help="end period of the reading. in format DD-MM-YYYY. For example: 01-03-2019 00:15")
parser.add_argument("-i", "--interval", nargs='+', required=True, type=int, default=15, choices=[15, 30]
                    , help="number of Interval per hour. Accepts only 15 or 30 minutes.")
parser.add_argument("-z", "--sendzero", nargs='?', required=False, type=str, default="NO", choices=["YES", "NO"]
                    , help="Optional: If set to YES then it will send zero valued Interval read")

args = parser.parse_args()

dt_start = args.start[0]
dt_end = args.end[0]

datetime_strp = "%d-%m-%Y %H:%M"
datetime_strf = "%Y%m%d%H%M"
datetime_strf2 = "%Y%m%d%H%M%S"

# 4 bytes interval readings, 2 bytes channel stat, 2 bytes interval stat. Total = 8
field_length = 8
period = args.interval[0]

reading_per_day = 1440/period  # 1440 minutes in a day

dt_start_strp = datetime.strptime(dt_start, datetime_strp)
dt_end_strp = datetime.strptime(dt_end, datetime_strp)

#  below is used to tell MBS the start of interval. Example: if interval starts at 00:15 then convert it to 00:01
#  if at 00:30, the convert it to 00:16
new_dt_start_strp = dt_start_strp - timedelta(minutes=14)

dt_start_strf = datetime.strftime(new_dt_start_strp, datetime_strf)
dt_end_strf = (datetime.strftime(dt_end_strp, datetime_strf)).replace("0000", "2400")
now = datetime.strftime(datetime.now(), datetime_strf)
file_ts = datetime.strftime(datetime.now(), datetime_strf2)

diff = dt_end_strp - dt_start_strp

day_count = ceil((diff.days + 0.5))

interval_count = reading_per_day * day_count

reading_row_count = int((interval_count * field_length)/192)  # 192 bytes of reading per record

mde_filename = 'MV90_MDEF_EXPORT_'+str(file_ts)+'_'+str(random.randint(1000, 5000))+'.MDE'

if os.path.exists(mde_filename):
    os.remove(mde_filename)


def write_meter_rec():
    global rec_count
    rec_count += 1
    put_bint(mde_filename, rec_length)
    put_bint(mde_filename, meter_rec)
    put_string(mde_filename, args.meter[0], 20)
    put_string(mde_filename, "Customer01", 20)
    put_string(mde_filename, "Address1", 20)
    put_string(mde_filename, "Address2", 20)
    put_string(mde_filename, args.nmi[0], 20)
    put_string(mde_filename, "", 7)
    put_string(mde_filename, len(args.reg), 4, 2)
    put_string(mde_filename, "", 4)
    put_string(mde_filename, dt_start_strf, 12)
    put_string(mde_filename, dt_end_strf, 12)
    put_string(mde_filename, "N", 1)
    put_string(mde_filename, "", 72)


def write_channel_rec(chn1, uom1, mmult):
    global rec_count
    rec_count += 1
    put_bint(mde_filename, rec_length)
    put_bint(mde_filename, channel_rec)
    put_string(mde_filename, args.meter[0], 20)
    put_string(mde_filename, args.meter[0], 14)
    put_string(mde_filename, "", 6)
    put_string(mde_filename, args.meter[0], 12)
    put_string(mde_filename, dt_start_strf, 12)
    put_string(mde_filename, dt_end_strf, 12)
    put_string(mde_filename, "000000000000", 12)
    put_string(mde_filename, "N", 1)
    put_string(mde_filename, chn1, 2)
    put_bint(mde_filename, int(chn1))
    put_string(mde_filename, translate_uom(uom1), 2)
    put_string(mde_filename, "Y", 1)
    put_string(mde_filename, "Y", 1)
    put_string(mde_filename, "000000000000", 12)
    put_string(mde_filename, "000000000000", 12)
    put_string(mde_filename, "", 1)
    put_string(mde_filename, '{:>010.3f}'.format(float(mmult)), 10)
    put_string(mde_filename, "", 30)
    put_string(mde_filename, "W", 1)
    put_string(mde_filename, "", 10)
    put_string(mde_filename, "04", 2)
    put_string(mde_filename, "", 12)
    put_string(mde_filename, "NA", 2)
    put_string(mde_filename, "AC", 2)
    put_string(mde_filename, "", 15)
    put_string(mde_filename, determine_dir(chn1, uom1), 1)
    put_bint(mde_filename, 0)
    put_string(mde_filename, "R", 1)
    put_string(mde_filename, "", 2)


def write_channel_and_int_data_rec():
    global rec_count
    for channels in args.reg:
        for channel in channels:
            spchn, spuom = channel.split(':')
            write_channel_rec(spchn, spuom, "1")
            i = 1
            dt = dt_start_strp
            while i <= int(reading_row_count):
                put_bint(mde_filename, rec_length)
                put_bint(mde_filename, interval_rec + i)
                put_string(mde_filename, args.meter[0], 20)
                j = 1
                while j <= 192/field_length:
                    if dt > dt_end_strp:
                        #  If no more data then fill the gap with Integer 32767 = FF7F
                        #       in Hex (Least Significant Byte Order)
                        put_bint(mde_filename, 32767)
                        put_bint(mde_filename, 32767)
                        put_bint(mde_filename, 32767)
                        put_bint(mde_filename, 32767)
                    else:
                        if args.sendzero[0] == "NO":
                            put_bfloat(mde_filename, gen_rand(50, 100))  # 4 bytes of float
                        else:
                            put_bfloat(mde_filename, 0)  # 4 bytes of float. If sendzero flag is set to YES
                        put_bint(mde_filename, 0)  # 2 bytes of int
                        put_bint(mde_filename, 0)  # 2 bytes of int
                    rec_count += 1
                    j += 1
                    dt += timedelta(minutes=period)
                i += 1


def write_trailer_rec():
    global rec_count
    rec_count += 1
    put_bint(mde_filename, rec_length)
    put_bint(mde_filename, trailer_rec)
    put_string(mde_filename, "", 30)
    put_string(mde_filename, '{:>010d}'.format(rec_count), 10)
    put_string(mde_filename, "", 160)
    put_string(mde_filename, now, 12)


# ==========Main Section=====================


write_meter_rec()
write_channel_and_int_data_rec()
write_trailer_rec()
print("File name is %s" % mde_filename)
