'''
1. Load device record from all sensors ordered by TS + identificator(krasi) - 3 % - Krasi
2. Define time_frame TF - Set or list
3. Gather sensor records per TF - list or Dict
4. Compute coordinates - x1, y1, p1, ts, x2, y2, p2
5. Convert to geo-coordinates
6. Save on DB
'''

from datetime import datetime, timedelta

import gridgen
from filtering import trilaterate_points, round_seconds
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
    integration_interval = 6  # hours

    venue_name = 'bricolage'

    start_date = choose_date("choose date")

    for hour in range(0, 24, integration_interval):

        start_date_time = start_date + timedelta(hours=hour)
        end_date_time = start_date + timedelta(hours=hour + integration_interval, minutes=59)

        db_records = load_data(sensors_ids, start_date_time, end_date_time)

        print('{:10} database records'.format(len(db_records)))

        zones = gridgen.get_bricolage_zones(10, 10)

        round_by_sec = round_seconds(db_records, approx_in_secs)

        addjusted = []
        outside_the_grid = 0
        coordinates = trilaterate_points(round_by_sec, sensor_points)
        for point in coordinates:
            point_fit = False
            for zone in zones:
                if zone.contain(point):
                    point_fit = True
                    zone.visit()
                    addjusted.append(zone)

            if not point_fit:
                outside_the_grid += 1

        print("{:10} coordinates".format(len(coordinates)))
        print("{:10} addjusted coordinates".format(len(addjusted)))
        print('{:10} points outside the grid'.format(outside_the_grid))
        if not len(addjusted):
            continue

        # for idx, zone in enumerate(zones):
        #     print('zone {}: visited {} times'.format(idx, zone))

        file_name = "".join([venue_name, '-', str(start_date_time)])

        heat = []
        for z in addjusted:
            heat.append((z.m.lat, z.m.lon, z.visited))
            # print(z)

        vizualization(heat, file_name)


if __name__ == '__main__':
    main()
