# -*- coding: utf-8 -*-


from flask import render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.contrib.cache import SimpleCache

from app import app
from datetime import datetime, timedelta

import bricolage, os
from filtering import trilaterate, round_seconds, segregate_average
from dbload import load_data, load_sensor_locations
from vizualization import vizualization

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


auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    if username == u'ShopUp':
        return str(username)
    else:
        return None


@auth.hash_password
def hash_pw(password):
    return password


def choose_date(prompt_sting):
    while True:
        now = '2016-08-10'  # input('{} {} ? '.format(prompt_sting, date.today()))
        try:
            return datetime.strptime(now, '%Y-%m-%d')
        except ValueError as val_err:
            print(val_err)
            continue


@app.route('/')
@app.route('/index')
@auth.login_required
def index():

    sensors_ids = (57, 58, 59, 60, 61, 62, 63, 64, 65, 66)
    sensor_points = load_sensor_locations(sensors_ids)
    approx_in_secs = 10
    integration_interval = 1  # hours
    hour = 10

    zones = bricolage.get_zones(10, 10)
    start_date = choose_date("choose date")

    start_date_time = start_date + timedelta(hours=hour)
    end_date_time = start_date + timedelta(hours=hour + integration_interval, minutes=59)

    db_records = load_data(sensors_ids, start_date_time, end_date_time)

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

    file_name = os.path.join('app', 'templates', 'index')

    heat = []
    for a in adjusted:
        heat.append((a.m.lat, a.m.lon, a.visited))

    for p in outside:
        heat.append((p.lat, p.lon, 1))

    vizualization(heat, file_name)

    return render_template("index.html")
