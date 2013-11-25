import copy
import time
import sys
import itertools
from Queue import Queue

bWidth = 7
bHeight = 5

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

CANT_MOVE=-1
CAN_MOVE=0
GOAL = 1

#work around....
wCatRevDirDict = {"u":UP, "l":LEFT, "d":DOWN, "r":RIGHT}

class State:
    def __init__(self, bCat, wCat, board, prev, direction):
        self.bCat = bCat
        self.wCat = wCat
        self.board = board
        self.prev = prev
        self.direction = direction

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Cat:
    def __init__(self, pos, direction, dirVal, dirDict):
        self.pos = pos
        self.direction = direction
        self.dirVal = dirVal
        self.dirDict = dirDict

#print Board State(num).
def printBoard(board):
    print "   |",
    for i in range(bWidth):
        print i + 1,"|",
    print ""
    for i in range(bHeight):
        print i + 1," |",
        for j in range(bWidth):
            #print "%1s" % board[i][j],
            print board[i][j],"|",
        print ""
    print "-------------------------------------------"
    return 

def leftMove(pos):
    pos.x = pos.x - 1
    return pos
def rightMove(pos):
    pos.x = pos.x + 1
    return pos
def upMove(pos):
    pos.y = pos.y - 1
    return pos
def downMove(pos):
    pos.y = pos.y + 1
    return pos

def isOutSpace(pos):
    if pos.x < 0 or pos.y < 0 or pos.x >= bWidth or pos.y >= bHeight:
        return True
    return False

def isHole(pos, board):
    if board[pos.y][pos.x] == "H":
        return True
    return False

def isGoal(pos, board):
    if board[pos.y][pos.x] == "G":
        return True
    return False

#this function is called only when wcat moving,
def isCollision(pos, board):
    if board[pos.y][pos.x] == "B":
        return True
    return False



def checkFish(cat, board):
    #if Fish is exist on right side.
    findFish = False
    prePos = Pos(cat.pos.x, cat.pos.y)
    if not isOutSpace(Pos(cat.pos.x + 1, cat.pos.y)):
        if board[cat.pos.y][cat.pos.x + 1] == "F":
            cat.pos = rightMove(cat.pos)
            cat.direction = RIGHT
            findFish = True
    #LEFT
    if not isOutSpace(Pos(cat.pos.x - 1, cat.pos.y)):
        if board[cat.pos.y][cat.pos.x - 1] == "F":
            cat.pos = leftMove(cat.pos)
            cat.direction = LEFT
            findFish = True
    #DOWN
    if not isOutSpace(Pos(cat.pos.x, cat.pos.y + 1)):
        if board[cat.pos.y + 1][cat.pos.x] == "F":
            cat.pos = downMove(cat.pos)
            cat.direction = DOWN
            findFish = True
    #UP
    if not isOutSpace(Pos(cat.pos.x, cat.pos.y - 1)):
        if board[cat.pos.y - 1][cat.pos.x] == "F":
            cat.pos = upMove(cat.pos)
            cat.direction = UP
            findFish = True
    if findFish == True:
        board[prePos.y][prePos.x] = " "
        board[cat.pos.y][cat.pos.x] = cat.dirDict[cat.direction]
            
    return True

def _move(cat, board):
    #bCatMove
    prePos = Pos(cat.pos.x, cat.pos.y)

    if cat.direction == UP:
        #I may erase equels.
        cat.pos = upMove(cat.pos)
    elif cat.direction == RIGHT:
        cat.pos = rightMove(cat.pos)
    elif cat.direction == DOWN:
        cat.pos = downMove(cat.pos)
    elif cat.direction == LEFT:
        cat.pos = leftMove(cat.pos)

    if isOutSpace(cat.pos):
        return CANT_MOVE
    if isHole(cat.pos, board):
        return CANT_MOVE
    if isCollision(cat.pos, board):
        return CANT_MOVE

    if isGoal(cat.pos, board):
        return GOAL

    #print cat.dirDict
    #print cat.direction
    board[prePos.y][prePos.x] = " "
    board[cat.pos.y][cat.pos.x] = cat.dirDict[cat.direction]
    cat = checkFish(cat, board) #update Pos and Direction.

    return CAN_MOVE

def rotate(bCat, wCat, direction, board):
    rotateDistance = 0
    index = bCat.dirVal.index(bCat.dirDict[bCat.direction])
    while index < len(bCat.dirVal):
        if bCat.dirVal[index] == bCat.dirDict[direction]:
            break
        index = index + 1
        rotateDistance = rotateDistance + 1

    wOffset = wCat.dirVal.index(wCat.dirDict[wCat.direction])
    bCat.direction = direction
    wCat.direction = wCatRevDirDict[wCat.dirVal[rotateDistance + wOffset]]
    """
    print "b:", bCat.dirVal[index]
    print "wOffset:", wOffset
    print rotateDistance
    print "w:", wCat.dirVal[rotateDistance + wOffset]
    """
    board[bCat.pos.y][bCat.pos.x] = bCat.dirVal[index]
    board[wCat.pos.y][wCat.pos.x] = wCat.dirVal[rotateDistance + wOffset]

