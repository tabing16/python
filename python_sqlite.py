import sqlite3
from sqlite3 import Error
import csv


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    finally:
        conn.close()    
    return None


def create_table(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

con = sqlite3.connect("uiq.db")
cur = con.cursor()
del_sql = 'DELETE FROM MTR_DATA'

with open('mtr_data.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['NMI'], i['MTR'], i['TARIFF'], i['TS'], i['RDPDAY'], 
        i['RDP_CHANGE_STAT'],
        i['RDG_CHN_01'], i['UOM_01'], i['LAG_UOM_01'], i['UOM_CHANGE_STAT_01'],
        i['RDG_CHN_02'], i['UOM_02'], i['LAG_UOM_02'], i['UOM_CHANGE_STAT_02'],
        i['RDG_CHN_03'], i['UOM_03'], i['LAG_UOM_03'], i['UOM_CHANGE_STAT_03'],
        i['RDG_CHN_04'], i['UOM_04'], i['LAG_UOM_04'], i['UOM_CHANGE_STAT_04'],
        i['RDG_CHN_05'], i['UOM_05'], i['LAG_UOM_05'], i['UOM_CHANGE_STAT_05']) 
        for i in dr]

# clear the Table before loading with data
cur.execute(del_sql) 
cur.executemany("INSERT INTO MTR_DATA VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                            ?,?,?,?,?,?,?,?,?);", to_db)
con.commit()
con.close()
