'''
1. Load device record from all sensors ordered by TS + identificator(krasi) - 3 % - Krasi
2. Define time_frame TF - Set or list
3. Gather sensor records per TF - list or Dict
4. Compute coordinates - x1, y1, p1, ts, x2, y2, p2
5. Convert to geo-coordinates
6. Save on DB
'''
import iso8601
from pprint import pprint

from heatmap.load_data import load_data
from datetime import datetime

KEY_SOURCE = 0
KEY_SENSOR_ID = 1
KEY_DATA_TS = 2
KEY_RSSI = 3
KEY_SEQ_CTL = 4

def main():

    db_records_sensor_date = load_data((57,58,59,60,61,62,63,64,65,66), "2016-08-21")
    round_by_sec = create_list(db_records_sensor_date)
    time_frames_records = create_time_frames(round_by_sec)
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    for n in time_frames_records:
        if n [2]!= None:
            count_1 +=1
        if n[5] != None:
            count_2 += 1
        if n[8] != None:
            count_3 += 1
        if n[11] != None:
            count_4 += 1
    #pprint(time_frames_records)
    print('''
    No of records 1: {}
    No of records 2: {}
    No of records 3: {}
    No of records 4: {}
    % of 2: {:.4f} %
    % of 3: {:.4f} %
    % of 4: {:.4f} %
    '''.format(count_1,count_2, count_3, count_4, count_2/count_1*100, count_3/count_1*100, count_4/count_1*100))

def create_list(data_table:tuple) -> list :
    approximation = 60
    sorted_table = []
    print(sorted_table)
    for idx, n in enumerate (data_table):
        date_time = n[KEY_DATA_TS].replace( microsecond=0)
        seconds_as = int(date_time.strftime('%S'))
        date_time = date_time.replace(second=seconds_as - seconds_as % approximation)

        source = n[KEY_SOURCE]
        sensor_id = n[KEY_SENSOR_ID]
        rssi = n[KEY_RSSI]
        seq_ctl = n[KEY_SEQ_CTL]

        sorted_table.append((source,  date_time, seq_ctl, sensor_id, rssi ))
    return sorted_table

def create_time_frames (data_table:list) -> list:
    arranged_table = []
    source = None
    time_frame = None
    router_id_1 = None
    router_1_counter = None
    rssi_1 = None
    router_id_2 = None
    router_2_counter = None
    rssi_2 = None
    router_id_3 = None
    router_3_counter = None
    rssi_3 = None
    router_id_4 = None
    router_4_counter = None
    rssi_4 = None
    rssi_1_average = None
    rssi_2_average = None
    rssi_3_average = None
    rssi_4_average = None

    for idx, n in enumerate(data_table):
        if source == n[0] and time_frame == n[1]:
            if router_id_1 == None:
                router_id_1 = n [3]
                router_1_counter = 1
                rssi_1 = n [4]

            elif router_id_1 == n[3]:
                router_1_counter += 1
                rssi_1 = (rssi_1 + n[4])
            elif router_id_2 == None:
                router_id_2 = n [3]
                router_2_counter = 1
                rssi_2 = n [4]
            elif router_id_2 == n[3]:
                router_2_counter += 1
                rssi_2 = (rssi_2 + n[4])
            elif router_id_3 == None:
                router_id_3 = n[3]
                router_3_counter = 1
                rssi_3 = n[4]
            elif router_id_3 == n[3]:
                router_3_counter += 1
                rssi_3 = (rssi_3 + n[4])
            elif router_id_4 == n[3]:
                router_4_counter += 1
                rssi_4 = (rssi_4 + n[4])
            else:
                router_id_4 = n[3]
                router_4_counter = 1
                rssi_4 = n[4]
        elif source == None:
            source = n[0]
            time_frame = n[1]
            router_id_1 = n[3]
            router_1_counter = 1
            rssi_1 = n[4]
        else:
            if router_1_counter != None:
                rssi_1_average = rssi_1/router_1_counter
            if router_2_counter != None:
                rssi_2_average = rssi_2/router_2_counter
            if router_3_counter != None:
                rssi_3_average = rssi_3/router_3_counter
            if router_4_counter != None:
                rssi_4_average = rssi_4/router_4_counter

            arranged_table.append((source,time_frame, router_id_1, rssi_1_average, router_1_counter, router_id_2,
                                  rssi_2_average, router_2_counter, router_id_3, rssi_3_average, router_3_counter,
                                   router_id_4, rssi_4_average, router_4_counter))
            source = n[0]
            time_frame = n[1]
            router_id_1 = n[3]
            router_1_counter = 1
            rssi_1 = n [4]
            router_id_2 = None
            router_2_counter = None
            rssi_2 = None
            router_id_3 = None
            router_3_counter = None
            rssi_3 = None
            router_id_4 = None
            router_4_counter = None
            rssi_4 = None
            rssi_1_average = None
            rssi_2_average = None
            rssi_3_average = None
            rssi_4_average = None
    return arranged_table





if __name__ == '__main__':
    main()