def getDir(dirStr):
    dir = dirStr.upper()
    if dir == "U":
        return UP
    if dir == "R":
        return RIGHT
    if dir == "D":
        return DOWN 
    if dir == "L":
        return LEFT

def move(bCat, wCat, board):
    bCatResult = _move(bCat, board)
    if bCatResult == CANT_MOVE:
        return CANT_MOVE
    wCatResult = _move(wCat, board)
    if wCatResult == CANT_MOVE:
        return CANT_MOVE

    if bCatResult == GOAL and wCatResult == GOAL:
        return GOAL
    elif bCatResult == GOAL or wCatResult == GOAL:
        return CANT_MOVE
    #printBoard(board)
    return CAN_MOVE 

def parseFiles(f, bCat, wCat):
    lines = f.readlines()
    index = 0
    for l in lines:
        if index == 0:
            bWidth = int(l)
        elif index == 1:
            bHeight = int(l)
            board = [[" " for j in range(bWidth)] for i in range(bHeight)]
            #board = [[] for i in range(bWidth * bHeight)]
            #for i in range(bWidth * bHeight):
            #    board[i].append("")
        else:
            sp = l.split()
            h = int(sp[0]) - 1
            w = int(sp[1]) - 1
            mark = sp[2]
            if mark in bCat.dirVal:
                bCat.pos.x = w
                bCat.pos.y = h
                bCat.direction = getDir(mark)
                """
                print"bCatDir", bCat.dirDict[bCat.direction]
                print "bCatPos", "x:", bCat.pos.x, "y:", bCat.pos.y
                """
            if mark in wCat.dirVal:
                wCat.pos.x = w
                wCat.pos.y = h
                wCat.direction = getDir(mark)
                """
                print"wCatDir", wCat.dirDict[wCat.direction]
                print "wCatPos", "x:", wCat.pos.x, "y:", wCat.pos.y
                """
 
            board[h][w] = mark
        index = index + 1
    return board

def btMovePath(state):
    DirDict = state.bCat.dirVal
    moveStack = []
    resultStack = []
    while state != None:
        resultStack.append(state.board)
        moveStack.append(state.direction)
        state = state.prev
    while moveStack:
        t = moveStack.pop()
        if t is not None:
            print DirDict[t]
    while resultStack:
        printBoard(resultStack.pop())

#main function.
if __name__ == '__main__':
    #pre processing
    argvs = sys.argv
    argc = len(argvs)
    strt = time.time()

    if (argc == 2):
        fileName = argvs[1]
    else:
        fileName = "p0.txt"

    f = open(fileName, 'r')

    bCatDirVal = ["U", "L", "D", "R", "U", "L", "D", "R"]
    wCatDirVal = ["u", "l", "d", "r", "u", "l", "d", "r"]
    bCatDirDict = {UP:"U", LEFT:"L", DOWN:"D", RIGHT:"R"}
    wCatDirDict = {UP:"u", LEFT:"l", DOWN:"d", RIGHT:"r"}

    bCat = Cat(Pos(0, 0), UP, bCatDirVal, bCatDirDict)
    wCat = Cat(Pos(0, 0), UP, wCatDirVal, wCatDirDict)

    board = parseFiles(f, bCat, wCat)
    print "----Init state----"
    printBoard(board)

    q = Queue()
    existTable = {}
    q.put(State(bCat, wCat, board, None, None))
    #print tuple(reduce(lambda x, y: x + y, board))
    existTable[tuple(reduce(lambda x, y: x + y, board))] = True

    path = (UP, LEFT, DOWN, RIGHT)
    while not q.empty():
        a = q.get()
        for d in path:
            _board = copy.deepcopy(a.board)
            _bCat = copy.deepcopy(a.bCat)
            _wCat = copy.deepcopy(a.wCat)
            rotate(_bCat, _wCat, d, _board)
            moveResult = move(_bCat, _wCat, _board)
            if moveResult == CANT_MOVE:
                continue
            elif moveResult == GOAL:
                print "Result Find!!"
                btMovePath(State(_bCat, _wCat, _board, a, d))
                endt = time.time()
                print "time:", endt - strt
                exit()
            key = tuple(reduce(lambda x, y: x + y, _board))
            if key in existTable:
                continue
            existTable[key] = True
            q.put(State(_bCat, _wCat, _board, a, d))
    print "cant' get Result!!!"
