from datetime import datetime
from math import ceil

dt_start = "01-01-2019 00:15"
dt_end = "01-01-2019 02:00"
datetime_strp = "%d-%m-%Y %H:%M"
datetime_strf = "%Y%m%d%H%M"

dt_start_strp = datetime.strptime(dt_start, datetime_strp)
dt_end_strp = datetime.strptime(dt_end, datetime_strp)

dt_start_strf = datetime.strftime(dt_start_strp,datetime_strf)
dt_end_strf = datetime.strftime(dt_end_strp,datetime_strf)

#print(dt_start_strf);
#print(dt_end_strf.replace('0000','2400'));

diff = dt_end_strp - dt_start_strp

#diff_in_minutes = (diff.days * 1440 + diff.seconds/60)

day_count = ceil((diff.days + 0.5))

print("Day Count: " + str(day_count))

interval_count = 96 * day_count

#print("Interval Count: " + str(interval_count))

#4 bytes interval readings, 2 bytes channel stat, 2 bytes interval stat. Total = 8
reading_row_count = int((interval_count * 4)/192) # 192 bytes of reading per record

print("Reading Row Count: " + str(int(reading_row_count)))

i = 1
j = 1

while i <= int(reading_row_count):
    print(1000 + i)
    # while j <= 192/4:
    #     print(j)
    #     j += 1
    i += 1
