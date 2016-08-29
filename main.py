'''
1. Load device record from all sensors ordered by TS + identificator(krasi) - 3 % - Krasi
2. Define time_frame TF - Set or list
3. Gather sensor records per TF - list or Dict
4. Compute coordinates - x1, y1, p1, ts, x2, y2, p2
5. Convert to geo-coordinates
6. Save on DB
'''

from data_manipulations import create_time_frames, report, create_list
from load_data import load_data
from vizualization import vizualization


hours = '23:59:59.000'
approx_in_secs = 10
routers_number = (57, 58, 59, 60, 61, 62, 63, 64, 65, 66)
requested_date = "2016-08-21"
name_file_outpup = 'bricolage'


def main():
    db_records_sensor_date = load_data(routers_number, requested_date, hours)
    round_by_sec = create_list(db_records_sensor_date, approx_in_secs)
    time_frames_records = create_time_frames(round_by_sec)
    report(time_frames_records)

    counter = 0
    gathered_coordinates = list()
    for n in time_frames_records:
        if n[26] != None:
            counter += 1
            gathered_coordinates.append(n[-2:])
    print("Number of coordinates: {}".format(counter))
    print(gathered_coordinates)
    file_name = name_file_outpup + '_' + requested_date + '_' + str(approx_in_secs)
    vizualization(gathered_coordinates, file_name)


if __name__ == '__main__':
    main()