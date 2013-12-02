if __debug__:
    import matplotlib.pyplot as plt

import argparse
import math
import time
import sys
import itertools
from Queue import Queue

width = 500
height = 500
margin = 250 #this variable is used for graphplot

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def show(self):
        print "x:", self.x, " y:", self.y

class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def show(self):
        print "x:", self.x, " y:", self.y

class DisInfo:
    def __init__(self, c, p, d):
        self.c = c
        self.pos = p
        self.d = d

    def show(self):
        print "c.x:", self.c.pos.x, "c.y:", self.c.pos.y
        print "x:", self.pos.x, " y:", self.pos.y
        print "distance:", self.d

class Circle:
    def __init__(self, p, r):
        self.pos = p
        self.r = r
        self.incList = [] #include list of points.
        self.vIncList = [] #virtual include list of points.

    def show(self):
        print "x:", self.pos.x, " y:", self.pos.y
        print "radius:", self.r


def graphPlot(dataList, circleList, convexList):
    fig = plt.figure(1, figsize=(6,6))
    plt.xlim(0 - margin, width + margin)
    plt.ylim(0 - margin, height + margin)

    #write data list
    xList = []
    yList = []
    for p in dataList:
        xList.append(p.x)
        yList.append(p.y)

    if xList:
        plt.scatter(xList, yList, color="r", marker=".", label="hoge")

    #write circles
    ax = fig.gca()
    for c in circleList:
        circle = plt.Circle( (c.pos.x, c.pos.y), c.r, edgecolor="black",
                facecolor="none")
        ax.add_artist(circle)

    #write convex list
    xList = []
    yList = []
    prevP = None
    firstP = None
    for p in convexList:
        xList.append(p.x)
        yList.append(p.y)
        if prevP is None:
            firstP = p
        else:
            plt.plot([prevP.x, p.x], [prevP.y, p.y], "k-")
        prevP = p

    if xList:
        plt.plot([prevP.x, firstP.x], [prevP.y, firstP.y], "k-")
        plt.scatter(xList, yList, color="b", marker="x", label="convex hull")


    #show plot result!
    plt.show()
    #fig.savefig("Model.png", dpi=150)

#output result
def printOutput(cList):
    print len(cList)
    for c in cList:
        print int(c.pos.x), int(c.pos.y), int(c.r)

def getVecLen(v):
    return (v.x **2 + v.y **2) ** 0.5
def dot(p1, p2):
    return p1.x * p2.x + p1.y * p2.y

def getLowestYPoint(posList):
    lowP = Pos(0, 500)
    for p in posList:
        if p.y < lowP.y:
            lowP = p
    return lowP

def checkWithinCircle(pList, c):
    r2 = c.r * c.r
    for p in pList:
        if ((p.x - c.pos.x) ** 2) + ((p.y - c.pos.y) ** 2) >= r2:
            #print "--------------------"
            #print "it is not within circle"
            #print "P:",
            #p.show()
            #print "C:",
            #c.show()
            #print "distance:", getDis(p, c.pos)
            #print "--------------------"
            return False
    return True

def getCos(v1, v2):
    return dot(v1, v2) / (getVecLen(v1) * getVecLen(v2))

def getTriArea(p1, p2, p3):
    return abs(0.5 * ((p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)))

def getCenterCircumCircle(p0, p1, p2):
    dA = p0.x * p0.x + p0.y * p0.y;
    dB = p1.x * p1.x + p1.y * p1.y;
    dC = p2.x * p2.x + p2.y * p2.y;

    aux1 = (dA*(p2.y - p1.y) + dB*(p0.y - p2.y) + dC*(p1.y - p0.y));
    aux2 = -(dA*(p2.x - p1.x) + dB*(p0.x - p2.x) + dC*(p1.x - p0.x));
    div = (2*(p0.x*(p2.y - p1.y) + p1.x*(p0.y-p2.y) +
    p2.x*(p1.y - p0.y)));

    if div == 0:
        return False;

    #aux1 and div is sometimes has big value,
    #so precision error is occured.
    center = Pos(aux1 / div, aux2 / div)

    radius = math.sqrt((center.x - p0.x)*(center.x - p0.x) +
            (center.y - p0.y)*(center.y - p0.y));
    return Circle(center, radius)
    
def isAcute(v1, v2):
    if getCos(v1, v2) <= 0:
        #print "cos:",getCos(v1, v2)
        return False
    else:
        return True

def getMinimumCircle(convList):
    if len(convList) < 3:
        s = len(convList)
        pos = Pos(0, 0)
        for p in convList:
            pos.x += p.x
            pos.y += p.y

        pos.x = pos.x / s
        pos.y = pos.y / s
        #because of precision problem.
        r = math.ceil(max(getDis(convList[0], pos), getDis(convList[1], pos))) + 1
        pos.x = round(pos.x)
        pos.y = round(pos.y)

        return Circle(pos, r)

    minC = None
    for pList in itertools.combinations(convList,3):
        maxSide = 0 
        for twoPos in itertools.combinations(pList, 2):
            side = getVecLen(Vec(twoPos[0].x - twoPos[1].x,
                twoPos[0].y - twoPos[1].y))
            if maxSide < side:
                maxSide = side
                maxTwoPos = twoPos
        topPos = list(set(pList) - set(maxTwoPos))[0]
        #topPos.show()

        #is it Acute?
        if isAcute(Vec(maxTwoPos[0].x - topPos.x, maxTwoPos[0].y - topPos.y),
                Vec(maxTwoPos[1].x - topPos.x, maxTwoPos[1].y - topPos.y)):
            #gaishin!
            c = getCenterCircumCircle(pList[0], pList[1], pList[2])
            #c.show()
            c.pos.x = round(c.pos.x)
            c.pos.y = round(c.pos.y)
            #because of precision problem.
            #c.r = math.ceil(c.r) + 2
            c.r = math.ceil(c.r) + 3
            #cList = []
            #cList.append(c)
            #graphPlot(convList, cList, pList)
        else: #90 also executes this flow
            midP = Pos((maxTwoPos[0].x + maxTwoPos[1].x) / 2,
                    (maxTwoPos[0].y + maxTwoPos[1].y) / 2)
            r = getVecLen(Vec(maxTwoPos[0].x - midP.x, maxTwoPos[0].y - midP.y))
            c = Circle(midP, r)
            c.pos.x = round(c.pos.x)
            c.pos.y = round(c.pos.y)
            #because of precision problem.
            c.r = math.ceil(c.r) + 2

        if checkWithinCircle(convList, c):
            minC = c
            break

    if minC is None:
        #graphPlot([], [], convList)
        #for p in convList:
        #    print p.x, p.y
        exit()

    return minC

