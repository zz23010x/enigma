

import os
from os.path import *

import re
import gzip
import hashlib
import zlib
import datetime
import pickle

TYPE_ERROR = '''

!! ERROR
  No.%d param (%s) need a %s type,
  But current is %s

'''

PATH_ERROR = '''

!! ERROR
  The path (%s) is not exist.

'''

def checkparam(param, name, type, pos):
    if not isinstance(param, type):
        raise Exception(TYPE_ERROR % ( pos, name, str(type), type(param)))

def read(path, mode='rb'):
    # check precondition
    if not exists(path):
        raise Exception(PATH_ERROR % path )

    with open(path, mode) as f:
        return f.read()

def readfile(path):
    read(path)

def write(path, content, mode="wb+" ):
    # check precondition
    if not isinstance(content, str) and not isinstance(content, bytes):
        raise Exception(TYPE_ERROR % ( 2, "content", "string or bytes",type(content)))

    if isinstance(content, str):
        content = content.encode()

    with open(path, mode) as f:
        f.write(content)

def writdata(path, data):
    write(path, data)

def datamd5(content):
    # check precondition
    if not isinstance(content, str) and not isinstance(content, bytes):
        raise Exception(TYPE_ERROR % ( 1, "content", "string or bytes",type(content)))

    if isinstance(content, str):
        content = content.encode()

    return hashlib.new('md5', content).hexdigest()

def filemd5(filepath):
    # check precondition
    if not exists(filepath):
        raise Exception(PATH_ERROR % filepath )

    with open(filepath, 'rb') as fin:
        content = fin.read()
        result  = datamd5(content)

    return result

def datacrc(content):
    # check precondition
    if not isinstance(content, str) and not isinstance(content, bytes):
        raise Exception(TYPE_ERROR % ( 1, "content", "string or bytes",type(content)))

    if isinstance(content, str):
        content = content.encode()

    return zlib.crc32(content)

def filecrc(filepath):
    # check precondition
    if not exists(filepath):
        raise Exception(PATH_ERROR % filepath )

    with open(filepath, 'rb') as fin:
        content = fin.read()
        result  = datacrc(content)

    return result

def filebuf(filepath):
    # check precondition
    if not exists(filepath):
        raise Exception(PATH_ERROR % filepath )

    size = getsize(filepath)
    barr = bytearray(size)

    with open(filepath, 'rb+') as fin:
        fin.readinto(barr)

    return barr

def aonencrypt(filepath, encryptedfile):
    # check precondition
    if not exists(filepath):
        raise Exception(PATH_ERROR % filepath )

    key  = b"AONESOFT"
    barr = filebuf(filepath)

    kofs = 0;
    sofs = 0;
    KLEN = len(key);
    SIZE = len(barr)
    counter = 0;

    while (sofs < SIZE):
        while (sofs < SIZE and counter < 64):
            barr[sofs] = barr[sofs] ^ key[kofs];
            sofs += 1
            kofs = (kofs + 1) % KLEN;
            counter+=1
        counter = 0;
        sofs += int(SIZE / 10);

    head = bytearray(4)
    head[0] = key[0]^key[1]
    head[1] = key[2]^key[3]
    head[2] = key[4]^key[5]
    head[3] = key[6]^key[7]

    with open(encryptedfile, 'wb') as fout:
        fout.write(head)
        fout.write(barr)

def aonedecrypt(filepath, encryptedfile):
    # check precondition
    if not exists(encryptedfile):
        raise Exception(PATH_ERROR % encryptedfile )

    key  = b"AONESOFT"
    barr = filebuf(encryptedfile)

    head = bytearray(4)
    head[0] = key[0]^key[1]
    head[1] = key[2]^key[3]
    head[2] = key[4]^key[5]
    head[3] = key[6]^key[7]

    if not barr.startswith(head):
        with open(filepath, 'wb') as fout:
            fout.write(barr)
        return


    kofs = 0;
    sofs = 0;
    KLEN = len(key)
    SIZE = len(barr) - 4
    counter = 0;

    while (sofs < SIZE):
        while (sofs < SIZE and counter < 64):
            barr[sofs+4] = barr[sofs+4] ^ key[kofs];
            sofs += 1
            kofs = (kofs + 1) % KLEN;
            counter+=1
        counter = 0;
        sofs += int(SIZE / 10);

    with open(filepath, 'wb') as fout:
        fout.write(barr.partition(head)[2])

def mkdir(dirpath):
    if exists(dirpath):
        return
    os.makedirs(dirpath)

def mkfdir(filepath):
    mkdir(dirname(filepath))

''' simple style
def gzfile(gzpath, filepath):
    # check precondition
    if not exists(filepath):
        raise Exception(PATH_ERROR % filepath )

    mkdir(dirname(gzpath))

    with open(filepath,'rb') as fin:
        with gzip.open(gzpath, 'wb') as fout:
            fout.write(fin.read())

def gzdata(gzpath, content):
    # check precondition
    if not isinstance(content, str) and not isinstance(content, bytes):
        raise Exception(TYPE_ERROR % ( 2, "content", "string or bytes",type(content)))

    if type(content) == 'string':
        content = content.encode()

    mkdir(dirname(gzpath))

    with gzip.open(gzpath, 'wb') as fout:
        fout.write(content)
'''

def gzfile(gzpath, filepath):
    # check precondition
    if not exists(filepath):
        raise Exception(PATH_ERROR % filepath )

    mkdir(dirname(gzpath))

    g = gzip.GzipFile(filename='', mode='wb', fileobj=open(gzpath,'wb'))

    with open(filepath,'rb') as fin:
        g.write(fin.read())
        g.close()

def ungzfile(gzpath, filepath):
    # check precondition
    if not exists(gzpath):
        raise Exception(PATH_ERROR % gzpath )

    mkdir(dirname(filepath))

    g = gzip.GzipFile(filename='', mode='rb', fileobj=open(gzpath,'rb'))

    with open(filepath,'wb') as fout:
        fout.write(g.read())
        g.close()


def gzdata(gzpath, content):
    # check precondition
    if not isinstance(content, str) and not isinstance(content, bytes):
        raise Exception(TYPE_ERROR % ( 2, "content", "string or bytes",type(content)))

    if type(content) == str:
        content = content.encode()

    mkdir(dirname(gzpath))

    g = gzip.GzipFile(filename='', mode='wb', fileobj=open(gzpath,'wb'))
    g.write(content)
    g.close()


def allfolders(dirpath, list=None):
    # check precondition
    if not isinstance(dirpath, str):
        raise Exception(TYPE_ERROR % ( 1, "dirpath", "string",type(dirpath)))
    if not exists(dirpath):
        raise Exception(PATH_ERROR % dirpath )

    if list==None:
        list = []

    list.append(dirpath)

    for d in os.listdir(dirpath):
        full = join(dirpath, d)

        if full.find(".svn") != -1:
            continue

        if isdir(full):
            allfolders(full, list)

    return list

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

class Increment:
    def __init__(self, p):
        self.__filepath = p
        self.__incrdict = {}
        mkfdir(p)
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

