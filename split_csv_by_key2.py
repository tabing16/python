import csv
import os
from itertools import groupby
import operator
import logging
from logging.handlers import RotatingFileHandler


def check_single_file(directory, csvextension):
    single_file = True
    # root_dir = os.path.join('dist','csv')
    extensions = csvextension
    files_arr = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[-1]
            if ext in extensions:
                files_arr.append(files)
    if(len(files_arr) != 1):
        single_file = False
    return single_file

csv_folder = 'csv'
output_folder = 'output'
csv_filename = 'mtr_data5.csv'
log_folder = 'log'
log_filename = 'file.log'

mykey = []
header = []

logger = logging.getLogger(os.path.relpath(__file__))  # get current script name. Relative Path.
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(os.path.join(log_folder, log_filename),
                            maxBytes=2000,
                            backupCount=10
                            )
handler.setFormatter(formatter)
logger.addHandler(handler)

if check_single_file(csv_folder, csv_filename):
    try:
        with open(os.path.join(csv_folder, csv_filename), 'r') as f:
            header = f.readlines(1)  # get header
            next(f)  # but dont include header into csv.reader
            reader = csv.reader(f)

            for key, rows in groupby(reader, operator.itemgetter(1)):
                mykey.append(key)  # collect all the keys
    except IOError:
        print(f'Failed. input file {csv_filename} cannot be located')
        logger.error(f'Failed. input file {csv_filename} cannot be located')

    # proceed only if there is an item in mykey array
    if mykey:
        for key, rows in groupby(csv.reader(open(os.path.join(csv_folder, csv_filename))), operator.itemgetter(1)):
            # if the key is in the mykey array then write to file
            if key in mykey:
                try:
                    with open(os.path.join(csv_folder, output_folder, "%s.csv" % key), "w") as output:
                        output.write(",".join(header))    
                        for row in rows:
                            output.write(",".join(row) + "\n")
                    logger.info(f'Successfully written file {key}.csv in {output_folder}')
                except IOError:
                    print(f'Failed to write file output')
                    logger.error(f'Failed to write file output')
else:
    logger.error('Failed. More than 1 csv file detected')

