# -*- coding: utf-8 -*-

from flask import render_template, request, session
from werkzeug.contrib.cache import SimpleCache
from app import app
from datetime import datetime, time

import bricolage
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


def compute_heatmap(start_date, current_hour):

    sensors_ids = (57, 58, 59, 60, 61, 62, 63, 64, 65, 66)
    sensor_points = load_sensor_locations(sensors_ids)
    approx_in_secs = 10

    zones = bricolage.get_zones(10, 10)
    borders = bricolage.get_borders()

    start_date_time = datetime.combine(start_date, time(current_hour, 0, 0))
    end_date_time = datetime.combine(start_date, time(current_hour, 59, 0))

    db_records = load_data(sensors_ids, start_date_time, end_date_time)

    print('{}'.format(start_date_time))
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

    heat = []
    # for a in adjusted:
    #     heat.append((a.m.lat, a.m.lon, a.visited))

    for p in coordinates:
        heat.append((p.lat, p.lon, 1))

    return heat


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    date_string = request.args.get('date', None)
    if date_string is not None:
        try:
            session['start_date'] = datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError as val_err:
            print('{}, {}'.format(val_err, date_string))

    hour_sting = request.args.get('time', None)
    if hour_sting is not None:
        try:
            session['current_hour'] = int(hour_sting)
        except Exception as ex:
            print('{}: {}'.format(ex, hour_sting))

    start_date = session.get('start_date', None)
    if start_date is None:
        start_date = datetime.strptime('2016-08-12', "%Y-%m-%d")

    current_hour = session.get('current_hour', None)
    if current_hour is None:
        current_hour = 8

    heat = compute_heatmap(start_date, current_hour)

    current_hour += 1
    session['current_hour'] = current_hour

    return render_template("index.html", points=heat)

