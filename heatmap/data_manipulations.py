import math
from heatmap.triangulation import triangulation
from pprint import pprint

from heatmap.load_data import load_sensor_locations
routers_number = (57,58,59,60,61,62,63,64,65,66)

KEY_SOURCE = 0
KEY_SENSOR_ID = 1
KEY_DATA_TS = 2
KEY_RSSI = 3
KEY_SEQ_CTL = 4

freq_in_mhz = 2462

def create_time_frames (data_table:list) -> list:
    arranged_table = []
    routers_coordinates = load_sensor_locations(routers_number)

    source = None
    time_frame = None
    router_id_1 = None
    router_1_counter = None
    rssi_1 = None
    rssi_1_meters = None
    router_id_2 = None
    router_2_counter = None
    rssi_2 = None
    rssi_2_meters = None
    router_id_3 = None
    router_3_counter = None
    rssi_3 = None
    rssi_3_meters = None
    router_id_4 = None
    router_4_counter = None
    rssi_4 = None
    rssi_4_meters = None
    router_id_5 = None
    router_5_counter = None
    rssi_5 = None
    rssi_5_meters = None
    router_id_6 = None
    router_6_counter = None
    rssi_6 = None
    rssi_6_meters = None
    rssi_1_average = None
    rssi_2_average = None
    rssi_3_average = None
    rssi_4_average = None
    rssi_5_average = None
    rssi_6_average = None

    coordinate_x = None
    coordinate_y = None

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

            elif router_id_4 == None:
                router_id_4 = n[3]
                router_4_counter = 1
                rssi_4 = n[4]
            elif router_id_4 == n[3]:
                router_4_counter += 1
                rssi_4 = (rssi_4 + n[4])

            elif router_id_5 == None:
                router_id_5 = n[3]
                router_5_counter = 1
                rssi_5 = n[4]

            elif router_id_5 == n[3]:
                router_5_counter += 1
                rssi_5 = (rssi_5 + n[4])

            elif router_id_6 == n[3]:
                router_6_counter += 1
                rssi_6 = (rssi_6 + n[4])
            else:
                router_id_6 = n[3]
                router_6_counter = 1
                rssi_6 = n[4]



        elif source == None:
            source = n[0]
            time_frame = n[1]
            router_id_1 = n[3]
            router_1_counter = 1
            rssi_1 = n[4]
        else:

            if router_1_counter != None:
                rssi_1_average = rssi_1/router_1_counter
                lat_A = routers_coordinates[router_id_1][0]
                lon_A = routers_coordinates[router_id_1][1]

            if router_2_counter != None:
                rssi_2_average = rssi_2/router_2_counter
                lat_B = routers_coordinates[router_id_2][0]
                lon_B = routers_coordinates[router_id_2][1]

            if router_3_counter != None:
                rssi_3_average = rssi_3/router_3_counter
                lat_C = routers_coordinates[router_id_3][0]
                lon_C = routers_coordinates[router_id_3][1]
                rssi_1_meters = compute_distance(rssi_1_average)
                rssi_2_meters = compute_distance(rssi_2_average)
                rssi_3_meters = compute_distance(rssi_3_average)

                coordinates = triangulation(float(lat_A),float (lon_A), float (lat_B),float (lon_B),
                                            float (lat_C), float (lon_C), rssi_1_meters, rssi_2_meters, rssi_3_meters)
                coordinate_x = coordinates[0]
                coordinate_y = coordinates[1]

            if router_4_counter != None:
                rssi_4_average = rssi_4/router_4_counter
                rssi_4_meters = compute_distance(rssi_4_average)
                if coordinate_x == None:
                    lat_D = routers_coordinates[router_id_4][0]
                    lon_D = routers_coordinates[router_id_4][1]
                    coordinates = triangulation(float(lat_A), float(lon_A), float(lat_B), float(lon_B),
                                                float(lat_D), float(lon_D), rssi_1_meters, rssi_2_meters, rssi_4_meters)
                    coordinate_x = coordinates[0]
                    coordinate_y = coordinates[1]

            if router_5_counter != None:
                rssi_5_average = rssi_5/router_5_counter
                rssi_5_meters = compute_distance(rssi_5_average)
                if coordinate_x == None:
                    lat_E = routers_coordinates[router_id_5][0]
                    lon_E = routers_coordinates[router_id_5][1]
                    coordinates = triangulation(float(lat_A), float(lon_A), float(lat_B), float(lon_B),
                                                float(lat_E), float(lon_E), rssi_1_meters, rssi_2_meters, rssi_5_meters)
                    coordinate_x = coordinates[0]
                    coordinate_y = coordinates[1]

            if router_6_counter != None:
                rssi_6_average = rssi_6/router_6_counter
                rssi_6_meters = compute_distance(rssi_6_average)
                if coordinate_x == None:
                    lat_F = routers_coordinates[router_id_6][0]
                    lon_F = routers_coordinates[router_id_6][1]
                    coordinates = triangulation(float(lat_A), float(lon_A), float(lat_B), float(lon_B),
                                                float(lat_F), float(lon_F), rssi_1_meters, rssi_2_meters, rssi_6_meters)
                    coordinate_x = coordinates[0]
                    coordinate_y = coordinates[1]


            arranged_table.append((source, time_frame,
                                   router_id_1, rssi_1_average, router_1_counter, rssi_1_meters,
                                   router_id_2, rssi_2_average, router_2_counter, rssi_2_meters,
                                   router_id_3, rssi_3_average, router_3_counter, rssi_3_meters,
                                   router_id_4, rssi_4_average, router_4_counter, rssi_4_meters,
                                   router_id_5, rssi_5_average, router_5_counter, rssi_5_meters,
                                   router_id_6, rssi_6_average, router_6_counter, rssi_6_meters,
                                   coordinate_x, coordinate_y
                                   ))
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
            router_id_5 = None
            router_5_counter = None
            rssi_5 = None
            router_id_6 = None
            router_6_counter = None
            rssi_6 = None
            rssi_1_average = None
            rssi_2_average = None
            rssi_3_average = None
            rssi_4_average = None
            rssi_5_average = None
            rssi_6_average = None
            rssi_2_meters = None
            rssi_3_meters = None
            rssi_4_meters = None
            rssi_5_meters = None
            rssi_6_meters = None
            coordinate_x = None
            coordinate_y = None

    return arranged_table



