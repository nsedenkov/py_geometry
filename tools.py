#!/usr/bin/python
#! coding: utf-8

from math import sqrt, acos, degrees, trunc, fabs, modf

class GeometryTools:

    '''
    clist - [(x,y),(x,y),(x,y)]
    precision - count of decimal signs
    '''
    def roundCoords(clist, precision):
        res = []
        for xy in clist:
            txy = (round(xy[0],precision), round(xy[1],precision))
            res.append(txy)
        return res

    roundCoords = staticmethod(roundCoords)

    '''
    input (x,y)
    returns float
    '''
    def length(xy1, xy2):
        return sqrt(((xy1[0] - xy2[0]) ** 2) + ((xy1[1] - xy2[1]) ** 2))
        
    length = staticmethod(length)

    '''
    clist - [(x,y),(x,y),(x,y)]
    returns float
    '''
    def area(clist):
        area = 0
        args = clist
        for i in xrange(len(args)):
            x1, y1 = args[i - 1]
            x2, y2 = args[i]
            area += x1*y2 - x2*y1
        return round(fabs(area / 2), 0)

    area = staticmethod(area)

    '''
    clist - [(x,y),(x,y),(x,y)]
    returns boolean
    '''
    def isConvexPolygon(clist): 
        res = False
        signPrime = 0
        cnt = len(clist)
        for i in xrange(cnt):
            signPrime = GeometryTools.__getSignVertex( clist[i],
                                            clist[(i+1) % cnt],
                                            clist[(i+2) % cnt])
            if signPrime != 0:
                break
        if signPrime == 0:
            return res
        for i in xrange(cnt):
            signNext = GeometryTools.__getSignVertex( clist[i],
                                           clist[(i+1) % cnt],
                                           clist[(i+2) % cnt])
            if signNext != signPrime and signNext != 0:
                return res
        res = True
        return res

    isConvexPolygon = staticmethod(isConvexPolygon)
        
    '''
    sign of Vertex
    returns -1, 0 , 1
    '''
    def __getSignVertex(xy1, xy2, xy3): # xy# - (x,y)
        res = 0
        area = (xy2[0] - xy1[0]) * (xy3[1] - xy1[1]) - (xy3[0] - xy1[0]) * (xy2[1] - xy1[1])
        if area == 0:
            return res
        if area > 0:
            res = 1 
        if area < 0:
            res = -1
        return res
        
    __getSignVertex = staticmethod(__getSignVertex)

    '''
    self-intersections in contour
    returns boolean
    '''
    def hasIntersect(clist): # clist - [(x,y),(x,y),(x,y)]
        def intersect(a,b,c,d):
            if a > b:
                a,b = b,a
            if c > d:
                c,d = d,c
            return max(a,c) <= min(b,d)
        
        res = False
        cnt = len(clist)
        for i in xrange(cnt): # clist[i] - clist[j] - 1st line
            j = i+1
            if i == cnt-1:
                j = 0
            for k in xrange(cnt): # clist[k] - clist[z] - 2nd line
                z = k+1
                if k == cnt-1:
                    z = 0
                if (i != k) and (i!= z) and (j != k) and (j != z): # if no common points
                    res = intersect(clist[i][0], clist[j][0], clist[k][0], clist[z][0]) and \
                          intersect(clist[i][1], clist[j][1], clist[k][1], clist[z][1]) and \
                          (GeometryTools.area([clist[i], clist[j], clist[k]]) * GeometryTools.area([clist[i], clist[j], clist[z]]) <= 0) and \
                          (GeometryTools.area([clist[k], clist[z], clist[i]]) * GeometryTools.area([clist[k], clist[z], clist[j]]) <= 0)
                if res:
                    break
            if res:
                break
        return res

    hasIntersect = staticmethod(hasIntersect)

    '''
    input - 2 tuples (x, y)
    returns - float
    static method !
    '''
    def getMathAngle(t1, t2):
        return degrees(acos(fabs(t1[1] - t2[1]) / GeometryTools.length(t1, t2)))

    getMathAngle = staticmethod(getMathAngle)

    '''
    input - 2 tuples (x, y)
    returns - tuple (d, m, dm)
    static method !
    '''
    def getDirectionAngle(t1, t2):
        da = GeometryTools.getMathAngle(t1, t2)
        if (t1[0] < t2[0]) and (t1[1] > t2[1]): # 2nd quater
            da = 180 - da
        elif (t1[0] >= t2[0]) and (t1[1] >= t2[1]): # 3rd quater
            da = 180 + da
        elif (t1[0] > t2[0]) and (t1[1] <= t2[1]): # 4th quater
            da = 360 - da
        return (trunc(da), trunc(modf(da)[0] * 60), trunc((modf(da)[0] * 60 -  modf(modf(da)[0] * 60)[1]) * 100 ))
        
    getDirectionAngle = staticmethod(getDirectionAngle)

    '''
    input - 2 tuples (x, y)
    returns - tuple (d, m, dm, str)
    static method !
    '''
    def getRumbAngle(t1, t2):
        TplRumb = (u'СВ', u'ЮВ', u'ЮЗ', u'СЗ')
        da = GeometryTools.getMathAngle(t1, t2)
        st = TplRumb[0]
        if (t1[0] < t2[0]) and (t1[1] > t2[1]): # 2nd quater
            st = TplRumb[1]
        elif (t1[0] >= t2[0]) and (t1[1] >= t2[1]): # 3rd quarter
            st = TplRumb[2]
        elif (t1[0] > t2[0]) and (t1[1] <= t2[1]): # 4th quarter
            st = TplRumb[3]
        return (trunc(da), trunc(modf(da)[0] * 60), trunc((modf(da)[0] * 60 -  modf(modf(da)[0] * 60)[1]) * 100 ), st)

    getRumbAngle = staticmethod(getRumbAngle)

