

'''
@2016.02.17 by wvkmind
    created
    
@2016.02.17 by zsz
    add genTargetFileName
    add some variables
'''

import os,os.path
import zipfile
import time

VERSION_FILE = './resources/version'
PUBLISH_FOLDER = './resources.publish'

def genTargetFileName():
    version = open(VERSION_FILE).readline()
    T = time.strftime('[%m%d.%H%M%S]', time.localtime( time.time() ) )
    return "v%s_BF_%s.zip" % ( version, T )

def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        print(arcname)
        zf.write(tar,arcname)
    zf.close()

if __name__ == '__main__':
    zip_dir(PUBLISH_FOLDER, genTargetFileName() )