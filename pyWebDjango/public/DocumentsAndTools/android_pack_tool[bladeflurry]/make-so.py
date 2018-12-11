
import sys
import os, os.path
import shutil

sys.path.append( sys.path[0] + "/.toolchain")
import env

from optparse import OptionParser

def copytree(src, dst, symlinks=False, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    try:
        os.makedirs(dst)
    except (IOError, os.error) as why:
        pass
        
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)





def compile( dbgmode, nthread ):
    opt_ndkpath = env.get("ndk_bat")
    opt_jnipath = os.path.join( env.get("ttk"), "03_client\\project\\proj.android\\jni" )
    opt_nthread = nthread;

    if dbgmode:
        opt_debug = "NDK_DEBUG=1"
    else:
        opt_debug = ""

    cmd = "{ndk} {debug} -j{nthread} -C {jni}".format(
        ndk     = opt_ndkpath,
        debug   = opt_debug,
        nthread = opt_nthread,
        jni     = opt_jnipath
        )

    return os.system(cmd) == 0

def cpbins( ):
    src = os.path.join( env.get("ttk"), "03_client\\project\\proj.android\\libs\\armeabi" )
    dst = os.path.join( os.getcwd()   , ".libs\\armeabi" )

    print( "\n" * 2 )
    print( "copy from " + src );
    print( "       to " + dst );
    
    copytree( src, dst )
    
    

    
    return True


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--debug",
        action  = "store_true",
        dest    = "debug",
        default = False,
        help    = "set NDK_DEBUG=1."
        ) 
    parser.add_option("-t", "--thread",
        action  = "store",
        dest    = "nthread",
        type    = "int",
        default = "4",
        help    = "compile thread number."
        )

    (opts, args) = parser.parse_args()
    
    env.setup()
    env.log()
    
    success = compile( opts.debug, opts.nthread )
    if not success:
        print( "\n" )
        print( " ndk-build error!!")
        quit()
    else:
        print( "\n" )
        print( " ndk-build success!!")

    success = cpbins( )
    if not success:
        print( "\n" )
        print( " copy files error!!")
        quit()
    else:
        print( "\n" )
        print( " copy files success!!")
