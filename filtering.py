import itertools
from statistics import median
from gridgen import Sensor


def segregate_average(data_table):   # function don't working properly for more than 2 record example:
                                      # 10,15,20 - gives 16.25 not 15
                                      # probably dict is not a good approach maybe list
                                      # add counter and devide based on it or use the example below with list
    stations_dict = {}
    for n in data_table:
        source = n[0]
        date_time = n[1]
        sensor_id = n[2]
        rssi = n[3]

        try:
            station_frame_dict = stations_dict[(source, date_time)]
            try:
                old_rssi = station_frame_dict[sensor_id]
                station_frame_dict[sensor_id] = (old_rssi + rssi) / 2
            except TypeError:
                pass
            except KeyError:
                station_frame_dict[sensor_id] = rssi
        except KeyError:
            stations_dict[(source, date_time)] = {sensor_id: rssi}

    print('{:10} ({:.2f}%) station-time frames aand % of all'.format(len(stations_dict), len(stations_dict)/len(data_table)*100))
    return stations_dict

def segregate_average_session(data_table):

# function don't working properly for more than 2 record example:  # 10,15,20 - gives 16.25 not 15
# probably dict is not a good approach maybe list
# add counter and devide based on it or use the example below with list

    stations_dict = {}
    for n in data_table:
        source = n[0]
        date_time = n[1]
        sensor_id = n[2]
        rssi = n[3]

        try:
            station_frame_dict = stations_dict[(source)]
            try:
                old_rssi = station_frame_dict[sensor_id]
                station_frame_dict[(date_time, sensor_id)] = ( (old_rssi + rssi) / 2)
            except TypeError:
                pass
            except KeyError:
                station_frame_dict[(date_time, sensor_id)] = (rssi)
        except KeyError:
            stations_dict[(source)] = {(date_time,sensor_id) : rssi}

    print('{:10} ({:.2f}%) station-time frames aand % of all'.format(len(stations_dict),
                                                                     len(stations_dict) / len(data_table) * 100))
    return stations_dict


def segregate_median(data_table):
    stations_dict = {}
    # (source, date_time, sensor_id, rssi)
    for n in data_table:
        source = n[0]
        date_time = n[1]
        sensor_id = n[2]
        rssi = n[3]

        try:
            station_frame_dict = stations_dict[(source, date_time)]
            try:
                rssi_list = station_frame_dict[sensor_id]
                rssi_list.append(rssi)
            except TypeError:
                pass
            except KeyError:
                rssi_list = [rssi]
                station_frame_dict[sensor_id] = rssi_list
        except KeyError:
            rssi_list = [rssi]
            stations_dict[(source, date_time)] = {sensor_id: rssi_list}

    print('{:10} station-time frames'.format(len(stations_dict)))

    for station_frame in stations_dict:
        station_frame_dict = stations_dict[station_frame]
        for key in station_frame_dict:
            rssi_list = station_frame_dict[key]
            sorted_rssi = sorted(rssi_list)
            rssi_len = len(sorted_rssi)
            middle = median(sorted_rssi)
            average = sum(sorted_rssi) / float(rssi_len)
            station_frame_dict[key] = middle
            # print('{}:{},{}'.format(rssi_len, middle, average))

    return stations_dict


def trilaterate(stations_dict, sensor_points):
    circles = []
    gathered = []
    size_2_1 = 0
    size_2_2 = 0
    num_sensors_dict = {}
    for station_frame in stations_dict:
        station_frame_dict = stations_dict[station_frame]
        size = len(station_frame_dict)
        try:
            num_sensors_dict[size] += 1
        except KeyError:
            num_sensors_dict[size] = 1

        if size == 2:
            sensors = []
            for sensor_id, rssi in station_frame_dict.items():
                s = Sensor(sensor_points[sensor_id], rssi)
                sensors.append(s)

            c0, c1 = map(lambda x: x, sensors)
            p = c0.intersect(c1)
            circles.append([c0, c1])
            if p:
                size_2_1 += 1
                gathered.append(p)

        if size >= 3:
            sensors = []
            for sensor_id, rssi in station_frame_dict.items():
                s = Sensor(sensor_points[sensor_id], rssi)
                sensors.append(s)

            cross = None
            for subset in itertools.combinations(sensors, 3):
                p1, p2, p3 = map(lambda x: x, subset)
                cross = p1.trilaterate(p2, p3)
                circles.append([p1, p2, p3])
                if cross:
                    gathered.append(cross)
                    break
                else:
                    pass

            if cross is None:
                for subset in itertools.combinations(sensors, 2):
                    c0, c1 = map(lambda x: x, subset)
                    p = c0.intersect(c1)
                    circles.append([c0, c1])
                    if p:
                        size_2_2 += 1
                        gathered.append(p)
                        break
                    else:
                        pass

    for sensors, count in num_sensors_dict.items():
        print('{:10} ({:.2f})No stations and % seen by {:2} sensors'.format(count, count/len(stations_dict)*100, sensors))

    print('{:10} ({:.2f}) No coordinates and % from  2 sensors\''.format(size_2_1, size_2_1/len(stations_dict)*100))
    print('{:10} ({:.2f}) No coordinates and % from  2 sensors\"'.format(size_2_2, size_2_2/len(stations_dict)*100))
    print('{:10} ({:.2f}) No coordinates and % from  3 sensors'.format(len(gathered) - size_2_1 - size_2_2,
                                                                       (len(gathered) - size_2_1 - size_2_2)/len(stations_dict)*100))


    return circles, gathered


def round_seconds(data_table, approx_in_sec):
    KEY_SOURCE = 0
    KEY_SENSOR_ID = 1
    KEY_DATA_TS = 2
    KEY_RSSI = 3
    sorted_table = []
    for n in data_table:
        date_time = n[KEY_DATA_TS].replace(microsecond=0)
        str_sec = date_time.strftime('%S')
        seconds_as = int(str_sec)
        date_time = date_time.replace(second=seconds_as - seconds_as % approx_in_sec)

        source = n[KEY_SOURCE]
        sensor_id = n[KEY_SENSOR_ID]
        rssi = n[KEY_RSSI]

        sorted_table.append((source, date_time, sensor_id, rssi))
    return sorted_table
