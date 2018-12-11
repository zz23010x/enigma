
import sys
import configparser
import os
from os.path import *

__env = dict()

def set(k, v):
    __env[k] = v

def get( k ):
    kk = k
    if kk in __env:
        return __env[kk]
    kk = '@' + kk
    if kk in __env:
        return __env[kk]
    
    if k in os.environ:
        return os.environ[k]
    
    return ""

def log():
    for k,v in __env.items():
        print( k, v )

def setup():
    cf = configparser.ConfigParser()
    cf.read(splitext(__file__)[0] + ".ini")
    def __set_all_env( dic ):
        for k,v in dic:
            set( '@'+k, v )
    cff = cf.items("_default")
    __set_all_env( cff )
    if cf.has_section(os.getlogin()):
        cff = cf.items(os.getlogin())
        __set_all_env( cff )
    # manual
    set( '@ndk_bat',     join(get('@android_ndk'), "ndk-build.cmd") )
    set( '@android_bat', join(get('@android_sdk'), "tools", "android.bat") )
    set( '@ant_bat',     join(get('@ant'), "bin", "ant.bat") )
    
    set( 'cwd', sys.path[0] )
