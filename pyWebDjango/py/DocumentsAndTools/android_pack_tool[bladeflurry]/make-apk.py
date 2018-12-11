
import sys
sys.path.append( sys.path[0] + "/.toolchain")

import os
from os.path import *

import shutil
import datetime
from datetime import *
from optparse import OptionParser

import env

default_version = "102"

def ps():
    #os.system("pause")
    pass

def sysrun( cmd ):
    return os.system( cmd )

def cpfile( src, dst ):
    return sysrun( "copy /b /y %s %s" % ( src, dst ) )

def cpdir( src, dst ):
    print( src, dst )
    return sysrun("xcopy /E /Y %s %s\\" % ( src, dst ))

def rmdir( dst ):
    return sysrun("rd /s /q %s" % dst )

def packOne(opts, path):
    project_path = os.path.abspath( path )
    project_name = os.path.basename( path )
    build_xml = os.path.join( project_path, "build.xml" )

    if not opts.nocpres:
        # copy resources
        resdir = os.path.join( os.getcwd(), "_v" + opts.version + "." + project_name )
        if not os.path.exists( resdir ):
            resdir = os.path.join( os.getcwd(), "_v" + opts.version )
        assets = os.path.join( project_path, "assets" )
        assext = os.path.join( project_path, "assets_ext" )
        rmdir( assets )
        cpdir( resdir, assets )
        cpdir( assext, assets )
    
    # copy libraries
    srclib = os.path.join( os.getcwd(), ".libs" )
    dstlib = os.path.join( project_path, "libs" )
    cpdir( srclib, dstlib )
    ps()
    # android update command
    bat = env.get("android_bat")
    tag = env.get("android_tag")
    cmd = "%s update project --target %s --path %s --name %s" \
     % ( bat, tag, project_path, project_name )
    sysrun(cmd)
    print( cmd )
    ps()

    # apache ant package command
    ant_bat = env.get("ant_bat")
    ant_cln = "clean"
    ant_cfg = "release"
    ant_cmd = "%s %s %s -f %s" % ( ant_bat, ant_cln, ant_cfg, build_xml )
    sysrun(ant_cmd)
    
    # copy apk
    bname = "C#{channel}_S#{server}_V#{version}_T#{time}_P#{purpose}".format(
        channel=project_name,
        server=opts.server,
        version=opts.version,
        time=datetime.now().strftime("%y%m%d%H%M"),
        purpose=opts.purpose,
        )
    
    oldname = os.path.join( path, "bin", project_name + "-" + ant_cfg + ".apk" )
    newname = os.path.join( os.getcwd(), ".output", bname + '.apk' )
    cpfile( oldname, newname )
    
    # copy apk
    oldname = join( path, "bin", "AndroidManifest.xml" )
    newname = join( os.getcwd(), ".output", bname + '.xml' )
    cpfile( oldname, newname )
    
    
def packAll(opts, args):
    for idx in range( 0, len(args) ):
        packOne(opts, args[idx])

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-v", "--version",
        action="store",
        dest="version",
        type="string",
        default=default_version,
        help="set target version."
    )
    parser.add_option("-d", "--debug",
        action="store_true",
        dest="debug",
        default=False,
        help="set NDK_DEBUG=1."
    )
    parser.add_option("-n", "--no-copy-res",
        action="store_true",
        dest="nocpres",
        default=False,
        help="do not copy resource."
    )
    parser.add_option(
        "-a",
        "--additional",
        action="store",
        dest="addi",
        default="",
        help="set additional infomation."
    )
    parser.add_option(
        "-c",
        "--commit",
        action="store_const",
        dest="purpose",
        const="commit",
        default="test",
        help="set the using purpose of final package."
        )
    parser.add_option(
        "-s",
        "--server",
        action="store",
        type="string",
        default="test",
        help="set the using server's alias."
        )

    (opts, args) = parser.parse_args()

    env.setup()
    env.log()
    
    packAll( opts, args )

