

import os
from os.path import *

import re
import datetime
import optparse
import pickle
import shutil

def mkdir(dirpath):
    if exists(dirpath):
        return
    os.makedirs(dirpath)

def mkfdir(filepath):
    mkdir(dirname(filepath))

class Increment:
    def __init__(self, p):
        self.__filepath = p
        self.__incrdict = {}
        self.load()

    def load(self):
        p = self.__filepath
        if not os.path.exists(p):
            return

        with open(p,"rb") as fin:
            self.__incrdict = pickle.load(fin)

    def save(self):
        dt = pickle.dumps(self.__incrdict )
        with open(self.__filepath, "wb") as fout:
            fout.write(dt)

    def newer(self, key, val):
        if not key in self.__incrdict:
            return True
        return self.__incrdict[key] != val

    def update(self, key, val):
        self.__incrdict[key] = val

class PathExcluder():
    def __init__(self):
        self.__regexes = []
        self.__bywhich = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

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

    def filter(self, pathlist):

        errordic = {}

        # check precondition
        if not isinstance(pathlist, list):
            raise Exception(TYPE_ERROR % ( 1, "pathlist", "list", type(pathlist)))
        if not isinstance(errordic, dict):
            raise Exception(TYPE_ERROR % ( 2, "errordic", "dict", type(errordic)))

        result = []

        for p in pathlist:

            if not exists(p):
                errp = p
                errs = "FileNotExist"
                errordic[p] = errs
                continue

            if self.expellent(p):
                errp = p
                errs = self.__bywhich
                errordic[p] = errs
                continue

            result.append(p)

        return result, errordic

def allfiles(dirpath, list=None):
    # check precondition
    if not isinstance(dirpath, str):
        raise Exception(TYPE_ERROR % ( 1, "dirpath", "string",type(dirpath)))
    if not exists(dirpath):
        raise Exception(PATH_ERROR % dirpath )

    if  list==None:
        list = []

    for d in os.listdir(dirpath):
        full = join(dirpath, d)

        if full.find(".svn") != -1:
            continue

        if isdir(full):
            allfiles(full, list)
        else:
            list.append(full)

    return list

CHANGE_INFO = '''
*
* summary:
*
*   total   : %d
*   changed : %d
*
'''
def logChangeInfo(total, change):
    print(CHANGE_INFO % (total, change))

def domainwork(opts, args):
    # generate three folder : source, encrypt, publish
    srcfd = opts.src
    dstfd = opts.dst

    # ergodic all files
    orglist = allfiles( srcfd )
    srclist = None
    with PathExcluder() as pe:
        pe.addregex(r"\.tags[\w_]*$")
        srclist,_ = pe.filter(orglist)

    # icrement generate encrypt and publish
    incr = Increment(opts.incr + ".incr")

    chang_count = 0
    add_count = 0
    for i in srclist:

        sfile = i
        dfile = sfile.replace(srcfd, dstfd)
        dexist = os.path.exists(dfile)
        
        if not dexist:
            add_count += 1
        
        
        tm = os.path.getmtime(sfile)
        
        if  dexist \
        and not incr.newer(sfile, tm):
            continue

        mkfdir(dfile)
        incr.update(sfile, tm)
        chang_count += 1
        
        print(dfile)
        shutil.copy2(sfile, dfile)

    incr.save()
    
    # print change log
    logChangeInfo(len(srclist), chang_count)
    
    # svn operate
    if opts.svn:
        if add_count>0:
            os.system("TortoiseProc /command:add    /path:%s /closeonend:2" % dstfd )
        os.system("TortoiseProc /command:commit /path:%s /closeonend:2" % dstfd )


def parseargs():
    parser = optparse.OptionParser()
    parser.add_option(
        "-s",
        action  = "store",
        dest    = "src",
        default = "",
        help    = "Set the target resource directory."
        )
    parser.add_option(
        "-d",
        action  = "store",
        dest    = "dst",
        default = "",
        help    = "Set the target resource directory."
        )
    parser.add_option(
        "-f",
        action  = "store",
        dest    = "incr",
        default = "",
        help    = "Set the increment file."
        )
    parser.add_option(
        "--svn",
        action  = "store_true",
        dest    = "svn",
        default = False,
        help    = "commit to svn."
        )

    return parser.parse_args()

if __name__ == "__main__":

    (opts, args) = parseargs()

    if opts.src == "" or opts.dst == "":
        print(" ERROR, param error!!")
    else:
        domainwork(opts, args)

    os.system("pause")

















