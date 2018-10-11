
import sys
sys.path.append( sys.path[0] + "/toolchain" )

import os

import helper
import optparse
import re
import shutil
import time


DEFAULT_RESOURCES_DIRECTORY = "resources"
xxtea_cmd = "toolchain\\bin\\xxtea e SMSP %s %s"

class Modifier:
    def __init__(self, config):
        helper.checkparam(config, "config", dict, 1)

        self.__config = {}

        FUNC_ERROR = '''

        !! ERROR
          Modifier constructor config param error.
          There's no '%s' in <class Modifier>.

          key(%s) - value(%s)

        '''

        # convert string that in config to function
        for k,v in config.items():
            fn = v
            f = getattr(self, fn)

            if f==None or not callable(f):
                raise Exception( FUNC_ERROR % ( fn, k, v ))

            self.__config[k] = f

    def execute(self, src, dst):
        _, ext = os.path.splitext(src)

        if ext not in self.__config:
            self.copy(src, dst)
            return

        f = self.__config[ext]
        f(src, dst)

    def __system(self,cmd):
        os.system(cmd)

    def publish(self, src, dst):

        if isinstance(src, bytes):
            helper.gzdata(dst, src)

        helper.checkparam(src, "src", str, 1)
        helper.gzfile(dst, src)
        print( "    >> GZIP - %s" % dst)

    def ungzip(self, src, dst):
        helper.ungzfile(src, dst)
        print( "    >> UNGZIP - %s" % dst)

    def aonede(self, src, dst):
        helper.aonedecrypt(dst,src)
        print( "    >> DECRYPT - %s" % dst)

    def xxtea(self, src, dst):
        self.__system(xxtea_cmd % ( src, dst ))
        print( "    >> XXTEA - %s" % dst)

    def aonenc(self, src, dst):
        helper.aonencrypt(src,dst)
        print( "    >> AONE ENCRYPT - %s" % dst)

    def copy(self, src, dst):
        shutil.copy2(src, dst)
        print( "    >> COPY - %s" % dst)

class sepinfo:
    def __init__(self, sfp, pfp):
        self.s = sfp
        self.p = pfp

    def visitEncrypt(self, modifier):
        modifier.execute(self.s, self.e)

    def visitPublish(self, modifier):
        modifier.publish(self.e, self.p)

    def visitDecrypt(self, modifier):
        modifier.aonede(self.s, self.s)
        
    def visitUngzip(self, modifier):
        modifier.ungzip(self.p, self.s)

    def __repr__(self):
        return "~ S|%s\n  E|%s\n  P|%s\n  G|%s\n  K|%s\n" % (self.s, self.e, self.p, self.gz, self.key)


# sepg -> src, enc, pub, gz
def getsepg(filepath, sf, pf):
    pub_fp = filepath
    src_fp = filepath.replace(pf, sf, 1)[0:-3]

    sepg = sepinfo(src_fp, pub_fp)
    return sepg


CHANGE_INFO = '''
*
* summary:
*
*   total   : %d
*   changed : %d
*
'''
def logChangeInfo(total, change):
    print(CHANGE_INFO % (total, change))

def parseargs():
    parser = optparse.OptionParser()
    parser.add_option(
        "-d",
        action  = "store",
        dest    = "directory",
        default = DEFAULT_RESOURCES_DIRECTORY,
        help    = "Set the target resource directory."
        )
    parser.add_option(
        "--decrypt",
        action  = "store_true",
        dest    = "dec",
        default = False,
        help    = "dec."
        )

    return parser.parse_args()

def domainwork(opts, args):
    # generate three folder : source, encrypt, publish
    pubfd = opts.directory
    srcfd = pubfd + ".src"

    # path excluder
    pe = helper.PathExcluder()

    # ergodic all files
    orglist = helper.allfiles( pubfd )
    publist = pe.filter(orglist)[0]

    # generate seplist
    seplist = []
    for i in publist:
        sepg = getsepg(i,srcfd,pubfd)
        seplist.append(sepg)

    # generate modifier
    mfconfig = {
        ".gz" : "ungzip",
    }
    modifier = Modifier(mfconfig)

    # icrement generate encrypt and publish

    for i in seplist:
        helper.mkfdir(i.p)
        i.visitUngzip(modifier)
        if opts.dec:
            i.visitDecrypt(modifier)
        print("")

if __name__ == "__main__":

    (opts, args) = parseargs()

    domainwork(opts, args)

    os.system("pause")


