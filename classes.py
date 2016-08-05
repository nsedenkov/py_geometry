#!/usr/bin/python

from tools import GeometryTools as GT

class Point:

    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z
        self.name = ''
        self.owners = []

    def __repr__(self):
        res = "(" + str(self.x) + "," + str(self.y)
        if self.z is not None:
            strend = "," + str(self.z) + ")"
            res += strend
        else:
            res += ")"
        return res

    def setName(self, name):
        self.name = name

    def setOwner(self, owner):
        if isinstance(owner, Line):
            self.owners.append(owner)

    def isOwner(self, obj):
        return (isinstance(obj, Line) and (obj in self.owners))

class Line:

    def __init__(self, p1, p2):
        self.owners = []
        if isinstance(p1, Point):
            self.start = p1
            self.start.setOwner(self)
        if isinstance(p2, Point):
            self.end = p2
            self.end.setOwner(self)
        self.length = GT.length((self.start.x, self.start.y), (self.end.x, self.end.y))

    def __repr__(self):
        return str(self.start) + " - " + str(self.end)
        
    def setOwner(self, owner):
        if isinstance(owner, Border):
            self.owners.append(owner)

    def isOwner(self, obj):
        return (isinstance(obj, Border) and (obj in self.owners))

class Border:

    def __init__(self, lines):
        self.owner = None
        self.isOuter = True
        self.isClosed = False
        self.area = 0
        self.perimeter = 0
        self.lines = []
        tmplst = []
        for lin in lines:
            if isinstance(lin, Line):
                lin.setOwner(self)
                self.lines.append(lin)
                self.perimeter += lin.length
        self.__closeBorder()
        self.__calcArea()

    def __repr__(self):
        res = '['
        for i in xrange(len(self.lines)):
            res += str(self.lines[i].start)
            if i != len(self.lines)-1:
                res += ','
        res += ']'
        return res
        
    def __calcArea(self):
        tmplst = []
        if self.isClosed:
            for lin in self.lines:
                tmplst.append(lin.start.x, lin.start.y)
            self.area = GT.area(tmplst)

    def __closeBorder(self):
        if len(self.lines) > 1:
            if not self.lines[len(self.lines)-1].end is self.lines[0].start:
                # TODO: Not registered Line - refactor to use factory
                tmp = Line(self.lines[len(self.lines)-1].end, self.lines[0].start)
                tmp.setOwner(self)
                self.perimeter += tmp.length
                self.lines.append(tmp)
            self.isClosed = True

    def getLinesCount(self):
        return len(self.lines)

    def getPointsCount(self):
        return self.getLinesCount()

    def setOwner(self, owner):
        if isinstance(owner, Contour):
            self.owner = owner

    def isOwner(self, obj):
        return  (obj is self.owner)

class Contour:

    def __init__(self, borders):
        self.owner = None
        self.borders = []
        for brd in borders:
            if isinstance(brd, Border):
                brd.setOwner(self)
                self.borders.append(brd)

    def setOwner(self, owner):
        if isinstance(owner, Parcel):
            self.owner = owner

    def isOwner(self, obj):
        return  (obj is self.owner)

class Parcel:

    def __init__(self, contours):
        self.contours = []
        for i in xrange(len(contours)):
            if isinstance(contours[i], Contour):
                contours[i].setOwner(self)
                self.contours.append(contours[i])

if __name__ == "__main__":
    p1 = Point(123.45, 456.78)
    p2 = Point(453.67, 987.25)
    p3 = Point(453.67, 987.25)
    p4 = Point(453.67, 987.25)
    p5 = Point(453.67, 987.25)
    p6 = Point(453.67, 987.25)
    l1 = Line(p1, p2)
    l2 = Line(p2, p3)
    l3 = Line(p3, p4)
    b1 = Border([l1, l2, l3])
    print b1.getPointsCount()
    print l1.length
