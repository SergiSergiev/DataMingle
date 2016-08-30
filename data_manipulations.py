import math

from load_data import load_sensor_locations
from triangulation import triangulation


KEY_SOURCE = 0
KEY_SENSOR_ID = 1
KEY_DATA_TS = 2
KEY_RSSI = 3

freq_in_mhz = 2462
TABLE_DB_TO_METERS = [0.009688, 0.010870, 0.012196, 0.013684, 0.015354, 0.017227, 0.019329, 0.021688,
                      0.024334, 0.027303, 0.030635, 0.034373, 0.038567, 0.043272, 0.048553, 0.054477,
                      0.061124, 0.068582, 0.076951, 0.086340, 0.096875, 0.108696, 0.121958, 0.136840,
                      0.153537, 0.172271, 0.193291, 0.216876, 0.243339, 0.273031, 0.306346, 0.343726,
                      0.385667, 0.432725, 0.485525, 0.544768, 0.611240, 0.685823, 0.769506, 0.863400,
                      0.968751, 1.086956, 1.219585, 1.368396, 1.535366, 1.722709, 1.932911, 2.168762,
                      2.433391, 2.730310, 3.063458, 3.437257, 3.856665, 4.327250, 4.855254, 5.447685,
                      6.112403, 6.858229, 7.695059, 8.633998, 9.687505, 10.869560, 12.195847, 13.683965,
                      15.353661, 17.227091, 19.329114, 21.687623, 24.333913, 27.303099, 30.634581, 34.372566,
                      38.566653, 43.272496, 48.552540, 54.476845, 61.124026, 68.582285, 76.950590, 86.339982,
                      96.875053, 108.695597, 121.958466, 136.839649, 153.536611, 172.270911, 193.291142, 216.876228,
                      243.339130, 273.030995, 306.345815, 343.725658, 385.666531, 432.724965, 485.525396, 544.768455,
                      611.240259, 685.822851, 769.505895, 863.399815]


