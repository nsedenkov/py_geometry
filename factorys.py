#!/usr/bin/python

from classes import Point, Line

class PointFactory:

    registry = []

    def newPoint(x, y, z=None):
        res = None
        for point in PointFactory.registry:
            if (point.x == x) and (point.y == y) and (point.z == z):
                res = point
                break
        if res is None:
            res = Point(x,y,z)
            PointFactory.registry.append(res)
        return res

    newPoint = staticmethod(newPoint)

class LineFactory:

    registry = []

    def newLine(p1, p2):
        res = None
        if isinstance(p1, Point) and isinstance(p2, Point):
            for line in LineFactory.registry:
                if (line.start is p1) and (line.end is p2):
                    res = line
                    break
            if res is None:
                res = Line(p1, p2)
                LineFactory.registry.append(res)
        return res

    newLine = staticmethod(newLine)

if __name__ == "__main__":
    p1 = PointFactory.newPoint(1,2)
    print p1
    p2 = PointFactory.newPoint(3,2,4)
    p3 = PointFactory.newPoint(3,2,4)
    if p2 is p3:
        print "Yes"