def getConvexHull(posList):
    convList = []
    lowP = getLowestYPoint(posList)
    convList.append(lowP)

    currentP = lowP
    prevVec = Vec(1, 0)
    nextP = Pos(-1, -1)
    while nextP is not lowP:
        maxCosVal = -2
        for p in posList:
            if currentP is p:
                continue
            cosVal = getCos(prevVec, Vec(p.x - currentP.x, p.y - currentP.y))
            if cosVal > maxCosVal:
                maxCosVal = cosVal
                nextP = p
        convList.append(nextP)
        prevVec = Vec(nextP.x - currentP.x, nextP.y - currentP.y)
        currentP = nextP

    #remove Last(duplicate) Pos!
    convList.pop()
    return convList
        

def getDis(p1, p2):
    return math.sqrt( (p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def printDList(dlist):
    for d in dList:
        d.show()

if __name__ == '__main__':
    #parse arguments
    parser = argparse.ArgumentParser(description="plot circle-clip dataList and\
            result to graph. matplotlib is required. if your environmentdoesn't\
            have this library, please use -O option.\
            Ex:python -O circle-clip.py -p prb.txt > ans.txt")
    parser.add_argument("-p", "--posData", nargs="?", type=argparse.FileType("r"),
            default="./prb.txt", help="data filename")
    #parser.add_argument("-o", "--outImage", nargs="?", type=argparse.FileType("w"),
    #        default="./plot.png", help="output filename")

    args = parser.parse_args()
    strt = time.time()

    #read pos Data
    lines = args.posData.readlines()
    index = 0
    dataList = []
    circleList = []
    pToCDic = {} #pos to circle dictionary
    for l in lines:
        if index == 0:
            dNum= int(l)
        elif index == 1:
            cMaxNum = int(l)
        else:
            sp = l.split()
            x = int(sp[0]) 
            y = int(sp[1])
            p = Pos(x,y)
            dataList.append(p)

        index = index + 1

    #remove duplicate pos!
    dataList = sorted(set(dataList), key=dataList.index)

    for p in dataList:
        c = Circle(p, 1)
        c.incList.append(p)
        circleList.append(c)
        pToCDic[p] = c

    cNum = len(dataList)
    #processing start!
    #dNum = number of data.
    #cMaxNum = limit number of circles.

    #calc distance between circle center and points
    #that is not included to own circle.
    dList = []
    for c in circleList:
        for p in dataList:
            if p not in c.incList:
                dList.append(DisInfo(c, p, getDis(p, c.pos)))

    #sorted by distance!
    dList.sort(cmp=lambda x, y:cmp(x, y), key=lambda x:x.d)

    #printDList(dList)

    while cMaxNum < len(circleList):
        #if time exceeds, get 1circle result immediately!
        if time.time()- strt > 55:
            circleList = []
            convList = getConvexHull(dataList)
            c = getMinimumCircle(convList)
            circleList.append(c)
            break

        for d in dList:
            if d.pos not in d.c.vIncList:
                d.c.vIncList.append(d.pos)

            #change Pos list to tuple, for compare.
            #more smart way may be exist...
            tVInc = []
            tInc = []
            for p in d.c.vIncList:
                tVInc.append((p.x, p.y))
            for p in pToCDic[d.pos].incList:
                tInc.append((p.x, p.y))

            #if vIncList includes all of point of another circle,
            if set(tVInc).issuperset(set(tInc)):
                #print "tVInc", tuple(tVInc)
                #print "tInc", tuple(tInc)
                c = d.c

                #vIncList also includes another point that is included in
                #another circle. so we shoule use pToCDic[].incList
                #c.incList = c.incList + c.vIncList
                c.incList = c.incList + pToCDic[d.pos].incList

                #calculate the minimum circle that can include points.
                convList = getConvexHull(c.incList)
                _c = getMinimumCircle(convList)
                _c.incList = c.incList

                #remove old circles and add new circle.
                circleList.remove(c)
                circleList.remove(pToCDic[d.pos])
                circleList.append(_c)

                #graphPlot(dataList, circleList, convList)

                #remove part of dList with old circles
                dList = filter(lambda x: x.c is not c, dList)
                dList = filter(lambda x: x.c is not pToCDic[d.pos], dList)

                #update pToCDic
                for p in _c.incList:
                    pToCDic[p] = _c

                #recalculate distance between new circle and other points.
                for p in dataList:
                    if p not in _c.incList:
                        dList.append(DisInfo(_c, p, getDis(p, _c.pos)))

                #sorted by distance!
                dList.sort(cmp=lambda x, y:cmp(x, y), key=lambda x:x.d)
                break

    if __debug__:
        graphPlot(dataList, circleList, [])
    printOutput(circleList)
