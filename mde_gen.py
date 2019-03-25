from math import ceil
from datetime import datetime
from datetime import timedelta
import struct
import argparse
import re
import random


class File:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    @staticmethod
    def write_string(name, value):
        with open(name, 'a') as writer:
            writer.write(value)

    @staticmethod
    def write_binary(name, value):
        with open(name, 'ab') as writer:
            writer.write(value)

    def put_string(self, filename, val, length, mode=1):
        filename = self.name
        if mode == 1:
            self.write_string(filename, val.ljust(length, " "))
        elif mode == 2:
            self.write_string(filename, str(val).rjust(length, "0"))

    def put_bint(self, filename, val):
        filename = self.name
        self.write_binary(filename, struct.pack('<H', val))

    def put_bfloat(self, filename, val):
        filename = self.name
        self.write_binary(filename, struct.pack('<f', val))


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
parser.add_argument("-e", "--end", nargs='+', required=True, type=dt_regex_validation
                    , help="end period of the reading. in format DD-MM-YYYY. For example: 01-03-2019 00:15")
parser.add_argument("-i", "--interval", nargs='+', required=True, type=int, default=15, choices=[15, 30]
                    , help="number of Interval per hour. Accepts only 15 or 30 minutes.")
parser.add_argument("-z", "--sendzero", nargs='?', type=str, choices=['Y', 'N']
                    , help="Optional argument: If set to YES then it will send zero valued Interval read")

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
interval_per_hour = 60/period
dt_start_strp = datetime.strptime(dt_start, datetime_strp)
dt_end_strp = datetime.strptime(dt_end, datetime_strp)

#  below is used to format timestamp in MV90 file for the start of interval
#  Example: for 15 minute interval, if interval starts at 00:15 then convert it to 00:01
#  if at 00:30 then convert it to 00:16
#  for 30 minute interval, if interval starts at 00:30 then convert to 00:01
#  if at 00:00 then convert to 00:31 (previous day)
new_dt_start_strp = dt_start_strp - timedelta(minutes=period-1)

dt_start_strf = datetime.strftime(new_dt_start_strp, datetime_strf)
dt_end_strf = (datetime.strftime(dt_end_strp, datetime_strf)).replace("0000", "2400")
now = datetime.strftime(datetime.now(), datetime_strf)
file_ts = datetime.strftime(datetime.now(), datetime_strf2)

diff = dt_end_strp - dt_start_strp

day_count = ceil((diff.days + 0.5))

interval_count = reading_per_day * day_count

reading_row_count = int((interval_count * field_length)/192)  # 192 bytes of reading per record

mde_filename = 'MV90_MDEF_LT_'+str(file_ts)+'_'+str(random.randint(1000, 5000))+'.MDE'

f = File(mde_filename)


def write_meter_rec():
    global rec_count
    rec_count += 1
    f.put_bint(f.get_name(), rec_length)
    f.put_bint(f.get_name(), meter_rec)
    f.put_string(f.get_name(), args.meter[0], 20)
    f.put_string(f.get_name(), "Customer01", 20)
    f.put_string(f.get_name(), "Address1", 20)
    f.put_string(f.get_name(), "Address2", 20)
    f.put_string(f.get_name(), args.nmi[0], 20)
    f.put_string(f.get_name(), "", 7)
    f.put_string(f.get_name(), len(args.reg), 4, 2)
    f.put_string(f.get_name(), "", 4)
    f.put_string(f.get_name(), dt_start_strf, 12)
    f.put_string(f.get_name(), dt_end_strf, 12)
    f.put_string(f.get_name(), "N", 1)
    f.put_string(f.get_name(), "", 72)


