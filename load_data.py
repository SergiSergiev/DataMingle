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


def load_data(sensor_installation:tuple, current_date, current_hour):
    try:
        db_connection = pyhdb.connect(host="52.58.251.227", port=30015, user='SYSTEM', password='a5_hS3aZ#')
        db_cursor = db_connection.cursor()
    except socket.error as why:
        print(why)
        sys.exit(1)
    try:
        current_day_time = current_date + ' ' + current_hour
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

def load_sensor_locations(sensors:tuple) -> dict:
    try:
        db_connection = pyhdb.connect(host="52.58.251.227", port=30015, user='SYSTEM', password='a5_hS3aZ#')
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

        #print(select_statement)
        db_cursor.execute(select_statement)
        selected_rows = db_cursor.fetchall()
        result=dict()
        for id,c1,c2 in selected_rows:
            result [id] = (c1, c2)
            #print(result)
        return result

    except pyhdb.exceptions.DatabaseError as why:
        print(why)
        sys.exit(1)

#q = load_sensor_locations((56,57))
# print(q)
#print( q[56][1] )
#p = q.keys()
#print(p)

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='load-data')
    args = parser.parse_args()


