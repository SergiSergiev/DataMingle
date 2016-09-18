'''
1. Load device record from all sensors ordered by TS + identificator(krasi) - 3 % - Krasi
2. Define time_frame TF - Set or list
3. Gather sensor records per TF - list or Dict
4. Define sessions
5. Observe sessions results - probably visualization on matplotlip based on timeframe and sensors


4. Compute coordinates - x1, y1, p1, ts, x2, y2, p2
5. Convert to geo-coordinates
6. Save on DB
'''

from datetime import datetime, timedelta

import bricolage
import os
from filtering import trilaterate, round_seconds, segregate_average, segregate_average_session
from dbload import load_samples, load_sensor_locations
from vizualization import vizualization, vizualize_devices
from pprint import pprint
import matplotlib.pyplot as plt


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
    approx_in_secs = 5
    integration_interval = 24  # hours

    zones = bricolage.get_zones(10, 10)
    borders = bricolage.get_borders()
    start_date = choose_date("choose date")
    max_hour = 24 - integration_interval + 1

    for start_hour in range(0, max_hour, integration_interval):

        db_records = load_samples(start_date, start_hour, integration_interval, sensors_ids)
        round_by_sec = round_seconds(db_records, approx_in_secs)
        start_date_time = start_date + timedelta(hours=start_hour)

        adjusted = []
        outside = []
        sensor_frames = segregate_average(round_by_sec)	# some errors see the comments in he filltering.py
        #vizualize_devices(sensor_frames)
        #pprint(sensor_frames)

        _, coordinates = trilaterate(sensor_frames, sensor_points)
        for point in coordinates:
            point_fit = False
            for zone in zones:
                if zone.contain(point):
                    point_fit = True
                    zone.visit()
                    adjusted.append(zone)
            if not point_fit:
                outside.append(point)

        try:
            print("{:10} ({:.3f}%) coordinates & % of all frames".format(len(coordinates), len(coordinates)/len(sensor_frames)*100))
            print("{:10} ({:.3f}%) adjusted coordinates & % of all frames".format(len(adjusted), len(adjusted)/len(sensor_frames)*100))
            print('{:10} ({:.3f}%) points outside the grid & % coordinates'.format(len(outside), len(outside)/len(coordinates)*100))
        except ZeroDivisionError:
           pass

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
