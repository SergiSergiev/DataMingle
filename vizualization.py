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


def vizualization(data, file_name):
    heatmap_map = folium.Map(data[0], zoom_start=19, control_scale=True)

    hm = plugins.HeatMap(data)
    heatmap_map.add_children(hm)

    if not os.path.exists('maps'):
        os.makedirs('maps')

    path = os.path.join('maps', file_name + '.html')
    heatmap_map.save(path)

    path = os.path.join('maps', file_name + '.csv')
    write_file(path, data)
