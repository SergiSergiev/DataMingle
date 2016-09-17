# Connect to SAP HANA account and then extract data
# the hour can be modified for small ranges
# input:
#     sensor_isnallation_id -> tupple = 57,58,59
#     choosen date - > string ="2016-08-21"
# Output:
#   table with columns SENSOR_INSTALLATION_ID, DATE_TIME, RSSI, SEQ_CTL, FRAME_TYPE, SUB_BITS
#    ORDER BY SOURCE, DATE_TIME, SEQ_CTL

import socket
import sys
import platform
import pyhdb

from gridgen import Point


def load_data(sensor_installation, start_date_time, end_date_time):
    host_name = platform.node()
    host = "127.0.0.1" if host_name == 'sid-hdb' else "52.58.251.227"
    try:
        db_connection = pyhdb.connect(host=host, port=30015, user='SYSTEM', password='a5_hS3aZ#')
        db_cursor = db_connection.cursor()
    except socket.error as why:
        print(why)
        sys.exit(1)
    try:
        # print(current_day_time)
        select_statement = '''
        SELECT SOURCE, SENSOR_INSTALLATION_ID, DATE_TIME, RSSI
        FROM "SHOPUP"."me.shopup.data::data"
        WHERE SENSOR_INSTALLATION_ID IN {sensors} AND
        DATE_TIME BETWEEN '{start_date_time}'  AND '{end_day_time}' AND
        IS_STA = 1
        ORDER BY SOURCE, DATE_TIME '''.format(sensors=sensor_installation, start_date_time=start_date_time,
                                              end_day_time=end_date_time)

        # print(select_statement)
        db_cursor.execute(select_statement)
        selected_rows = db_cursor.fetchall()

        return selected_rows

    except pyhdb.exceptions.DatabaseError as why:
        print(why)
        sys.exit(1)


def load_sensor_locations(sensors):
    host_name = platform.node()
    host = "127.0.0.1" if host_name == 'sid-hdb' else "52.58.251.227"
    try:
        db_connection = pyhdb.connect(host=host, port=30015, user='SYSTEM', password='a5_hS3aZ#')
        db_cursor = db_connection.cursor()
    except socket.error as why:
        print(why)
        sys.exit(1)
    try:
        # print(current_day_time)
        select_statement = '''
        SELECT ID, COORDINATES_NORTH, COORDINATES_EAST
        FROM "SHOPUP"."me.shopup.data::sensor_installations"
        WHERE ID IN {sensors}
        ORDER BY ID '''.format(sensors=sensors)

        # print(select_statement)
        db_cursor.execute(select_statement)
        selected_rows = db_cursor.fetchall()
        result = dict()
        for id, c1, c2 in selected_rows:
            result[id] = Point(c1, c2)
            # print(result)
        return result

    except pyhdb.exceptions.DatabaseError as why:
        print(why)
        sys.exit(1)
