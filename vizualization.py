import csv
import os

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
