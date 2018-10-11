
import sys
import os

import optparse
import re
import shutil
import time

# 目标文件夹
COPY_DIR = "resources.googleplay"

# 待过滤的文件夹
SRC_DIR  = "resources.encrypt"

# 限制大小
# 这个是压缩后的大小
# 应该和达到包里的大小差不多
LMT_SIZE = 13 * 1024 * 1024

def createFliter():
    filter = PathExcluder()
    filter.addregex(r"^ccbi/.*$")
    filter.addregex(r"^logo/.*$")
    filter.addregex(r"^sound/.*$")
    filter.addregex(r"^scripts/.*$")
    filter.addregex(r"^spine/.*$")
    filter.addregex(r"^table/.*$")
    filter.addregex(r"^[\w\.]+$")
    return filter




# --------------------------------------------- 分割线 ---------------------------------------------


class PathExcluder():
    def __init__(self):
        self.__regexes = []
        self.__bywhich = None

    def addregex(self, s):
        r = re.compile(s, re.I)
        self.__regexes.append(r)
        return self

    def expellent(self, p):
        self.__bywhich = None
        for r in self.__regexes:
            if r.search(p) != None:
                self.__bywhich = str(r)
                return True
        return False

def mkdir(dirpath):
    if os.path.exists(dirpath):
        return
    os.makedirs(dirpath)

def mkfdir(filepath):
    mkdir(os.path.dirname(filepath))

def parseargs():
    parser = optparse.OptionParser()
    parser.add_option(
        "-d",
        action  = "store",
        dest    = "directory",
        default = "",
        help    = "Set the target resource directory."
        )

    return parser.parse_args()

def ptFirstValue( lst ):
    for i in range(0, len(lst)):
        print( "%03d - %s", i, lst[i] )

def ptTup( lst ):
    for i in range(0, len(lst)):
        ii = lst[i]
        print( "%03d - %s, %s" %( i, ii[1], ii[2] ))

    print( "count", len(lst))

def write_csv( reserve, dstfd ):

    f = os.path.join( dstfd, "list.csv")
    
    csv = ""
    
    for i in reserve:
        csv += "%s,%s,%s\r\n" % ( i[0], i[1], i[2] )
    
    with open(f, "wb") as fout:
        fout.write( csv.encode() )

def do_copying( reserve, srcfd, dstfd ):

    for i in reserve:
        k = i[2]
        k = k[:-3]

        src = os.path.join( srcfd, k )
        dst = os.path.join( dstfd, k )

        print( "cp file: %s" % dst)

        mkfdir(dst)
        shutil.copy2( src, dst )


def combine_with_limitsize( reserve, pending, currentSize, limitSize ):
    if currentSize < limitSize:
        for i in pending:
            s = int(i[1])

            if currentSize + s >= limitSize:
                break

            currentSize += s
            reserve.append(i)

    return (reserve, pending, currentSize)

def partition_by_filter( ctup, filter ):
    reserve = []
    pending = []

    total_size = 0

    for i in ctup:
        p = i[2]
        if filter.expellent(p):
            reserve.append(i)
            total_size += int(i[1])
        else:
            pending.append(i)

    return (reserve, pending, total_size)


def read_csv_file( csvfile ):
    c = ""
    with open(csvfile, 'rb') as fin:
        c = fin.read().decode("utf8")

    splc = c.split("\r\n")

    ctup = []
    for ix in range(0, len(splc)):
        i = splc[ix]
        if len(i) < 2:
            continue

        tup = i.split(',')
        tup.append( ix )
        ctup.append( tup )

    def compute_(a):
        return int(a[1])

    ctup.sort(key=compute_)

    return ctup


if __name__ == "__main__":

    (opts, args) = parseargs()

    filter = createFliter()

    ctup = read_csv_file(SRC_DIR + "/list.csv")
    (reserve, pending, ts) = partition_by_filter( ctup, filter )
    (reserve, pending, cs) = combine_with_limitsize( reserve, pending, ts, LMT_SIZE)

    def compute_(a):
        return int(a[3])
    reserve.sort(key=compute_)

    do_copying( reserve, SRC_DIR, COPY_DIR)
    write_csv( reserve, COPY_DIR )

    print( "base size %.3f MB" % ( ts / 1024 / 1024 ))
    print( "drop %d files" % (len(ctup) - len(reserve)))

    os.system("pause")


