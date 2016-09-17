import csv
import os
import matplotlib.pyplot as plt
import folium
from folium import plugins


def write_file(file_name, csv_out_lines):
    with open(file_name, 'w', encoding='utf-8') as plain_out_file:
        file_out_csv = csv.writer(plain_out_file, escapechar="'", quotechar="'", quoting=csv.QUOTE_NONE)

        try:
            for csv_line in csv_out_lines:
                file_out_csv.writerow(csv_line)
        except csv.Error as csv_err:
            print(csv_err)


def read_file(file_name, display=False):
    csv_lines = []
    with open(file_name, 'r', encoding='utf-8') as in_file:
        in_csv = csv.reader(in_file, escapechar="'", quotechar="'", quoting=csv.QUOTE_NONE)

        try:
            for index, csv_line in enumerate(in_csv):
                if display:
                    print('{:2}: {}'.format(index, csv_line))
                csv_lines.append(csv_line)
        except csv.Error as csv_err:
            print(csv_err)
    return csv_lines


def vizualization(data, file_name, margers):
    heatmap_map = folium.Map(data[0], zoom_start=18, max_zoom=21, control_scale=True, detect_retina=True)

    if margers:
        for m in margers:
            marker = folium.RegularPolygonMarker(location=[m.lat, m.lon], fill_color='#769d96',
                                                number_of_sides=8, radius=10)
            marker.add_to(heatmap_map)

    hm = plugins.HeatMap(data)
    heatmap_map.add_children(hm)

    name = file_name + '.html'
    heatmap_map.save(name)

    update_script = """

        <script type="text/JavaScript">

           function timedRefresh(timeoutPeriod) {
               setTimeout("location.reload(true);",timeoutPeriod);
           }

           window.onload = timedRefresh(5000);

        </script>

    """

    with open(name, 'a') as text_file:
        text_file.write(update_script)

    # name = file_name + '.csv'
    # write_file(name, data)

def vizualize_devices (sensor_frames) :
    for source in sensor_frames:
        station_frame_dict = sensor_frames[(source)]
        session_list = []
        session_list_1 = []
        session_list_2 = []
        session_list_3 = []
        session_list_4 = []
        session_list_5 = []
        session_list_6 = []
        session_list_7 = []
        session_list_8 = []
        session_list_9 = []
        old_sensor_1 = None
        old_sensor_2 = None
        old_sensor_3 = None
        old_sensor_4 = None
        old_sensor_5 = None
        old_sensor_6 = None
        old_sensor_7 = None
        old_sensor_8 = None
        old_sensor_9 = None

        # print(station_frame_dict)
        for i, (datetime, sensor) in enumerate(station_frame_dict):
            if i == 0 or sensor == old_sensor:
                session_list.append((sensor, datetime, station_frame_dict[datetime, sensor]))
                old_sensor = sensor
            elif (sensor != old_sensor and old_sensor_1 == None) or sensor == old_sensor_1:
                session_list_1.append((sensor, datetime, station_frame_dict[datetime, sensor]))
                old_sensor_1 = sensor
            elif (sensor != old_sensor and old_sensor_2 == None) or sensor == old_sensor_2:
                session_list_2.append((sensor, datetime, station_frame_dict[datetime, sensor]))
                old_sensor_2 = sensor
            elif (sensor != old_sensor and old_sensor_3 == None) or sensor == old_sensor_3:
                session_list_3.append((sensor, datetime, station_frame_dict[datetime, sensor]))
                old_sensor_3 = sensor
            elif (sensor != old_sensor and old_sensor_4 == None) or sensor == old_sensor_4:
                session_list_4.append((sensor, datetime, station_frame_dict[datetime, sensor]))
                old_sensor_4 = sensor
            elif (sensor != old_sensor and old_sensor_5 == None) or sensor == old_sensor_5:
                session_list_5.append((sensor, datetime, station_frame_dict[datetime, sensor]))
                old_sensor_5 = sensor
            elif (sensor != old_sensor and old_sensor_6 == None) or sensor == old_sensor_6:
                session_list_6.append((sensor, datetime, station_frame_dict[datetime, sensor]))
                old_sensor_6 = sensor
            elif (sensor != old_sensor and old_sensor_7 == None) or sensor == old_sensor_7:
                session_list_7.append((sensor, datetime, station_frame_dict[datetime, sensor]))
                old_sensor_7 = sensor
            elif (sensor != old_sensor and old_sensor_8 == None) or sensor == old_sensor_8:
                session_list_8.append((sensor, datetime, station_frame_dict[datetime, sensor]))
                old_sensor_8 = sensor
            elif (sensor != old_sensor and old_sensor_9 == None) or sensor == old_sensor_9:
                session_list_9.append((sensor, datetime, station_frame_dict[datetime, sensor]))
                old_sensor_9 = sensor

                # print(station_frame_dict)
                # print(station_frame_dict[datetime,sensor])

        plt.xscale('linear')
        plt.yscale('linear')
        plt.scatter(column(session_list, 1), column(session_list, 2), label=old_sensor, color='y', s=200, marker="x")
        if old_sensor_1 != None:
            plt.scatter(column(session_list_1, 1), column(session_list_1, 2), label=old_sensor_1, color='b', s=200,
                        marker="o")
        if old_sensor_2 != None:
            plt.scatter(column(session_list_2, 1), column(session_list_2, 2), label=old_sensor_2, color='g', s=200,
                        marker="v")
        if old_sensor_3 != None:
            plt.scatter(column(session_list_3, 1), column(session_list_3, 2), label=old_sensor_3, color='r', s=200,
                        marker="^")
        if old_sensor_4 != None:
            plt.scatter(column(session_list_4, 1), column(session_list_4, 2), label=old_sensor_4, color='c', s=200,
                        marker="1")
        if old_sensor_5 != None:
            plt.scatter(column(session_list_5, 1), column(session_list_5, 2), label=old_sensor_5, color='m', s=200,
                        marker="2")
        if old_sensor_6 != None:
            plt.scatter(column(session_list_6, 1), column(session_list_6, 2), label=old_sensor_6, color='y', s=200,
                        marker="3")
        if old_sensor_7 != None:
            plt.scatter(column(session_list_7, 1), column(session_list_7, 2), label=old_sensor_7, color='k', s=200,
                        marker="4")
        if old_sensor_8 != None:
            plt.scatter(column(session_list_8, 1), column(session_list_8, 2), label=old_sensor_8, color='y', s=200,
                        marker="s")
        if old_sensor_9 != None:
            plt.scatter(column(session_list_9, 1), column(session_list_9, 2), label=old_sensor_9, color='b', s=200,
                        marker="p")

        plt.title(source)
        plt.legend()
        plt.show()

def column(matrix, i):
    return [row[i] for row in matrix]