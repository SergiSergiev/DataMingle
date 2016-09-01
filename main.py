'''
1. Load device record from all sensors ordered by TS + identificator(krasi) - 3 % - Krasi
2. Define time_frame TF - Set or list
3. Gather sensor records per TF - list or Dict
4. Compute coordinates - x1, y1, p1, ts, x2, y2, p2
5. Convert to geo-coordinates
6. Save on DB
'''

import os, pickle
import gridgen

from data_manipulations import create_time_frames, create_time_frames2, report, create_list_with_rounded_seconds
from load_data import load_data
from vizualization import vizualization

hours = '23:59:59.000'
approx_in_secs = 10
routers_number = (57, 58, 59, 60, 61, 62, 63, 64, 65, 66)
requested_date = "2016-8-21"
name_file_outpup = 'bricolage'


def main():
    pickle_file_name = name_file_outpup + '_' + requested_date + '_' + hours + '.pickle'
    if os.path.exists(pickle_file_name):
        with open(pickle_file_name, "rb") as pickle_file:
            db_records_sensor_date = pickle.load(pickle_file)
    else:
        db_records_sensor_date = load_data(routers_number, requested_date, hours)
        with open(pickle_file_name, "wb") as pickle_file:
            pickle.dump(db_records_sensor_date, pickle_file)

    print('matching records count = {}'.format(len(db_records_sensor_date)))

    zones = gridgen.get_bricolage_zones(10, 10)

    round_by_sec = create_list_with_rounded_seconds(db_records_sensor_date, approx_in_secs)

    addjusted = []
    coordinates = create_time_frames2(round_by_sec, routers_number)
    for point in coordinates:
        point_fit = False
        for zone in zones:
            if zone.contain(gridgen.Point(point[0], point[1])):
                zone.visit()
                addjusted.append((zone.m.lat, zone.m.lon))

        if not point_fit:
            print('point {} outside the grid'.format(point))

    print("number of coordinates: {}".format(len(coordinates)))
    print("addjusted coordinates: {}".format(len(addjusted)))

    for idx, zone in enumerate(zones):
        print('zone {}: visited {} times'.format(idx, zone))

    file_name = name_file_outpup + '-2_' + requested_date + '_' + str(approx_in_secs)
    vizualization(addjusted, file_name)

if __name__ == '__main__':
    main()
