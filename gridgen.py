# 42.623833, 23.353693
# 42.624525, 23.354109
# 42.624743, 23.353345
# 42.624106, 23.352924

from math import cos, sin, asin, sqrt, pi, degrees, radians


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
        r = 6378137.0
        return c * r

    def offset(self, delta_east, delta_nort):
        """
        Algorithm for offsetting a latitude/longitude by some amount of meters
        """
        # Coordinate offsets in radians
        r = 6378137.0
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
        return '{}'.format(self.visited)

    def visit(self):
        self.visited += 1


def get_bricolage_zones(x, y):
    a = Point(42.623833, 23.353693)

    m = Point(42.623706, 23.354146)
    n = Point(42.624090, 23.354344)
    t = m.angle(n)

    # mr. Bricolage SF3
    r = Zone(a, 60, 50, t)

    return r.split(x, y)


if __name__ == '__main__':
    a = Point(42.623833, 23.353693)
    b = Point(42.624531, 23.354114)
    c = Point(42.624743, 23.353345)
    d = Point(42.624095, 23.352912)

    # random point
    z = Point(51.0, 0.0)
    z = z.offset(0, 100.0)
    # print(z)

    m = Point(42.623706, 23.354146)
    n = Point(42.624090, 23.354344)
    t = m.angle(n)

    # mr. Bricolage SF3
    r = Rectangle(a, 60, 50, t)
    print(r)

    # Unit Tests?
    print('Is poligon center inside poligon? {}'.format(r.contain(r.center())))
    print('Is random point inside poligon?   {}'.format(r.contain(z)))

    grid = r.split(10, 10)
    for r in grid:
        print(r)

