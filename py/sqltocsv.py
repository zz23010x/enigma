# -*- coding: UTF-8 -*-

import sys,os
import hashlib
import sqlite3
import csv
import time
import pickle
import shutil
from optparse import OptionParser

class SqlFile:
    def __init__(self, filepath):
        self.filepath = filepath

    def getTabName(self):
        try:
            tabNames = []
            conn = sqlite3.connect(self.filepath)
            cur = conn.cursor()    
            tabs = cur.execute("select name from sqlite_master where type = 'table' order by name").fetchall()
            for tab in tabs:
                if tab[0] == '':
                    continue
                tabNames.append(tab[0])
            conn.close()
        except Exception as e:
            print('\nget tabel name error', e)
        finally:
            return tabNames    

    def read(self, tabname):
        try:
            localpara = []
            conn = sqlite3.connect(self.filepath)
            cur = conn.cursor()    
            paras = cur.execute("pragma table_info ('%s')" % (tabname)).fetchall()
            for para in paras:
                localpara.append(para[1])
            values = cur.execute("select * from %s" % (tabname)).fetchall()
            result = [tuple(localpara)] + values
            return result
        except Exception as e:
            print(tabname, '\nsqlite read failed', e)

class CsvFile:
    @staticmethod
    def write(filepath, content):
        try:
            with open(filepath, 'w') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerows(content)
        except Exception as e:
            print(content, '\ncsv write failed :', e)
            
class File:
    @staticmethod
    def ergodic( dirpaths ):
        if isinstance( dirpaths, str ):
            dirpaths = [ dirpaths ]

        flist = []
        for dirpath in dirpaths:
            dpath = os.path.join(os.path.dirname(__file__), dirpath)
            if not os.path.isdir( dpath ):
                print('Path [%s] is not a directory!' % dpath)
                continue
       
            for root,dirs,files in os.walk( dpath ):
                for file in files:
                    fpath = os.path.join(root,file)
                    flist.append( fpath )
        return flist

    @staticmethod
    def md5sum(filepath):             
        fd = open(filepath,"rb")  
        fcont = fd.read()
        fd.close()           
        fmd5 = hashlib.md5(fcont)  
        return fmd5

    @staticmethod
    def createdir(Slogan):
        dirname = input('%s\n' % (Slogan))
        newpath = os.path.join(os.path.dirname(__file__),dirname)
        if not os.path.exists(newpath):
            os.mkdir(newpath)
        return newpath

class Pickle:
    csvfile_lastrecord = {}
    def __init__(self, picpath):
        self.path = os.path.join(picpath, '_modifyRecord')
        if (os.path.exists(self.path)):
            with open(self.path,'rb') as f:  
                self.csvfile_lastrecord = pickle.load(f)

    def write(self, key, value):
        with open(self.path,'wb') as f:  
            self.csvfile_lastrecord[key] = value
            pickle.dump(self.csvfile_lastrecord, f)  

def work(filepath, fileurl):
    sqlpath = SqlFile(filepath)
    if not os.path.exists(fileurl):
        os.mkdir(fileurl)
    else:
        shutil.rmtree(fileurl)
        os.mkdir(fileurl)
    pic = Pickle(fileurl)
    for csvfile in sqlpath.getTabName():
        CsvFile.write(os.path.join(fileurl, csvfile + '.csv'), sqlpath.read(csvfile))
    list = File.ergodic(fileurl)
    for f in list:
        if '.csv' in f:
            pic.write(os.path.basename(f).split('.')[:-1][0], os.path.getmtime(f));

def contrast(filepath1, filepath2):
    sql1dict = {}
    sql2dict = {}
    sql1path = SqlFile(filepath1)
    sql2path = SqlFile(filepath2)
    tab1names = sql1path.getTabName()
    tab2names = sql2path.getTabName()
    differenceResult = []
    differenceTabs = ('表差异',) + tuple(set(tab1names) ^ set(tab2names))
    differenceValues = []

    for csv1file in tab1names:
        sql1dict[csv1file] = sql1path.read(csv1file)
    for csv2file in tab2names:
        sql2dict[csv2file] = sql2path.read(csv2file)
    for key,val in sql1dict.items():
        if key in (sql2dict):
            locallist = list(set(val) ^ set(sql2dict[key]))
            if locallist:
                locallist.sort()
                tupstr = find(locallist)
                differenceValues.extend([('%s' % (key),)])
                differenceValues.extend(tupstr)
                differenceValues.extend([(val[0])])
                differenceValues.extend(locallist) 

    differenceResult.extend([differenceTabs])
    differenceResult.extend(differenceValues)
    CsvFile.write(os.path.join(os.path.dirname(__file__), 'difference.csv'), differenceResult)
    csv1path = File.createdir("%s1、数据库目录名" % (os.path.basename(filepath1)))
    csv2path = File.createdir("%s2、数据库目录名" % (os.path.basename(filepath2)))
    for csv1file in sql1path.getTabName():
        CsvFile.write(os.path.join(csv1path, csv1file + '.csv'), sql1path.read(csv1file))
    for csv2file in sql2path.getTabName():
        CsvFile.write(os.path.join(csv2path, csv2file + '.csv'), sql2path.read(csv2file))

def find(xlist):
    result = []
    if len(xlist) == 1:
        return [('行数变化',)]
    if len(xlist[0]) != len(xlist[1]):
        return [('列数变化',)]
    for num, xval in enumerate(xlist):
        if num < len(xlist)-1:
            if xval[0] == xlist[num+1][0]:
                item = "id[" + str(xval[0]) + "]{"
                for n, x in enumerate(xval):
                    if x != xlist[num+1][n]:
                         item += randomCode(n) + "列%s -> %s," % (x, xlist[num+1][n])
                item = item[:-1]
                item += "}"
                localtuple = (item,)
                result.append(localtuple)
    return result

def randomCode(count):
    result = ''
    ch = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]
    if count / 27 < 1:
        result = ch[count%26]
    else:
        result = ch[0] + ch[count%26]
    return result

def random(code):
    if code == "" or code[0] != "a":
        return code
    ch = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]
    result = ch.index(code[-1])
    if len(code) == 2:
        result += 26
    return result

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-f", "--sqlfile",
                      action="store",
                      dest="file",
                      default=os.path.join(os.path.dirname(__file__), "trunk\VALUE_DB.db"),
                      help="set sqlite directory"
                      )
    parser.add_option("-d", "--directory",
                      action="store",
                      dest="dir",
                      default=os.path.join(os.path.dirname(__file__), "trunk_csv"),
                      help="set csv directory"
                      )

    (opts, args) = parser.parse_args()
    fileurl = opts.file
    directory = os.path.join(os.path.dirname(__file__), opts.dir)
    work(fileurl, directory)

# if __name__=="__main__":
#     if len(sys.argv)==2:
#         sqlurl = sys.argv[1]
#         work(sqlurl)
#     elif len(sys.argv)==3:
#         sqlurl = sys.argv[1]
#         sqlurl2 = sys.argv[2]
#         contrast(sqlurl,sqlurl2)
#     else:
#         sqlurl = input('拖入.sql数据库\n')
#         work(sqlurl)