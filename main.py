'''
1. Load device record from all sensors ordered by TS + identificator(krasi) - 3 % - Krasi
2. Define time_frame TF - Set or list
3. Gather sensor records per TF - list or Dict
4. Compute coordinates - x1, y1, p1, ts, x2, y2, p2
5. Convert to geo-coordinates
6. Save on DB
'''

from datetime import datetime, timedelta

import bricolage
import os, pickle
from filtering import trilaterate, round_seconds, segregate_average
from dbload import load_data, load_sensor_locations
from vizualization import vizualization


def choose_date(prompt_sting):
    while True:
        now = '2016-08-10'  # input('{} {} ? '.format(prompt_sting, date.today()))
        try:
            return datetime.strptime(now, '%Y-%m-%d')
        except ValueError as val_err:
            print(val_err)
            continue


def main():
    sensors_ids = (57, 58, 59, 60, 61, 62, 63, 64, 65, 66)
    sensor_points = load_sensor_locations(sensors_ids)
    approx_in_secs = 10
    integration_interval = 1  # hours
    use_pickle = False

    venue_name = 'bricolage'
    zones = bricolage.get_zones(10, 10)
    borders = bricolage.get_borders()
    start_date = choose_date("choose date")

    for hour in range(8, 22, integration_interval):

        start_date_time = start_date + timedelta(hours=hour)
        end_date_time = start_date + timedelta(hours=hour + integration_interval, minutes=59)

        pickle_file_name = venue_name + '.pickle'
        if use_pickle and os.path.exists(pickle_file_name):
            with open(venue_name + '.pickle', "rb") as pickle_file:
                db_records = pickle.load(pickle_file)
        else:
            db_records = load_data(sensors_ids, start_date_time, end_date_time)
            if use_pickle:
                with open(pickle_file_name, "wb") as pickle_file:
                    pickle.dump(db_records, pickle_file)

        print('{:10} database records'.format(len(db_records)))

        round_by_sec = round_seconds(db_records, approx_in_secs)

        adjusted = []
        outside = []
        sensor_frames = segregate_average(round_by_sec)
        coordinates = trilaterate(sensor_frames, sensor_points)
        for point in coordinates:
            point_fit = False
            for zone in zones:
                if zone.contain(point):
                    point_fit = True
                    zone.visit()
                    adjusted.append(zone)
            if not point_fit:
                outside.append(point)

        print("{:10} coordinates".format(len(coordinates)))
        print("{:10} adjusted coordinates".format(len(adjusted)))
        print('{:10} points outside the grid'.format(len(outside)))
        if not len(adjusted):
            continue

        # for idx, zone in enumerate(zones):
        #     print('zone {}: visited {} times'.format(idx, zone))

        file_name = os.path.join('app', 'templates', 'index')
        date_string = str(start_date_time).replace(':', '-')
        file_name = file_name + '-' + date_string

        heat = []
        for z in adjusted:
            heat.append((z.m.lat, z.m.lon, z.visited))
            # print(z)

        for z in outside:
            heat.append((z.lat, z.lon, 1))
            # print(z)

        vizualization(heat, file_name, [borders.a, borders.b, borders.c, borders.d])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
