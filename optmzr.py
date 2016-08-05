#!/usr/bin/python

from __future__ import division
from math import fabs, factorial, trunc
import random
from tools import GeometryTools as GT

'''
 Class is callable!
 opt = Optimizator(list)
 if opt("round", 1):
    print opt.target
 
 Call parameters:
    round - search polygon with equal area and coords rounded to ints
    reduce - reduce count of polygon nodes
 
'''

class Optimizator:

    '''
    input - list of lists - [[(x,y), (x,y), (x,y)],[(x,y), (x,y), (x,y)]]
    '''
    def __init__(self, sourcePolygons):
        self.source = []
        for sourcePolygon in sourcePolygons:
            self.source.append(GT.roundCoords(sourcePolygon, 2))
        self.target = []
        self.targetAreas = [GT.area(src) for src in self.source]
        self.foundAreas = [x - x for x in xrange(len(self.source))]
        self.maxLength = 0
        for src in self.source:
            if len(src) > self.maxLength:
                self.maxLength = len(src)
        self.restricted = set()
        self.commonPoints = []
        self.maxHops = 0
        self.hops = 0

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type:
            print '%s: %s %s' % (type, value, traceback)

    def __call__(self, kind, tolerance):
        self.target = []
        if kind == "round":
            return self.__found(tolerance)
        elif kind == "reduce":
            return self.__reduce(tolerance)
        else:
            return self.__error()

    '''
    input - list of lists - [[(x,y), (x,y), (x,y)],[(x,y), (x,y), (x,y)]]
    '''
    def __getCommonPoints(self, listList):
        res = []
        isFirst = (len(self.restricted) == 0)
        for i in listList:
            s1 = set(i)
            tmp = []
            for j in listList:
                s2 = set(j)
                s3 = s1 & s2
                tmp.append(len(s3))
                if (i is not j) and isFirst:
                    self.restricted = self.restricted.union(s3)
            res.append(tmp)
        return res

    '''
    input:
        point - (x, y)
        tolerance - int
    output:
        (x, y)
    '''
    def __randomize(self, point, tolerance):
        if point not in self.restricted:
            random.seed()
            dx = random.randint(-tolerance,tolerance)
            dy = random.randint(-tolerance,tolerance)
            x = point[0] + dx
            y = point[1] + dy
            return (x, y)
        else:
            return point

    def __calcMaxHops(self, tolerance):
        try:
            # n! / k! * (n-k)!
            self.maxHops = trunc(factorial(self.maxLength * (tolerance * 2 + 1)) / \
                           factorial(self.maxLength) * \
                           factorial(self.maxLength * (tolerance * 2 + 1) - (tolerance * 2 + 1)))
        except:
            self.maxHops = 2**63-1

    def __countEqualAreas(self):
        res = True
        i = 0
        while i < len(self.targetAreas):
            if self.targetAreas[i] != self.foundAreas[i]:
                res = False
            if not res:
                break
            i += 1
        return i

    def __isAllCommonPoints(self, lst):
        res = True
        if len(self.commonPoints) > 0:
            for i in xrange(len(self.commonPoints)):
                for j in xrange(len(self.commonPoints[i])):
                    res = self.commonPoints[i][j] == lst[i][j]
                    if not res:
                        break
                if not res:
                    break
        return res

    def __found(self, tolerance):
        res = False
        usedlist = []
        foundCount = 0
        self.__calcMaxHops(tolerance)
        if(len(self.source) > 0) and (len(self.targetAreas) > 0):
            target = []
            for src in self.source:
                target.append(GT.roundCoords(src, 0))
            self.commonPoints = self.__getCommonPoints(target)
            i = 0
            sample = []
            while i < self.maxHops:
                error = False
                if foundCount > 0:
                    sample = sample[0:foundCount]
                else:
                    sample = []
                i += 1
                self.foundAreas = []
                for j in xrange(foundCount, len(target)):
                    tmp = []
                    for xy in target[j]:
                        tmp.append(self.__randomize(xy, tolerance))
                    #error = GT.hasIntersect(tmp)
                    if error:
                        #print "Self-Intersect on contour " +  str(j)+ "! Next iter..."
                        break
                    sample.append(tmp)
                if error:
                    continue
                if sample not in usedlist: # DRY
                    usedlist.append(sample)
                    for lst in sample:
                        self.foundAreas.append(GT.area(lst))
                    print self.foundAreas
                    foundCount = self.__countEqualAreas()
                    if (foundCount == len(target)):
                        #print self.foundAreas
                        print self.__getCommonPoints(sample)
                        print self.commonPoints
                        condition = self.__isAllCommonPoints(self.__getCommonPoints(sample))
                        if (not condition):
                            print condition
                            print "Resetting"
                            foundCount = 0
                        else:
                            self.target.extend(sample)
                            self.hops = i
                            res = True
                            break

        return res
        
    def __reduce(self, tolerance):
        res = False
        for pline in self.source:
            txy = pline[0]
            tmplst = []
            tmplst.append(txy)
            for i in xrange(1,len(pline)):
                if GT.length(txy, pline[i]) > tolerance:
                    tmplst.append(pline[i])
                    txy = pline[i]
            self.target.append(tmplst)
        res = len(self.target) > 0
        return res
        
    def __error(self):
        print "Error: Argument not supported"

if __name__ == "__main__":

    srcCoords = [
          [
          (2315934.75,629819.55),
          (2315981.72,629796.35),
          (2315977.94,629789.46),
          (2315975.60,629791.46),
          (2315966.80,629796.51),
          (2315930.65,629812.44)
          ],
          [
          (2315930.65,629812.44),
          (2315966.80,629796.51),
          (2315975.60,629791.46),
          (2315977.94,629789.46),
          (2315953.19,629744.32),
          (2315936.58,629753.30),
          (2315939.88,629758.95),
          (2315931.06,629764.56),
          (2315927.56,629759.07),
          (2315906.38,629770.37)
          ]
       ]
    myopt = Optimizator(srcCoords)
    for i in xrange(1,5):
        if myopt(i):
            print "Hops count = " + str(myopt.hops) + " of " + str(myopt.maxHops)
            print "Target area = " + str(myopt.targetAreas)
            print "Found area = " + str(myopt.foundAreas)
            print myopt.target
            break
        else:
            print "With tolerance " + str(i) + " not found"
