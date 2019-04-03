from datetime import datetime
 
date_format = "%d-%m-%Y %H:%M:%S"

time1  = datetime.strptime('01-01-2008 00:00:00', date_format)
time2  = datetime.strptime('02-01-2008 00:30:00', date_format)

diff = time2 - time1

diff_in_minutes = (diff.days * 1440 + diff.seconds/60)

print(str(diff_in_minutes) + ' minutes')
