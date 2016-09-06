# -*- coding: utf-8 -*-

from datetime import datetime

from app import db


class Sensors(db.Model):
    __tablename__ = 'me.shopup.data::sensors'
    __table_args__ = {'schema': 'SHOPUP'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('mac', db.String(12))
    version = db.Column(db.String(5))

    def __init__(self, name):
        self.name = name
        self.version = '1.0.0'

    def __repr__(self):
        return 'sensor: {} v.{}'.format(self.name, self.version)


class Installations(db.Model):
    __tablename__ = 'me.shopup.data::sensor_installations'
    __table_args__ = {'schema': 'SHOPUP'}

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column('sensor_id', db.String(12), primary_key=True)

    installed = db.Column('installation_date', db.DateTime, primary_key=True)
    removed = db.Column('removal_date', db.DateTime, primary_key=True)

    latitude = db.Column('coordinates_north', db.Float)
    longitude = db.Column('coordinates_east', db.Float)

    description = db.Column(db.Unicode(500))

    # deprecated
    venue_id = db.Column('shop_id', db.Integer)

    def __init__(self, sensor_id, latitude, longitude, notes,
                 start=datetime.min, end=datetime.max):
        self.sensor_id = sensor_id
        self.latitude = latitude
        self.longitude = longitude
        self.installed = start
        self.removed = end
        self.description = notes

    def __repr__(self):
        return 'installation: S({}) {} {} {} {} {}'.format(self.sensor_id, self.installed, self.removed, self.latitude,
                                                           self.longitude, self.description.encode('utf-8', 'ignore'))

class Samples(db.Model):
    __tablename__ = 'me.shopup.data::data'
    __table_args__ = {'schema': 'SHOPUP'}

    date_time = db.Column(db.DateTime, primary_key=True)
    destination = db.Column(db.String(12), nullable=True)
    source = db.Column(db.String(12), index=True)
    ssid = db.Column(db.Unicode(200), nullable=True)
    rssi = db.Column(db.Integer)
    is_station = db.Column('is_sta', db.Integer)

    installation_id = db.Column('sensor_installation_id', db.Integer, primary_key=True)

    def __init__(self, installation_id, date_time, destination, source, ssid, rssi, is_station):
        self.date_time = date_time
        self.destination = destination
        self.source = source
        self.ssid = None if ssid == u'' else ssid
        self.rssi = rssi
        self.is_station = is_station
        self.installation_id = installation_id

    def __getitem__(self, index):
        as_list = [self.date_time, self.destination, self.source, self.ssid,
                   self.rssi, self.is_station, self.installation_id]
        return as_list[index]

    def __hash__(self):
        return hash((self.installation_id, self.date_time, self.destination,
                     self.source, self.ssid, self.rssi, self.is_station))

    def to_list(self):
        return [self.date_time, self.destination, self.source, self.ssid,
                self.rssi, self.is_station, self.installation_id]

    def __repr__(self):
        return 'sample: {} {} {} {} {} {} {:2}'.format(self.date_time, self.destination, self.source, self.ssid,
                                                       self.rssi, self.is_station, self.installation_id)
