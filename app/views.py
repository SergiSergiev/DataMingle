# -*- coding: utf-8 -*-

from flask import render_template, request, session
from werkzeug.contrib.cache import SimpleCache
from app import app
from datetime import datetime, time
import os
import bricolage, pickle
from filtering import trilaterate, round_seconds, segregate_average
from dbload import load_data, load_sensor_locations

CACHE_TIMEOUT = 10

cache = SimpleCache()


class cached(object):
    def __init__(self, timeout=None):
        self.timeout = timeout or CACHE_TIMEOUT

    def __call__(self, f):
        def decorator(*args, **kwargs):
            response = cache.get(request.path)
            if response is None:
                response = f(*args, **kwargs)
                cache.set(request.path, response, self.timeout)
            return response

        return decorator


def parse_parameters():
    date_string = request.args.get('date', None)
    if date_string is not None:
        try:
            session['start_date'] = datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError as val_err:
            print('{}, {}'.format(val_err, date_string))

    hour_sting = request.args.get('time', None)
    if hour_sting is not None:
        try:
            current_hour = int(hour_sting)
            if current_hour > 23:
                current_hour = 23
            session['current_hour'] = current_hour
        except Exception as ex:
            print('{}: {}'.format(ex, hour_sting))

    start_date = session.get('start_date', None)
    if start_date is None:
        start_date = datetime.strptime('2016-08-12', "%Y-%m-%d")

    sec_sting = request.args.get('sec', None)
    if sec_sting is not None:
        try:
            approx_in_secs = int(sec_sting)
            session['approx_in_secs'] = approx_in_secs
        except Exception as ex:
            print('{}: {}'.format(ex, sec_sting))


    current_hour = session.get('current_hour', None)
    if current_hour is None:
        current_hour = 8

    if current_hour > 23:
        current_hour = 8

    approx_in_secs = session.get('approx_in_secs', None)
    if approx_in_secs is None:
        approx_in_secs = 10

    return start_date, current_hour, approx_in_secs


def load_db_samples(start_date, current_hour, sensors_ids):
    db_records = None
    db_file_name = 'db-{}-{}.pickle'.format(str(start_date), str(current_hour))
    db_records_name = os.path.join('tmp', db_file_name)

    try:
        with open(db_records_name, 'rb') as pickle_file:
            db_records = pickle.load(pickle_file)
    except FileNotFoundError:
        pass

    print('{}'.format(datetime.combine(start_date, time(current_hour, 0, 0))))

    if db_records is None:
        start_date_time = datetime.combine(start_date, time(current_hour, 0, 0))
        end_date_time = datetime.combine(start_date, time(current_hour, 59, 0))
        db_records = load_data(sensors_ids, start_date_time, end_date_time)
        with open(db_records_name, 'wb') as pickle_file:
            pickle.dump(db_records, pickle_file)

    print('{:10} database records'.format(len(db_records)))

    return db_records


def compute_heatmap(db_records, sensors_ids, approx_in_secs):
    sensor_points = load_sensor_locations(sensors_ids)

    zones = bricolage.get_zones(10, 10)

    round_by_sec = round_seconds(db_records, approx_in_secs)

    adjusted = []
    outside = []
    sensor_frames = segregate_average(round_by_sec)
    circles, coordinates = trilaterate(sensor_frames, sensor_points)
    for point in coordinates:
        point_fit = False
        for zone in zones:
            if zone.contain(point):
                point_fit = True
                zone.visit()
                adjusted.append(zone)
        if not point_fit:
            outside.append(point)

    print('{:10} seconds approximation'.format(approx_in_secs))
    print("{:10} coordinates".format(len(coordinates)))
    print("{:10} adjusted coordinates".format(len(adjusted)))
    print('{:10} points outside the grid'.format(len(outside)))

    heatmap = []
    # for a in adjusted:
    #     heatmap.append((a.m.lat, a.m.lon, a.visited))

    for p in coordinates:
        heatmap.append((p.lat, p.lon, 1))

    return circles, heatmap


@app.route('/circles', methods=['GET'])
def circles():
    sensors_ids = (57, 58, 59, 60, 61, 62, 63, 64, 65, 66)

    start_date, current_hour, approx_in_secs = parse_parameters()

    db_records = load_db_samples(start_date, current_hour, sensors_ids)

    circles, _ = compute_heatmap(db_records, sensors_ids, approx_in_secs)

    current_circles = session.get('current_circles', None)

    if current_circles is None or current_circles >= len(circles):
        current_circles = 0

    circle_list = circles[current_circles]
    current_circles += 1
    session['current_circles'] = current_circles

    session['start_date'] = start_date
    session['current_hour'] = current_hour
    session['approx_in_secs'] = approx_in_secs

    return render_template("index.html", points=None, circles=circle_list, auto_refresh=True)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    sensors_ids = (57, 58, 59, 60, 61, 62, 63, 64, 65, 66)

    start_date, current_hour, approx_in_secs = parse_parameters()

    db_records = load_db_samples(start_date, current_hour, sensors_ids)

    _, heatmap = compute_heatmap(db_records, sensors_ids, approx_in_secs)

    current_hour += 1

    session['start_date'] = start_date
    session['current_hour'] = current_hour
    session['approx_in_secs'] = approx_in_secs

    return render_template("index.html", points=heatmap, circles=None, auto_refresh=False)

