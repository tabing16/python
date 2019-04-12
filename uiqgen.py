import os
import csv
import random
from datetime import timedelta
from datetime import datetime
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except OSError:
        print(f'creation of {csv_folder} folder failed')


def folder_exists(folder_name):
    folder_exists = True
    if not os.path.exists(folder_name):
        folder_exists = False
    return folder_exists


csv_folder = 'csv'
uiq_folder = 'uiq'
strptime_format = "%d/%b/%Y %H:%M"
strftime_format = "%Y-%m-%dT%H:%M"
uiq_time_suffix = ":00.000+08:00"
now = datetime.strftime(datetime.now(), strftime_format) + uiq_time_suffix

uiq_file = os.path.join(uiq_folder, 'SSPN_SSNE_' + datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + '_' + str(random.randint(1000, 5000)) + '.uiq')


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


'''Beautify the XML output'''
def prettyfy(element):
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


'''This is to get the last timestamp from the csv file'''
def get_line_count(filename):
    with open(filename, 'r') as f:  
        row_count = sum(1 for row in csv.reader(f)) - 1
    return row_count


'''This is to get supply point(sp) detail from the csv file  '''
def get_sp_detail(filename):
    sp = {}
    row_count = get_line_count(filename)
    with open(filename, 'r') as f2:
        csv_reader = csv.DictReader(f2)
        for i, row in enumerate(csv_reader):
            if i == 0: 
                sp['nmi'] = row['NMI']
                sp['mtr'] = row['MTR']
                sp['datestart'] = row['TS']
                sp['rdpday'] = row['RDPDAY']
                sp['no_of_rows'] = row_count
            if i == row_count - 1:
                sp['dateend'] = (row['TS'])
    return sp

'''UIQ App has certain time format. We must comply with the format so that uiq file can be processed by MBS HUB'''
def convert_to_uiq_time(t):
    input_t = datetime.strptime(t, strptime_format)
    converted_t = datetime.strftime(input_t, strftime_format)
    return converted_t + uiq_time_suffix


if check_single_file(csv_folder, '.csv'):
    if not folder_exists(uiq_folder):
        create_folder(uiq_folder)

    for root, dirs, files in os.walk(csv_folder):
        input_file = files[0]            
    #print(input_file)

    csv_file = os.path.join(csv_folder, input_file)

    sp_detail = get_sp_detail(csv_file)
    mtr = sp_detail['mtr']
    no_of_rec = sp_detail['no_of_rows']
    rdp = sp_detail['rdpday']
    datestart = convert_to_uiq_time(sp_detail['datestart'])
    dateend = convert_to_uiq_time(sp_detail['dateend'])

    ssnexportdocattr = {"xmlns:n": "urn:com:ssn:schema:export:SSNExportFormat.xsd",
                        "xmlns": "urn:com:ssn:schema:export:SSNExportFormat.xsd",
                        "xmlns:wp": "http://www.westernpower.com.au",
                        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                        "xsi:schemaLocation": "urn:com:ssn:schema:export:\
                            SSNExportFormat.xsd ../../SSNExportFormat.xsd",
                        "DocumentID": "8339ee98-8e43-4fe6-9950-af61e11c18dc-2",
                        "ExportID": "8339ee98-8e43-4fe6-9950-af61e11c18dc",
                        "JobID": "4059155",
                        "RunID": "31164047",
                        "CreationTime": ""+now+"",
                        "StartTime": ""+datestart+"",
                        "EndTime": ""+dateend+"",
                        "Version": "0.1"
                        }

    meterdataattr = {"MeterName": ""+mtr+"", "MacID": "00:13:50:03:00:01:3d:2b", 
                            "UtilDeviceID": ""+mtr+""}
    intreaddataattr = {"IntervalLength": ""+rdp+"", "StartTime": ""+datestart+"",  
                        "EndTime": ""+dateend+"", "NumberIntervals": ""+str(no_of_rec)+""}

    root = ET.Element("n:SSNExportDocument", attrib=ssnexportdocattr)
    meterdata = ET.SubElement(root, "n:MeterData", attrib=meterdataattr)
    intreaddata = ET.SubElement(meterdata, "n:IntervalReadData", 
                                attrib=intreaddataattr) 

    j = 1

    with open(csv_file,'r') as f3:
        csv_reader = csv.DictReader(f3)
        for items in csv_reader:
            interval = ET.SubElement(intreaddata, "n:Interval", attrib={"EndTime": convert_to_uiq_time(items['TS']),
                                            "BlockSequenceNumber": "1", "IntervalSequenceNumber" : str(j),
                                            "GatewayCollectedTime": now
                                            })
            if(items["ID_CHN_01"]):
                ET.SubElement(interval, "n:Reading", attrib={"Channel":  items["ID_CHN_01"], "RawValue": "0", "Value": str(items["RDG_CHN_01"]), "UOM": items["UOM_01"]})
            if(items["ID_CHN_02"]):
                ET.SubElement(interval, "n:Reading", attrib={"Channel":  items["ID_CHN_02"], "RawValue": "0", "Value": str(items["RDG_CHN_02"]), "UOM": items["UOM_02"]})
            if(items["ID_CHN_03"]):
                ET.SubElement(interval, "n:Reading", attrib={"Channel":  items["ID_CHN_03"], "RawValue": "0", "Value": str(items["RDG_CHN_03"]), "UOM": items["UOM_03"]})
            if(items["ID_CHN_04"]):
                ET.SubElement(interval, "n:Reading", attrib={"Channel":  items["ID_CHN_04"], "RawValue": "0", "Value": str(items["RDG_CHN_04"]), "UOM": items["UOM_04"]})
            if(items["ID_CHN_05"]):
                ET.SubElement(interval, "n:Reading", attrib={"Channel":  items["ID_CHN_05"], "RawValue": "0", "Value": str(items["RDG_CHN_05"]), "UOM": items["UOM_05"]})
            j += 1

    with open(uiq_file, "w") as f:
        f.write(prettyfy(root))

    print(f'Success. file name is {uiq_file}')
else:
    print(f'Failed. Make sure only 1 csv file exists')