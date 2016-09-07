
from gridgen import Point, Rectangle, Zone

"""

A = 3545.1, m**2

h = 8.5 * 8.0 = 68.0, m
w = 8.5 * 6.1 = 52.1, m

"""

def get_zones(x, y):
    # mr. Bricolage SF3
    a = Point(42.623801, 23.353842)
    m = Point(42.623706, 23.354146)
    n = Point(42.624090, 23.354344)
    t = m.angle(n)

    cc = 8.5 # column to column offset in meters
    area = 3545.1   # square meters

    height = cc * 8.0
    width = cc * 7.0

    # print('mr.Bricolage SF3')
    # print('area={}, width={}/{}, height={}/{}'.format(area, width, width / cc, height, height / cc))

    r = Zone(a, 82.0, 80.0, t)

    return r.split(x, y)


def get_borders():
    # mr. Bricolage SF3
    a = Point(42.623801, 23.353842)
    m = Point(42.623706, 23.354146)
    n = Point(42.624090, 23.354344)
    t = m.angle(n)

    cc = 8.5 # column to column offset in meters

    height = cc * 8.0
    width = cc * 7.0

    return Rectangle(a, width, height, t)


if __name__ == '__main__':

    # mr. Bricolage SF3
    a = Point(42.623801, 23.353842)
    m = Point(42.623706, 23.354146)
    n = Point(42.624090, 23.354344)
    t = m.angle(n)

    cc = 8.5 # column to column offset in meters
    area = 3545.1   # square meters

    height = cc * 8.0
    width = cc * 7.0

    print('mr.Bricolage SF3')
    print('area={}, width={}/{}, height={}/{}'.format(area, width, width / cc, height, height / cc))

    r = Rectangle(a, width, height, t)
    print(r)

    sensors = [
        Point(cc * 1.4, cc * 1.4),  # 1
        Point(cc * 1.9, cc * 4.0),  # 2
        Point(cc * 1.0, cc * 5.5),  # 3
        Point(cc * 3.5, cc * 6.9),  # 4
        Point(cc * 5.0, cc * 7.0),  # 5
        Point(cc * 5.0, cc * 4.8),  # 6
        Point(cc * 7.5, cc * 4.6),  # 7
        Point(cc * 7.0, cc * 3.0),  # 8
        Point(cc * 4.5, cc * 2.0),  # 9
        Point(cc * 4.0, cc * 0.0)]  # 10

    for s in sensors:
        n = a.offset(s.lon, s.lat)
        z = a.angle(n)
        m = a.slide(a.distance(n), t + z)
        print('Point({}),'.format(m))