class CoordListTools:
    
    '''
    input: list of tuples (x, y)
           direction: N, S, E, W
    returns: one tuple or None in case of error
    static method !
    '''
    def getUltimateDirPoint(clist, direction):
        dicDirection = {
            'N':{'elem':1, 'sign': 'more'},
            'S':{'elem':1, 'sign': 'less'},
            'E':{'elem':0, 'sign': 'more'},
            'W':{'elem':0, 'sign': 'less'}
            }
        if direction not in dicDirection:
            return None
        rxy = clist[0]
        for txy in clist:
            if dicDirection[direction]['sign'] == 'more':
                if txy[dicDirection[direction]['elem']] > rxy[dicDirection[direction]['elem']]:
                    rxy = txy
            else: # less
                if txy[dicDirection[direction]['elem']] < rxy[dicDirection[direction]['elem']]:
                    rxy = txy
        return rxy

    getUltimateDirPoint = staticmethod(getUltimateDirPoint)
    
    '''
    input: list of tuples (x, y)
           direction: N, S, E, W
    returns: swapped list with start point is ultimate point
    static method !
    '''
    def swapPointList(clist, direction):
        res = []
        SP = CoordListTools.getUltimateDirPoint(clist, direction)
        if SP is None:
            return None
        res.extend(clist[clist.index(SP):len(clist)])
        res.extend(clist[0:clist.index(SP)])
        return res

    swapPointList = staticmethod(swapPointList)
    
    '''
    input: list of tuples (x, y), or any other list
    returns: reversed list
    static method !
    '''
    def reverseList(clist):
        lIdx = 0
        hIdx = len(clist) - 1
        while hIdx - lIdx >= 1:
            clist[lIdx], clist[hIdx] = clist[hIdx], clist[lIdx]
            lIdx += 1
            hIdx -= 1
        return clist

    reverseList = staticmethod(reverseList)
    
    '''
    input: list of lists [[(x,y), (x,y), (x,y)],[(x,y), (x,y), (x,y)]]
    returns: list of unique points
    static method !
    '''
    def getUniquePointsList(listList):
        res = []
        for lst in listList:
            for txy in lst:
                if res.count(txy) == 0:
                    res.append(txy) 
        return res

    getUniquePointsList = staticmethod(getUniquePointsList)
    
    '''
    input: TWO list of lists [[(x,y), (x,y), (x,y)],[(x,y), (x,y), (x,y)]]
    returns: list of indexes in FIRST list wich haves common points with
             contours in SECOND list
    static method !
    '''
    def findRelatedContours(lst1, lst2):
        res = []
        for tmpcrd in lst2:
            idx = -1
            m1 = set(tmpcrd)
            for crdlst in lst1:
                m2 = set(crdlst)
                # if power of intersection gt 0 - nearest contour found
                if len(m1 & m2) > 0:
                    idx = lst1.index(crdlst)
                    if not idx in res:
                        res.append(idx)
        return res

    findRelatedContours = staticmethod(findRelatedContours)
    
    '''
    input: TWO list of lists [[(x,y), (x,y), (x,y)],[(x,y), (x,y), (x,y)]]
    returns: index in FIRST list wich haves point, nearest to
             contours in SECOND list
    static method !
    '''
    def findNearestContour(lst1, lst2):
        res = -1
        minlen = 1000000
        dirs = ['N', 'S', 'W', 'E']
        PP = None
        lxy = CoordListTools.getUniquePointsList(lst1)

        for tmpcrd in lst2:
            for txy in tmpcrd:
                for curDir in dirs:
                    CP = CoordListTools.getUltimateDirPoint(lxy, curDir)
                    curlen = GeometryTools.length(txy, CP)
                    if curlen < minlen:
                        minlen = curlen
                        PP = CP

        for crdlst in lst1:
            if PP in crdlst:
                res = lst1.index(crdlst)

        return res

    findNearestContour = staticmethod(findNearestContour)
    
    '''
    input: list of lists [[(x,y), (x,y), (x,y)],[(x,y), (x,y), (x,y)]]
    returns: list of lists sorted from direction (N, S, E, W)
    static method !
    '''
    def sortPointList(listList, direction):
        res = []
        
        lxy = CoordListTools.getUniquePointsList(listList)
        uPoint = CoordListTools.getUltimateDirPoint(lxy, direction)
        
        # First contour - owner of ultimate point    
        idx = -1
        for lst in listList:
            if uPoint in lst:
                idx = listList.index(lst)
        res.append(CoordListTools.swapPointList(listList.pop(idx), direction))
        
        looplst = []
        looplst.extend(res)
        while len(listList) > 0:
            # list for founded indexes
            lidx = CoordListTools.findRelatedContours(listList, looplst)
            
            # list of found contours - lives 1 iteration
            fndlst = []
            
            if len(lidx) > 0:
                i = 0
                for idx in lidx:
                    idx -= i # Сдвиг индекса в случае удаления нескольких записей (на 2 шаге -1 и т.д.)
                    i += 1
                    fndlst.append(CoordListTools.swapPointList(listList.pop(idx), direction))
            else:
                idx = CoordListTools.findNearestContour(listList, looplst)
                fndlst.append(CoordListTools.swapPointList(listList.pop(idx), direction))

            del looplst[0:len(looplst)]
            looplst.extend(fndlst)
            del fndlst[0:len(fndlst)]
            res.extend(looplst)
        return res

    sortPointList = staticmethod(sortPointList)

if __name__ == "__main__":
    lst = [(1,1), (2,1), (3,3), (4,2), (7, 10), (3,3)]
    print CoordListTools.swapPointList(lst, "N")
    print CoordListTools.reverseList(lst)
    print CoordListTools.getUniquePointsList([lst,])
