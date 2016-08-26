# -*- coding: utf-8 -*-

import argparse
import csv
import socket
import sys

import pyhdb


def query_save(select_statement, output_file_name):
    try:
        db_connection = pyhdb.connect(host="52.58.251.227", port=30015, user='SYSTEM', password='a5_hS3aZ#')
    except socket.error as why:
        print(why)
        sys.exit(1)

    db_cursor = db_connection.cursor()

    try:

        db_cursor.execute(select_statement)
        selected_rows = db_cursor.fetchall()

        print('matching records count = {}'.format(len(selected_rows)))

    except pyhdb.exceptions.DatabaseError as why:
        print(why)
        sys.exit(1)

    with open(output_file_name, 'w') as plain_file:

        csv_file = csv.writer(plain_file, escapechar="'", quotechar="'", quoting=csv.QUOTE_NONE)

        try:
            for csv_line in selected_rows:
                csv_file.writerow(csv_line)
        except csv.Error as why:
            print('csv.Error: {}'.format(why))
            sys.exit(1)

    db_cursor.close()
    db_connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='query-save')
    parser.add_argument('--output', default='data/output.csv', dest='output_file', action='store', help='Output file name')

    args = parser.parse_args()

    shopup_samples = '"SHOPUP"."me.shopup.data::data"'
    shopup_installations = '"SHOPUP"."me.shopup.data::sensor_installations"'
    shopup_sensors = '"SHOPUP"."me.shopup.data::sensors"'
    shopup_users = '"SHOPUP"."me.shopup.data::users"'
    shopup_shops = '"SHOPUP"."me.shopup.data::shops"'

    table_name = shopup_samples

#    select_statement = 'SELECT TOP 100 * FROM "SHOPUP"."me.shopup.data::data" WHERE "IS_STA"=0 AND CAST("DATE_TIME" AS time) NOT BETWEEN \'5:00:00\' and \'23:00:00\''
    select_statement= 'SELECT * FROM "SHOPUP"."me.shopup.data::data" WHERE "IS_STA" = 0 AND "MAC1" <> \'\' AND "NETWORK" <> \'\' ORDER BY "MAC2"'
#    select_statement = "SELECT TOP 10000 * FROM {} ORDER BY {} DESC".format(table_name, '"DATE_TIME"')
    print(select_statement)

    query_save(select_statement, args.output_file)

    print('result saved to: {}'.format(args.output_file))
