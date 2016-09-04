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

import pyhdb

from gridgen import Point


def load_data(sensor_installation, start_date_time, end_date_time):
    try:
        db_connection = pyhdb.connect(host="52.58.251.227", port=30015, user='SYSTEM', password='a5_hS3aZ#')
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
        DATE_TIME BETWEEN '{start_date_time}'  AND '{end_day_time}'
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
    points = [Point(42.62393886817023, 23.353757702944623),
              Point(42.624138028085596, 23.35380489989459),
              Point(42.62422073744083, 23.353947437337943),
              Point(42.624388399629474, 23.353756414412317),
              Point(42.624436167476794, 23.353614560506056),
              Point(42.62427910733995, 23.353533576499174),
              Point(42.62433254398108, 23.35328365611738),
              Point(42.62420477560003, 23.353273270369936),
              Point(42.624065669596334, 23.353479017555472),
              Point(42.623909344542184, 23.353453907296416)]

    result = dict()
    match = zip(sensors, points)
    for id, p in match:
        result[id] = p
        # print(result)
    return result

    # try:
    #     db_connection = pyhdb.connect(host="52.58.251.227", port=30015, user='SYSTEM', password='a5_hS3aZ#')
    #     db_cursor = db_connection.cursor()
    # except socket.error as why:
    #     print(why)
    #     sys.exit(1)
    # try:
    #     # print(current_day_time)
    #     select_statement = '''
    #     SELECT ID, COORDINATES_NORTH, COORDINATES_EAST
    #     FROM "SHOPUP"."me.shopup.data::sensor_installations"
    #     WHERE ID IN {sensors}
    #     ORDER BY ID '''.format(sensors=sensors)
    #
    #     # print(select_statement)
    #     db_cursor.execute(select_statement)
    #     selected_rows = db_cursor.fetchall()
    #     result = dict()
    #     for id, c1, c2 in selected_rows:
    #         result[id] = Point(c1, c2)
    #         # print(result)
    #     return result
    #
    # except pyhdb.exceptions.DatabaseError as why:
    #     print(why)
    #     sys.exit(1)