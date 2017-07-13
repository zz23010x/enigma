# -*- coding: UTF-8 -*-

import sys,os
import csv
from optparse import OptionParser

stepdic = {};
strlist = [('id','type','step')];

class CsvFile:
    @staticmethod
    def write(filepath, content):
        try:
            with open(filepath, 'w') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerows(content)
        except Exception as e:
            print(content, '\ncsv write failed :', e)

class LuaFile:
    def __init__(self, filepath):
        self.filename = os.path.basename(filepath).split('.')[:-1][0]
        self.list = self.filename.split('_')
        self.id = self.list[1]
        self.type = len(self.list)-1
        self.step =['0']
        step = self.list[2:]
        if len(step) != 0:
            step = ["_".join(step)]
            if self.id in stepdic:
                self.step = stepdic[self.id].step + step
            else:
                self.step = step
        stepdic[self.id] = self
            
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

def work(fileurl):
    list = File.ergodic(fileurl)
    for f in list:
        if '.lua' in f:
            lf = LuaFile(f)
            print(lf.filename)
    for key, val in stepdic.items():
        strlist.append((val.id, val.type, "|".join(val.step)))
    CsvFile.write(os.path.join(os.path.dirname(__file__), "client_story_id.csv"), strlist)

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-d", "--directory",
                      action="store",
                      dest="dir",
                      default=os.path.join(os.path.dirname(__file__), "story"),
                      help="set lua directory"
                      )

    (opts, args) = parser.parse_args()
    directory = os.path.join(os.path.dirname(__file__), opts.dir)
    work(directory)