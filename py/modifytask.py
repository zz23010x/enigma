# -*- coding: UTF-8 -*-

import re
import os, sys
from multiprocessing import Pool

class File:
    @staticmethod
    def read( filepath ):
        try:
            fp = open( filepath, 'r' , encoding='utf-8')
            content = fp.read()
            fp.close()
        except Exception as e:
            print(e)
            return Null
        finally:
            return content

    @staticmethod
    def write( filepath, content ):
        try:
            newpath = os.path.join(os.path.dirname(os.path.dirname(filepath)) , 'newfile' , os.path.basename(filepath))
            fp = open( newpath, 'w' , encoding='utf-8')
            fp.write( content )
            fp.close()
        except:
            pass
        finally:
            pass
    
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
            
            if not os.path.exists(os.path.join(os.path.dirname(dpath),'newfile')):
            	os.mkdir(os.path.join(os.path.dirname(dpath),'newfile'))
            for root,dirs,files in os.walk( dpath ):
                for file in files:
                    fpath = os.path.join(root,file)
                    flist.append( fpath )
        return flist

    @staticmethod
    def update( filepath, content ):
        try:
            newpath = os.path.join(os.path.dirname(os.path.dirname(filepath)) , 'newfile' , os.path.basename(filepath))
            fp = open( newpath, 'a' , encoding='utf-8')
            fp.write( content )
            fp.close()
        except Exception as e:
            print(e)
        finally:
            pass

    @staticmethod
    def modify( filepath, keyword, content ):
        try:
            fp = open( filepath, 'r' , encoding='utf-8')
            for line in fp.readlines():
                if line.find(keyword) != -1:
                    print(filepath, '修改前', line)
                    value = line.split(',')[0].split('=')[-1].strip()
                    realvalue = str(int(float(value)*content))
                    line = line.replace(value, realvalue)
                    print(filepath, '修改后', line)
                File.update(filepath, line)
        except Exception as e:
            print(e)
        finally:
           	fp.close()

def work(filepath):
    try:
        pk = re.compile(r".*\['exp'].*" )
        old_c = File.read(filepath)
        old_s = pk.search(old_c)
        style = old_s.group().split('=')[0]
        old_v = old_s.group().split(',')[0].split('=')[-1].strip()
        new_v = str(int(float(old_v)*1.5))
        new_s = style + '= ' + new_v + ','
        new_c = pk.sub(new_s, old_c)
        File.write(filepath, new_c)
    except Exception as e:
        print(filepath, e)

if __name__=="__main__":
    list = File.ergodic("task")
    for f in list:
        work(f)
	# p = Pool(50)
	# for f in list:
	# 	p.apply_async(work,(f, "['exp'] =", 1.5,))
	# p.close()
	# p.join()