def report(time_frames_records):
    total = len(time_frames_records)
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0
    count_6 = 0
    for n in time_frames_records:
        if n [2]!= None and n[6] == None :
            count_1 +=1
        if n[6] != None and n[10] == None:
            count_2 += 1
        if n[10] != None and n [14] == None:
            count_3 += 1
        if n[14] != None and n[18] == None:
            count_4 += 1
        if n[18] != None and n[22] == None:
            count_5 += 1
        if n[22] != None:
            count_6 += 1


    #pprint(time_frames_records)
    print('''
    total No: {}
    No of records 1: {}
    No of records 2: {}
    No of records 3: {}
    No of records 4: {}
    No of records 5: {}
    No of records 6: {}
    % of 1: {:.4f} %
    % of 2: {:.4f} %
    % of 3: {:.4f} %
    % of 4: {:.4f} %
    % of 5: {:.4f} %
    % of 6: {:.4f} %
    '''.format(total, count_1,count_2, count_3, count_4, count_5, count_6, count_1/total*100, count_2/total*100, count_3/total*100, count_4/total*100, count_5/total*100,count_6/total*100))

def create_list(data_table:tuple, approx_in_sec) -> list :

    sorted_table = []
    for n in data_table:
        date_time = n[KEY_DATA_TS].replace( microsecond=0)
        seconds_as = int(date_time.strftime('%S'))
        date_time = date_time.replace(second=seconds_as - seconds_as % approx_in_sec)

        source = n[KEY_SOURCE]
        sensor_id = n[KEY_SENSOR_ID]
        rssi = n[KEY_RSSI]
        seq_ctl = n[KEY_SEQ_CTL]

        sorted_table.append((source,  date_time, seq_ctl, sensor_id, rssi ))
    return sorted_table

def compute_distance (level_in_db)-> int:
    meters = float()
    '''
    free-space path loss (FSPL)
    For typical radio applications, it is common to find f measured in units of GHz and d in km, in which case the FSPL equation becomes

    =20\log _{10}(d)+20\log _{10}(f)+92.45} \ =20\log _{{10}}(d)+20\log _{{10}}(f)+92.45
    For d,f in meters and kilohertz, respectively, the constant becomes  -87.55 .

    For  d,f in meters and megahertz, respectively, the constant becomes -27.55 .

    For d,f in kilometers and megahertz, respectively, the constant becomes  32.45 .
    https://en.wikipedia.org/wiki/Free-space_path_loss#Free-space_path_loss_in_decibels
    '''
 #   try:
    try:
        result = (27.55 - (20 * math.log10(freq_in_mhz)) + math.fabs(level_in_db)) / 20.0
        meters = math.pow(10, result)/1000

    except:
        meters = None
    return meters


#    except:
 #       meters = None
#    feet = meters * 3.2808

# p = compute_distance(-60)
# print(p)