import copy
import time
import sys
import itertools

N = 4
NN = N * N

def printBoard(c, lu, ld, ru, rd):
    lt = set(lu) - set(ld) - set(ru)
    rt = set(ru) - set(rd) - set(lu)
    lb = set(ld) - set(lu) - set(rd)
    rb = set(rd) - set(ru) - set(ld)
    topLine = (set(lu) | set(ru)) - set(ld) - set(rd) - lt - rt
    bottomLine = (set(ld) | set(rd)) - set(lu) - set(ru) - lb - rb
    leftLine = (set(lu) | set(ld)) - set(ru) - set(rd) - lt - lb 
    rightLine = (set(ru) | set(rd)) - set(lu) - set(ld) - rt - rb 
    center = list(c)
    print "{0:2d}|".format(lt.pop()),
    for k in topLine:
        print "{0:2d}|".format(k),
    print "{0:2d}|".format(rt.pop())
    for i in range(N - 2):
        print "{0:2d}|".format(leftLine.pop()),
        for i in range(N - 2):
            print "{0:2d}|".format(center.pop()),
        print "{0:2d}|".format(rightLine.pop())
    print "{0:2d}|".format(lb.pop()),
    for k in bottomLine:
        print "{0:2d}|".format(k),
    print "{0:2d}|".format(rb.pop())
    print "---------------"

def checkResult(b):
    leftup = b[0] + b[1] + b[3] + b[4]
    rightup = b[1] + b[2] + b[4] + b[5]
    if leftup != rightup:
        return False
    leftdown = b[3] + b[4] + b[6] + b[7]
    rightdown = b[4] + b[5] + b[7] + b[8]
    if leftdown != rightdown:
        return False
    if leftup != leftdown:
        return False
    return True

#main function.
if __name__ == '__main__':
    #pre processing
    argvs = sys.argv
    argc = len(argvs)
    strt = time.time()

    numbers = range(1,NN + 1)
    len = 0
    #center
    for c in itertools.combinations(numbers, (N - 2) ** 2):
        center_sum = reduce(lambda x, y: x + y, c)
        remain_num_c = list(set(numbers) - set(c))

        #left-up
        for lu in itertools.combinations(remain_num_c, (N - 1) ** 2 - (N - 2) ** 2):
            lu_sum = reduce(lambda x, y: x + y, lu)
            remain_num_lu = list(set(remain_num_c) - set(lu))

            #right-down
            for rd in itertools.combinations(remain_num_lu, (N - 1) ** 2 - (N - 2) ** 2):
                rd_sum = reduce(lambda x, y: x + y, rd)
                remain_num_rd = list(set(remain_num_lu) - set(rd))

                if lu_sum == rd_sum:
                    #calc ld_sum use lu,rd
                    #if ld_sum equals lu/rd,
                    #left-down
                    for ld_from_lu in itertools.combinations(lu, N - 2):
                        ld_sum_ = reduce(lambda x, y: x + y, ld_from_lu) + remain_num_rd[0]

                        for ld_from_rd in itertools.combinations(rd, N - 2):
                            ld_sum = ld_sum_ + reduce(lambda x, y: x + y, ld_from_rd)

                        if ld_sum == lu_sum:
                            lu_last = list(set(lu) - set(ld_from_lu))
                            rd_last = list(set(rd) - set(ld_from_rd))
                            ld = tuple([remain_num_rd[0]]) + ld_from_lu + ld_from_rd
                            
                            #right-up
                            for ru_from_lu in itertools.combinations(lu_last, N - 2):
                                ru_sum_ = reduce(lambda x, y: x + y, ru_from_lu) + remain_num_rd[1]

                                for ru_from_rd in itertools.combinations(rd_last, N - 2):
                                    ru_sum = ru_sum_ + reduce(lambda x, y: x + y, ru_from_rd)

                                if ru_sum == lu_sum:
                                    ru = tuple([remain_num_rd[1]]) + ru_from_lu + ru_from_rd
                                    print "answer found"
                                    printBoard(c, lu, ld, ru, rd)
                                    endt = time.time()
                                    print "time:{0:0.5f}[sec]".format(endt - strt)
                                    exit()
