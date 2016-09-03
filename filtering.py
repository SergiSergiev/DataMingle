import itertools

from gridgen import Circle


def trilaterate_points(data_table, sensor_points):
    gathered = []
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
                old_rssi = station_frame_dict[sensor_id]
                station_frame_dict[sensor_id] = (old_rssi + rssi) / 2
            except TypeError:
                pass
            except KeyError:
                station_frame_dict[sensor_id] = rssi
        except KeyError:
            stations_dict[(source, date_time)] = {sensor_id: rssi}

    print('{:10} stations'.format(len(stations_dict)))

    num_sensors_dict = {}
    for station_frame in stations_dict:
        station_frame_dict = stations_dict[station_frame]
        size = len(station_frame_dict)
        try:
            num_sensors_dict[size] += 1
        except KeyError:
            num_sensors_dict[size] = 1

        if size >= 3:
            sensors = []
            for sensor_id, rssi in station_frame_dict.items():
                s = Circle(sensor_points[sensor_id], rssi)
                sensors.append(s)

            for subset in itertools.combinations(sensors, 3):
                p1, p2, p3 = map(lambda x: x, subset)
                cross = p1.trilaterate(p2, p3)
                if cross:
                    gathered.append(cross)
                    break
                else:
                    pass

    for sensors, count in num_sensors_dict.items():
        print('{:10} stations seen by {:2} sensors'.format(count, sensors))

    return gathered


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
