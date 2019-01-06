

import re
import sys, os


class File:
    @staticmethod
    def read( filepath ):
        try:
            fp = open( filepath, 'rb' )
            content = fp.read()
            fp.close()
        except:
            return Null
        finally:
            return content
            
    @staticmethod
    def write( filepath, content ):
        try:
            fp = open( filepath, 'wb+' )
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
            dpath = os.path.realpath( dirpath )
            if not os.path.isdir( dpath ):
                print 'Path [%s] is not a directory!' % dpath
                continue
            
            for root,dirs,files in os.walk( dpath ):
                for file in files:
                    fpath = os.path.join(root,file)
                    flist.append( fpath )
        return flist
    


list = File.ergodic("script")

p = re.compile(r"function\s*(\w+)\s*\((.*)\)" )
pid = re.compile(r'return\s*"([0-9]+)"')
pp = re.compile(r"script")

for f in list:
    old_c = File.read( f )
    cls = "task_" + pid.search( old_c).group(1)
    new_s = "function %s:\\1(\\2)" % cls
    new_c = p.sub( new_s, old_c )
    
    new_f = pp.sub( "script_new", f)
    
    File.write( new_f, cls + " = {}\n" + new_c )