def create_time_frames(data_table, routers_number):
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

    for n in data_table:
        if source == n[0] and time_frame == n[1]:
            if router_id_1 == None:
                router_id_1 = n[2]
                router_1_counter = 1
                rssi_1 = n[3]

            elif router_id_1 == n[2]:
                router_1_counter += 1
                rssi_1 = (rssi_1 + n[3])
            elif router_id_2 == None:
                router_id_2 = n[2]
                router_2_counter = 1
                rssi_2 = n[3]
            elif router_id_2 == n[2]:
                router_2_counter += 1
                rssi_2 = (rssi_2 + n[3])
            elif router_id_3 == None:
                router_id_3 = n[2]
                router_3_counter = 1
                rssi_3 = n[3]
            elif router_id_3 == n[2]:
                router_3_counter += 1
                rssi_3 = (rssi_3 + n[3])

            elif router_id_4 == None:
                router_id_4 = n[2]
                router_4_counter = 1
                rssi_4 = n[3]
            elif router_id_4 == n[2]:
                router_4_counter += 1
                rssi_4 = (rssi_4 + n[3])

            elif router_id_5 == None:
                router_id_5 = n[2]
                router_5_counter = 1
                rssi_5 = n[3]

            elif router_id_5 == n[2]:
                router_5_counter += 1
                rssi_5 = (rssi_5 + n[3])

            elif router_id_6 == n[2]:
                router_6_counter += 1
                rssi_6 = (rssi_6 + n[3])
            else:
                router_id_6 = n[2]
                router_6_counter = 1
                rssi_6 = n[3]



        elif source == None:
            source = n[0]
            time_frame = n[1]
            router_id_1 = n[2]
            router_1_counter = 1
            rssi_1 = n[3]
        else:

            if router_1_counter:
                rssi_1_average = rssi_1 / router_1_counter
                lat_A = routers_coordinates[router_id_1][0]
                lon_A = routers_coordinates[router_id_1][1]

            if router_2_counter:
                rssi_2_average = rssi_2 / router_2_counter
                lat_B = routers_coordinates[router_id_2][0]
                lon_B = routers_coordinates[router_id_2][1]

            if router_3_counter:
                rssi_3_average = rssi_3 / router_3_counter
                lat_C = routers_coordinates[router_id_3][0]
                lon_C = routers_coordinates[router_id_3][1]
                rssi_1_meters = compute_distance(rssi_1_average)
                rssi_2_meters = compute_distance(rssi_2_average)
                rssi_3_meters = compute_distance(rssi_3_average)

                coordinates = triangulation(float(lat_A), float(lon_A), float(lat_B), float(lon_B),
                                            float(lat_C), float(lon_C), rssi_1_meters, rssi_2_meters, rssi_3_meters)
                coordinate_x = coordinates[0]
                coordinate_y = coordinates[1]

            if router_4_counter:
                rssi_4_average = rssi_4 / router_4_counter
                rssi_4_meters = compute_distance(rssi_4_average)
                if not coordinate_x:
                    lat_D = routers_coordinates[router_id_4][0]
                    lon_D = routers_coordinates[router_id_4][1]
                    coordinates = triangulation(float(lat_A), float(lon_A), float(lat_B), float(lon_B),
                                                float(lat_D), float(lon_D), rssi_1_meters, rssi_2_meters, rssi_4_meters)
                    coordinate_x = coordinates[0]
                    coordinate_y = coordinates[1]

            if router_5_counter:
                rssi_5_average = rssi_5 / router_5_counter
                rssi_5_meters = compute_distance(rssi_5_average)
                if not coordinate_x:
                    lat_E = routers_coordinates[router_id_5][0]
                    lon_E = routers_coordinates[router_id_5][1]
                    coordinates = triangulation(float(lat_A), float(lon_A), float(lat_B), float(lon_B),
                                                float(lat_E), float(lon_E), rssi_1_meters, rssi_2_meters, rssi_5_meters)
                    coordinate_x = coordinates[0]
                    coordinate_y = coordinates[1]

            if router_6_counter:
                rssi_6_average = rssi_6 / router_6_counter
                rssi_6_meters = compute_distance(rssi_6_average)
                if not coordinate_x:
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
            router_id_1 = n[2]
            router_1_counter = 1
            rssi_1 = n[3]
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
        if n[2] and not n[6]:
            count_1 += 1
        if n[6] and not n[10]:
            count_2 += 1
        if n[10] and not n[14]:
            count_3 += 1
        if n[14] and not n[18]:
            count_4 += 1
        if n[18] and not n[22]:
            count_5 += 1
        if n[22]:
            count_6 += 1

    # pprint(time_frames_records)
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
    '''.format(total, count_1, count_2, count_3, count_4, count_5, count_6, count_1 / total * 100,
               count_2 / total * 100, count_3 / total * 100, count_4 / total * 100, count_5 / total * 100,
               count_6 / total * 100))


def create_list(data_table, approx_in_sec):
    sorted_table = []
    for n in data_table:
        date_time = n[KEY_DATA_TS].replace(microsecond=0)
        seconds_as = int(date_time.strftime('%S'))
        date_time = date_time.replace(second=seconds_as - seconds_as % approx_in_sec)

        source = n[KEY_SOURCE]
        sensor_id = n[KEY_SENSOR_ID]
        rssi = n[KEY_RSSI]

        sorted_table.append((source, date_time, sensor_id, rssi))
    return sorted_table


def compute_distance(level_in_db):
    '''
    free-space path loss (FSPL)
    For typical radio applications, it is common to find f measured in units of GHz and d in km, in which case the FSPL equation becomes

    =20\log _{10}(d)+20\log _{10}(f)+92.45} \ =20\log _{{10}}(d)+20\log _{{10}}(f)+92.45
    For d,f in meters and kilohertz, respectively, the constant becomes  -87.55 .

    For  d,f in meters and megahertz, respectively, the constant becomes -27.55 .

    For d,f in kilometers and megahertz, respectively, the constant becomes  32.45 .
    https://en.wikipedia.org/wiki/Free-space_path_loss#Free-space_path_loss_in_decibels
    '''
    try:
        dB = int(math.ceil(math.fabs(level_in_db)))
        # result = (27.55 - (20 * math.log10(freq_in_mhz)) + dB) / 20.0
        # meters = math.pow(10, result)

        meters = TABLE_DB_TO_METERS[dB]
    except:
        meters = None
    return meters
