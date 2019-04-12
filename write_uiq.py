import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from xml.sax.saxutils import escape
import sqlite3
from sqlite3 import Error


# def create_connection(db_file):
#     try:
#         conn = sqlite3.connect(db_file)
#     except Error as e:
#         print(e)
#     finally:
#         conn.close()


# if __name__ == '__main__':
#     create_connection('uiq.db')


def prettyfy(element):
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

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
                    "CreationTime": "2019-04-09T12:30:56.745+08:00",
                    "StartTime": "2019-04-09T00:00:00.000+08:00",
                    "EndTime": "2019-04-09T12:00:00.000+08:00",
                    "Version": "0.1"
                    }

meterdataattr = {"MeterName": "0530002671", "MacID": "00:13:50:03:00:01:3d:2b", 
                        "UtilDeviceID": "0530002671"}
intreaddataattr = {"IntervalLength": "30", "StartTime":
                            "2019-04-09T00:00:00.000+08:00", 
                    "EndTime": "2019-04-09T12:00:00.000+08:00",
                            "NumberIntervals": "24"}

root = ET.Element("n:SSNExportDocument", attrib=ssnexportdocattr)
meterdata = ET.SubElement(root, "n:MeterData", attrib=meterdataattr)
intreaddata = ET.SubElement(meterdata, "n:IntervalReadData", 
                            attrib=intreaddataattr) 

with open("filename.xml", "w") as f:
    f.write(prettyfy(root))
   