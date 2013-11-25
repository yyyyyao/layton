import time
import sys
import itertools

#show result
def showResult(underList):
    pVal= 0
    cVal = 0
    nData = []
    inData = underList
    index = 0

    print "----------------"
    for i in underList:
        print "{0:3d}".format(i),
    print ""

    while inData:
        index = index + 1
        i = inData.pop(0)
        if index == 1:
            pVal = i
            continue
        cVal = i
        val = abs(pVal - cVal)

        nData.append(val)
        pVal = cVal

        if not inData:
            for i in nData:
                print "{0:3d}".format(i),
            print ""
            inData = nData 
            nData = []
            pVal = 0
            cVal = 0
            index = 0
    return 
 
#check result is correct or not
def isAnswer(inData, remain_num):
    pVal= 0 #Left operand value
    cVal = 0 #Right overand value
    index = 0
    nData = []
    while inData:
        index = index + 1
        i = inData.pop(0)
        if index == 1:
            pVal = i
            continue
        cVal = i
        val = abs(pVal - cVal)

        if val not in remain_num:
            #print "False"
            return False
        remain_num.remove(val)
        nData.append(val)
        pVal = cVal

        if not remain_num:
            return True
        if not inData:
            inData = nData 
            nData = []
            pVal = 0
            cVal = 0
            index = 0
    print "this line never executed!"
    return False
        
#main function.
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    strt = time.time()
    N = 5

    if (argc == 2):
        N = int(argvs[1])
        
    #get All of number.
    numN = N * (1 + N) / 2
    numbers = range(1,numN + 1)

    find = False
    #get permutations
    for underList in itertools.permutations(numbers, N):
        temp_numbers = list(set(numbers) - set(underList))

        #check result is correct or not.
        if isAnswer(list(underList), temp_numbers):
            #if result is correct, show result
            showResult(list(underList))
            find = True
    if not find:
        print "nothing result!"

    endt = time.time()
    print "time:{0:0.5f}[sec]".format(endt - strt)
