# -*- coding: UTF-8 -*-

import sys,os
import sqlite3
import csv
import time
import pickle
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

    def getField(self, tabname):
        try:
            conn = sqlite3.connect(self.filepath)
            cur = conn.cursor()    
            self.paras = cur.execute("pragma table_info ('%s')" % (tabname)).fetchall()
            conn.close()
        except Exception as e:
            print('\nget tabel paras error', e)
        finally:
            return len(self.paras)

    def execomSql(self, sqlstr):
        try:
            conn = sqlite3.connect(self.filepath)
            cur = conn.cursor()    
            cur.execute(sqlstr)
            conn.commit()
        except Exception as e:
            print(sqlstr, e)
        finally:
            conn.close()

    def execomSqls(self, sqlstr, sqlpara):
        try:
            conn = sqlite3.connect(self.filepath)
            cur = conn.cursor()    
            cur.executemany(sqlstr, sqlpara)
            conn.commit()
        except Exception as e:
            print(sqlstr, e)
        finally:
            conn.close()    

class CsvFile:
    def __init__(self, filepath):
        self.dir = os.path.dirname(filepath);
        self.name = os.path.basename(filepath).split('.')[:-1][0]
        self.path = filepath
        self.updatetime = os.path.getmtime(filepath)

    def read(self):
        result = []
        try:
            with open(self.path, 'r') as file:
                self.content = csv.reader(file)
                for k,v in enumerate(self.content):
                    if k==0:
                        continue
                    result.append(tuple(v))
        except UnicodeDecodeError:
            with open(self.path, 'r', encoding='utf-8') as file:
                self.content = csv.reader(file)
                for k,v in enumerate(self.content):
                    if k==0:
                        continue
                    result.append(tuple(v))
        except Exception as e:
            print(self.path, '\ncsv read failed :', e)
        finally:
            return result

    def record(self):
        try:
            with open():
                pass
        except Exception as e:
            pass

    # def makevalues(self):
    #     result = []
    #     self.read()
    #     try:
    #         for k,v in enumerate(self.content):
    #             if k==0:
    #                 continue
    #             result.append(tuple(v))
    #     except UnicodeDecodeError as e:
    #         print(e)
    #         # self.file = open(self.path, 'r', encoding='utf-8')
    #         # self.makevalues()
    #     return result

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

def work(sqlpath, csvpath):
    sq = SqlFile(sqlpath)
    tabNames = sq.getTabName()
    list = File.ergodic(csvpath)
    pic = Pickle(csvpath)
    sucsNum = 0
    failNum = 0
    maskingword = ['_updaterecord','.py']
    for f in list:
        if '.csv' not in f:
            continue
        cs = CsvFile(f)
        if cs.name in tabNames:
            if cs.name in pic.csvfile_lastrecord:
                if cs.updatetime <= pic.csvfile_lastrecord[cs.name]:
                    continue            
            print("清空表%s" % cs.name)
            sq.execomSql('delete from %s;' % (cs.name))
            print("插入表%s" % cs.name)
            sq.execomSqls('INSERT INTO %s VALUES(%s) ;' % (cs.name,    makemark(sq.getField(cs.name))), cs.read())
            pic.write(cs.name, cs.updatetime)
            sucsNum += 1
        else:
            print("%s数据库不存在该表,先创建!" % cs.name)
    print("修改表个数:%s" %(sucsNum) )

def makemark(num):
    result = ''
    for i in range(0, num):
        result += '?,'
    return result[:-1]

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
    print('Complete...窗口直点x关闭!!!')
    while(1):
        pass
    
# if __name__=="__main__":
#     if len(sys.argv) == 2:
#         sqlurl = sys.argv[1]
#         csvurl = input('拖入csv文件夹\n')
#         work(sqlurl, csvurl)
#         input('Ok...Press any key EXIT!!!')
#     else:
#         print('sqlite数据库直拖入此py执行 本窗口直点x关闭')
#         while(1):
#             pass