# 42.623833, 23.353693
# 42.624525, 23.354109
# 42.624743, 23.353345
# 42.624106, 23.352924

from math import cos, sin, asin, sqrt, pi, degrees, radians, atan2, isnan, log10, fabs, ceil

import numpy as np

scale = 1
earthR = 6378137.0 / scale


class Point(object):
    def __init__(self, lat, lon):
        self.lat = float(lat)
        self.lon = float(lon)

    def __repr__(self):
        return '{},{}'.format(self.lat, self.lon)

    def distance(self, p):
        """
        Haversine
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [self.lon, self.lat, p.lon, p.lat])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        # r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        r = earthR
        return c * r

    def offset(self, delta_east, delta_nort):
        """
        Algorithm for offsetting a latitude/longitude by some amount of meters
        """
        # Coordinate offsets in radians
        r = earthR
        dlat = delta_nort / r
        dlon = delta_east / (r * cos(pi * self.lat / 180.0))

        # offset position, decimal degrees
        lat = self.lat + dlat * 180.0 / pi
        lon = self.lon + dlon * 180.0 / pi

        return Point(lat, lon)

    def slide(self, c, t):
        r = radians(t)
        dn = c * sin(r)
        de = c * cos(r)

        return self.offset(de, dn)

    def angle(self, p):
        c = self.distance(p)
        x = Point(p.lat, self.lon)
        b = self.distance(x)
        o = b / c

        return degrees(asin(o))

    def ecef(self):
        """
        Using authalic sphere, if using an ellipsoid this step is slightly different
        Convert geodetic Lat/Long to ECEF xyz
          1. Convert Lat/Long to radians
          2. Convert Lat/Long(radians) to ECEF  (Earth-Centered,Earth-Fixed)
        """
        x = earthR * (cos(radians(self.lat)) * cos(radians(self.lon)))
        y = earthR * (cos(radians(self.lat)) * sin(radians(self.lon)))
        z = earthR * (sin(radians(self.lat)))

        return [x, y, z]


class Rectangle(object):
    def __init__(self, p, w, h, t):
        self.a = p
        self.w = float(w)
        self.h = float(h)
        self.t = float(t)
        self.b = self.a.slide(w, t)
        self.c = self.b.slide(h, t + 90)
        self.d = self.a.slide(h, t + 90)

        points = [self.a, self.b, self.c, self.d]
        center = Point(0, 0)
        num = len(points)
        for i in range(num):
            center.lon += points[i].lon
            center.lat += points[i].lat
        center.lon /= num
        center.lat /= num
        self.m = center

    def __repr__(self):
        return '{}\n{}\n{}\n{}'.format(self.a, self.b, self.c, self.d)

    def center(self):
        return self.m

    def contain(self, p):
        ba_lon = self.b.lon - self.a.lon
        ba_lat = self.b.lat - self.a.lat
        da_lon = self.d.lon - self.a.lon
        da_lat = self.d.lat - self.a.lat

        if (p.lon - self.a.lon) * ba_lon + (p.lat - self.a.lat) * ba_lat < 0.0:
            return False
        if (p.lon - self.b.lon) * ba_lon + (p.lat - self.b.lat) * ba_lat > 0.0:
            return False
        if (p.lon - self.a.lon) * da_lon + (p.lat - self.a.lat) * da_lat < 0.0:
            return False
        if (p.lon - self.d.lon) * da_lon + (p.lat - self.d.lat) * da_lat > 0.0:
            return False

        return True

    def split(self, lon_cnt, lat_cnt):
        rectangles = []
        new_w = self.w / lon_cnt
        new_h = self.h / lat_cnt

        for y in range(0, lat_cnt):
            for x in range(0, lon_cnt):
                p = self.a
                p = p.slide(new_w * x, self.t)
                p = p.slide(new_h * y, self.t + 90)
                r = self.__class__(p, new_w, new_h, self.t)
                rectangles.append(r)

        return rectangles


class Zone(Rectangle):
    def __init__(self, p, w, h, t):
        Rectangle.__init__(self, p, w, h, t)
        self.visited = 0

    def __repr__(self):
        return '{},{},{},{},{}'.format(self.a, self.b, self.c, self.d, self.visited)

    def visit(self):
        self.visited += 1


class Circle(object):
    def __init__(self, p, r):
        self.p = p
        self.r = r

    def __repr__(self):
        return '{},{}'.format(self.p, self.r)

    def intersect(self, c1):
        """
        http://mathworld.wolfram.com/Circle-CircleIntersection.html
        http://stackoverflow.com/questions/3349125/circle-circle-intersection-points
        http://paulbourke.net/geometry/circlesphere/tvoght.c
        """
        # dx and dy are the vertical and horizontal distances between the circle centers.
        dx = c1.p.lon - self.p.lon
        dy = c1.p.lat - self.p.lat

        d = self.p.distance(c1.p)
        # d = sqrt((dy * dy) + (dx * dx))
        r0 = self.r
        r1 = c1.r

        if d > r0 + r1:
            return None  # no solution. circles do not intersect.

        if d < fabs(r0 - r1):
            return None  # no solution. one circle is contained in the other

        if not d and r0 == r1:
            return None

        # 'point 2' is the point where the line through the circle
        # intersection points crosses the line between the circle
        # centers.
        #
        # Determine the distance from point 0 to point 2.
        a = ((r0 * r0) - (r1 * r1) + (d * d)) / (2.0 * d)

        t = self.p.angle(c1.p)
        p2 = self.p.slide(a, t)

        # Determine the distance from point 2 to either of the intersection points.
        h = sqrt((r0 * r0) - (a * a))

        # print('{:10} distance'.format(h))
        return p2 if h < Sensor.horde_max else None

    def trilaterate(self, s2, s3):
        """
        http://en.wikipedia.org/wiki/Trilateration
        assuming elevation = 0
        length unit : m
        """
        P1, P2, P3 = map(lambda x: np.array(x.p.ecef()), [self, s2, s3])
        DistA, DistB, DistC = map(lambda x: x.r, [self, s2, s3])

        # vector transformation: circle 1 at origin, circle 2 on x axis
        ex = (P2 - P1) / (np.linalg.norm(P2 - P1))
        i = np.dot(ex, P3 - P1)
        ey = (P3 - P1 - i * ex) / (np.linalg.norm(P3 - P1 - i * ex))
        ez = np.cross(ex, ey)
        d = np.linalg.norm(P2 - P1)
        j = np.dot(ey, P3 - P1)

        try:
            # plug and chug using above values
            x = (pow(DistA, 2) - pow(DistB, 2) + pow(d, 2)) / (2 * d)
            y = ((pow(DistA, 2) - pow(DistC, 2) + pow(i, 2) + pow(j, 2)) / (2 * j)) - ((i / j) * x)

            # only one case shown here
            dz = pow(DistA, 2) - pow(x, 2) - pow(y, 2)
            # only one case shown here
            z = np.sqrt(dz)
        except TypeError as type_err:
            return None

        # xyz is an array with ECEF x,y,z of trilateration point
        xyz = P1 + x * ex + y * ey + z * ez

        # convert back to lat/long from ECEF
        # convert to degrees
        lat = degrees(asin(xyz[2] / earthR))
        lon = degrees(atan2(xyz[1], xyz[0]))

        if isnan(lat) or isnan(lon):
            return None

        return Point(lat, lon)


class Sensor(Circle):
    horde_max = 2.5 # meters
    dB_m = []
    for dB in range(0, -101, -1):
        # FSPL(dB) = 20log_10(d) + 20log_10(f) - 27.55
        # (dB - 20 * log10(f) + 27.55) / 20 = log10(d)
        # 10 exp (dB - 20 * log10(f) + 27.55) / 20 = d
        frequency = 2462
        exp = (fabs(dB) - 20 * log10(frequency) + 27.55) / 20
        meters = pow(10.0, exp / 1.6)
        v = meters / scale
        dB_m.append(v)
        # print(fspl)

    def __init__(self, p, dB):
        try:
            r = Sensor.dB_m[int(ceil(fabs(dB)))]
        except IndexError as idx_err:
            print('{},{}'.format(idx_err, dB))
            raise idx_err

        Circle.__init__(self, p, r)


if __name__ == '__main__':
    a = Point(42.623801, 23.353842)
    # b = Point(42.624531, 23.354114)
    # c = Point(42.624743, 23.353345)
    # d = Point(42.624095, 23.352912)

    # random point
    z = Point(51.0, 0.0)
    z = z.offset(0, 100.0 / scale)
    # print(z)

    m = Point(42.623706, 23.354146)
    n = Point(42.624090, 23.354344)
    t = m.angle(n)

    # mr. Bricolage SF3
    r = Rectangle(a, 82.0 / scale, 80.0 / scale, t)
    # print(r)
    #
    # # Unit Tests?
    # print('Is poligon center inside poligon? {}'.format(r.contain(r.center())))
    # print('Is random point inside poligon?   {}'.format(r.contain(z)))
    #
    grid = r.split(10, 10)
    for r in grid:
        print(r)

    # s1 = Sensor(Point(31.257474, 121.620974), 0.228)
    # s2 = Sensor(Point(31.260217, 121.621095), 0.123)
    # s3 = Sensor(Point(31.259148, 121.623835), 0.187)
    #
    # p = s1.trilaterate(s2, s3)
    # print(p)

    c0 = Circle(Point(-1.0, -1.0), 1.5)
    c1 = Circle(Point(1.0, 1.0), 2.0)
    print(c0.intersect(c1))

    c0 = Circle(Point(1.0, -1.0), 1.5)
    c1 = Circle(Point(-1.0, 1.0), 2.0)
    print(c0.intersect(c1))

    c0 = Circle(Point(-1.0, 1.0), 1.5)
    c1 = Circle(Point(1.0, -1.0), 2.0)
    print(c0.intersect(c1))

    c0 = Circle(Point(1.0, 1.0), 1.5)
    c1 = Circle(Point(-1.0, -1.0), 2.0)
    print(c0.intersect(c1))