def write_channel_rec(chn1, uom1, mmult):
    global rec_count
    rec_count += 1
    f.put_bint(f.get_name(), rec_length)
    f.put_bint(f.get_name(), channel_rec)
    f.put_string(f.get_name(), args.meter[0], 20)
    f.put_string(f.get_name(), args.meter[0], 14)
    f.put_string(f.get_name(), "", 6)
    f.put_string(f.get_name(), args.meter[0], 12)
    f.put_string(f.get_name(), dt_start_strf, 12)
    f.put_string(f.get_name(), dt_end_strf, 12)
    f.put_string(f.get_name(), "000000000000", 12)
    f.put_string(f.get_name(), "N", 1)
    f.put_string(f.get_name(), chn1, 2)
    f.put_bint(f.get_name(), int(chn1))
    f.put_string(f.get_name(), translate_uom(uom1), 2)
    f.put_string(f.get_name(), "Y", 1)
    f.put_string(f.get_name(), "Y", 1)
    f.put_string(f.get_name(), "000000000000", 12)
    f.put_string(f.get_name(), "000000000000", 12)
    f.put_string(f.get_name(), "", 1)
    f.put_string(f.get_name(), '{:>010.3f}'.format(float(mmult)), 10)
    f.put_string(f.get_name(), "", 30)
    f.put_string(f.get_name(), "W", 1)
    f.put_string(f.get_name(), "", 10)
    if period == 30:
        f.put_string(f.get_name(), "02", 2)
    else:
        f.put_string(f.get_name(), "04", 2)
    f.put_string(f.get_name(), "", 12)
    f.put_string(f.get_name(), "NA", 2)
    f.put_string(f.get_name(), "AC", 2)
    f.put_string(f.get_name(), "", 15)
    f.put_string(f.get_name(), determine_dir(chn1, uom1), 1)
    f.put_bint(f.get_name(), 0)
    f.put_string(f.get_name(), "R", 1)
    f.put_string(f.get_name(), "", 2)


def write_channel_and_int_data_rec():
    global rec_count
    for channels in args.reg:
        for channel in channels:
            spchn, spuom = channel.split(':')
            write_channel_rec(spchn, spuom, "1")
            i = 1
            dt = dt_start_strp
            while i <= int(reading_row_count):
                f.put_bint(f.get_name(), rec_length)
                f.put_bint(f.get_name(), interval_rec + i)
                f.put_string(f.get_name(), args.meter[0], 20)
                j = 1
                while j <= 192/field_length:
                    if dt > dt_end_strp:
                        #  If no more data then fill the gap with Integer 32767 = FF7F
                        #       in Hex (Least Significant Byte Order)
                        f.put_bint(f.get_name(), 32767)
                        f.put_bint(f.get_name(), 32767)
                        f.put_bint(f.get_name(), 32767)
                        f.put_bint(f.get_name(), 32767)
                    else:
                        if args.sendzero is not None:
                            if args.sendzero[0] == 'Y':
                                f.put_bfloat(f.get_name(), 0)  # 4 bytes of float. Send 0 reading when flag is set to YES
                            else:
                                f.put_bfloat(f.get_name(), gen_rand(50, 100))
                        else:
                            f.put_bfloat(f.get_name(), gen_rand(50, 100))  # 4 bytes of float.
                        f.put_bint(f.get_name(), 0)  # 2 bytes of int
                        f.put_bint(f.get_name(), 0)  # 2 bytes of int
                    rec_count += 1
                    j += 1
                    dt += timedelta(minutes=period)
                i += 1


def write_trailer_rec():
    global rec_count
    rec_count += 1
    f.put_bint(f.get_name(), rec_length)
    f.put_bint(f.get_name(), trailer_rec)
    f.put_string(f.get_name(), "", 30)
    f.put_string(f.get_name(), '{:>010d}'.format(rec_count), 10)
    f.put_string(f.get_name(), "", 160)
    f.put_string(f.get_name(), now, 12)


# ==========Main Section=====================


write_meter_rec()
write_channel_and_int_data_rec()
write_trailer_rec()
print("File name is %s" % mde_filename)

