# 42.623833, 23.353693
# 42.624525, 23.354109
# 42.624743, 23.353345
# 42.624106, 23.352924


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


def generate_line(p1, p2):
    for x in range(0, 11):
        delta = 0.1 * x
        x = p1.x + (p2.x - p1.x) * delta
        y = p1.y + (p2.y - p1.y) * delta
        print('{},{}'.format(x, y))


def generate_grid(A, B, C, D):
    for x in range(0, 11):
        dx = 0.1 * x

        x = A.x + (B.x - A.x) * dx
        y = A.y + (B.y - A.y) * dx
        L = Point(x, y)

        x = D.x + (C.x - D.x) * dx
        y = D.y + (C.y - D.y) * dx
        N = Point(x, y)

        generate_line(L, N)


if __name__ == '__main__':
    A = Point(42.623833, 23.353693)
    B = Point(42.624531, 23.354114)
    C = Point(42.624743, 23.353345)
    D = Point(42.624095, 23.352912)

    generate_grid(A, B, C, D)