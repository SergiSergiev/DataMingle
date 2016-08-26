# Connect to SAP HANA account and then extract data
# input:
#     sensor_isnallation_id -> tupple = 57,58,59
#     choosen date - > string ="2016-08-21"
# Output:
#   table with columns SENSOR_INSTALLATION_ID, DATE_TIME, RSSI, SEQ_CTL, FRAME_TYPE, SUB_BITS
#    ORDER BY SOURCE, DATE_TIME, SEQ_CTL

import argparse
import csv
import socket
import sys

import pyhdb


def load_data(sensor_installation:tuple, current_date):
    try:
        db_connection = pyhdb.connect(host="52.58.251.227", port=30015, user='SYSTEM', password='a5_hS3aZ#')
        db_cursor = db_connection.cursor()
    except socket.error as why:
        print(why)
        sys.exit(1)
    try:
        current_day_time = current_date + ' 23:59:59.000'
        #print(current_day_time)
        select_statement = '''
        SELECT SOURCE, SENSOR_INSTALLATION_ID, DATE_TIME, RSSI, SEQ_CTL, FRAME_TYPE, SUB_BITS
        FROM "SHOPUP"."me.shopup.data::data"
        WHERE SENSOR_INSTALLATION_ID IN {sensors} AND
        DATE_TIME BETWEEN '{current_day}'  AND '{current_day_time}'
        ORDER BY SOURCE, DATE_TIME, SEQ_CTL '''.format (sensors = sensor_installation, current_day = current_date, current_day_time = current_day_time) #, [sensor_installation]

        #print(select_statement)
        db_cursor.execute(select_statement)
        selected_rows = db_cursor.fetchall()
        print('matching records count = {}'.format(len(selected_rows)))

        return selected_rows

    except pyhdb.exceptions.DatabaseError as why:
        print(why)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='load-data')
    args = parser.parse_args()



