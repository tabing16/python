import csv
from datetime import datetime
from datetime import timedelta

row_count = 0

with open('mtr_data2.csv', 'r') as f:  
    row_count = sum(1 for row in csv.reader(f)) - 1

with open('mtr_data2.csv','r') as f2:
    csv_reader = csv.DictReader(f2)
    for i, row in enumerate(csv_reader):
        if i == 1: 
            print(row)
        if i == row_count - 1:
            print(row)

    # for items in csv_reader:
    #     print(f'<n:Reading Channel="{items["ID_CHN_01"]}" RawValue="0" Value="{items["RDG_CHN_01"]} UOM="{items["UOM_01"]}"/>')
    #     print(f'<n:Reading Channel="{items["ID_CHN_02"]}" RawValue="0" Value="{items["RDG_CHN_02"]} UOM="{items["UOM_02"]}"/>')
    #     print(f'<n:Reading Channel="{items["ID_CHN_03"]}" RawValue="0" Value="{items["RDG_CHN_03"]} UOM="{items["UOM_03"]}"/>')
    #     print(f'<n:Reading Channel="{items["ID_CHN_04"]}" RawValue="0" Value="{items["RDG_CHN_04"]} UOM="{items["UOM_04"]}"/>')
    #     print(f'<n:Reading Channel="{items["ID_CHN_05"]}" RawValue="0" Value="{items["RDG_CHN_05"]} UOM="{items["UOM_05"]}"/>')
