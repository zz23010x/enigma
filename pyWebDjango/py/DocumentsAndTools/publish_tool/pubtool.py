
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
bpgen_cmd = "toolchain\\bin\\bpg\\bpgenc -o %s %s"

INCREMENT_FORMAT = "toolchain\\temp\\%s.incr"
ENCRYPT_SUFFIX = ".encrypt"
PUBLISH_SUFFIX = ".publish"

class Modifier:
    def __init__(self, config):

        self.__config = []

        FUNC_ERROR = '''

        !! ERROR
          Modifier constructor config param error.
          There's no '%s' in <class Modifier>.

          key(%s) - value(%s)

        '''

        # convert string that in config to function
        for r, v in config:
            f = getattr(self, v)

            if f==None or not callable(f):
                raise Exception( FUNC_ERROR % ( v, k, v ))

            rex = re.compile( r )

            self.__config.append( ( rex, f ) )
            #self.__config[k] = f

    def execute(self, src, dst):
        for r, f in self.__config:
            if r.search( src ) != None:
                f(src,dst)
                return

        self.copy(src, dst)
        '''
        _, ext = os.path.splitext(src)

        if ext not in self.__config:
            self.copy(src, dst)
            return

        f = self.__config[ext]
        f(src, dst)
        '''

    def __system(self,cmd):
        os.system(cmd)

    def publish(self, src, dst):

        print( "    >> GZIP - %s" % dst)
        if isinstance(src, bytes):
            helper.gzdata(dst, src)

        helper.checkparam(src, "src", str, 1)
        helper.gzfile(dst, src)

    def xxtea(self, src, dst):
        print( "    >> XXTEA - %s" % dst)
        self.__system(xxtea_cmd % ( src, dst ))

    def bpgen(self, src, dst):
        print( "    >> BPG - %s" % dst)
        self.__system(bpgen_cmd % ( dst, src ))

    def aonenc(self, src, dst):
        print( "    >> AONE ENCRYPT - %s" % dst)
        helper.aonencrypt(src,dst)

    def copy(self, src, dst):
        print( "    >> COPY - %s" % dst)
        shutil.copy2(src, dst)

class sepinfo:
    def __init__(self, sfp, efp, pfp, gz):
        self.s = sfp
        self.e = efp
        self.p = pfp
        self.gz = gz
        self.key = gz.replace(".gz", "")

    def visitEncrypt(self, modifier):
        modifier.execute(self.s, self.e)

    def visitPublish(self, modifier):
        modifier.publish(self.e, self.p)

    def __repr__(self):
        return "~ S|%s\n  E|%s\n  P|%s\n  G|%s\n  K|%s\n" % (self.s, self.e, self.p, self.gz, self.key)

    def listinfo(self):
        uniq = "%s|%010d" % (helper.filemd5(self.s), helper.datacrc(self.key))
        size = os.path.getsize(self.p)
        name = self.gz
        return "%s,%d,%s\r\n" % (uniq,size,name)

    def randinfo(self):
        rnif = str(time.time())
        bsnm = os.path.basename(self.s)
        uniq = "%s|%010d" % (helper.datamd5(rnif), helper.datacrc(bsnm))
        size = os.path.getsize(self.p)
        name = self.gz
        return "%s,%d,%s\r\n" % (uniq,size,name)


# sepg -> src, enc, pub, gz
def getsepg(filepath, sf, ef, pf):
    src_fp = filepath
    enc_fp = filepath.replace(sf, ef, 1)
    pub_fp = filepath.replace(sf, pf, 1) + ".gz"
    gz = pub_fp.replace(pf + '\\', "", 1)
    gz = gz.replace('\\', '/')

    sepg = sepinfo(src_fp, enc_fp, pub_fp, gz)
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

    return parser.parse_args()

def domainwork(opts, args):
    # generate three folder : source, encrypt, publish
    srcfd = opts.directory
    encfd = srcfd + ENCRYPT_SUFFIX
    pubfd = srcfd + PUBLISH_SUFFIX
    incrtag = srcfd

    # path excluder
    pe = helper.PathExcluder()
    pe.addregex(r"list\.csv")
    pe.addregex(r"version$")
    pe.addregex(r"straw$")
    pe.addregex(r"\.tags[\w_]*$")
    pe.addregex(r"aonesdk\.json$")
    pe.addregex(r"uuSdkConfig\.json$")
    pe.addregex(r"uuSdkInfo\.json$")

    # ergodic all files
    orglist = helper.allfiles( srcfd )
    srclist = pe.filter(orglist)[0]

    # generate seplist
    seplist = []
    for i in srclist:
        sepg = getsepg(i,srcfd,encfd,pubfd)
        seplist.append(sepg)

    # generate modifier
    mfconfig = [
        (r".*\.lua$", "xxtea"),
        (r"\\Icon.*\.png$" , "copy"),
        (r"\\sdk\\" , "copy"),
        (r".*\.png$" , "aonenc"),
        (r".*\.jpg$" , "aonenc"),
    ]
    modifier = Modifier(mfconfig)


    # icrement generate encrypt and publish
    incr = helper.Increment(INCREMENT_FORMAT % incrtag)

    chang_count = 0
    for i in seplist:

        tm = os.path.getmtime(i.s)

        if  os.path.exists(i.e) \
        and os.path.exists(i.p) \
        and not incr.newer(i.key, tm):
            continue

        helper.mkfdir(i.e)
        helper.mkfdir(i.p)
        incr.update(i.key, tm)
        chang_count += 1

        print(i.s)
        i.visitEncrypt(modifier)
        i.visitPublish(modifier)
        print("")

    incr.save()

    # print change log
    logChangeInfo(len(seplist), chang_count)

    # version and straw
    version = getsepg(os.path.join(srcfd, "version"), srcfd, encfd, pubfd)
    print(version.s)
    version.visitEncrypt(modifier)
    version.visitPublish(modifier)

    # generate list.csv
    lst = getsepg(os.path.join(srcfd, "list.csv"), srcfd, encfd, pubfd)
    print(lst.s)

    csv = ""
    for i in seplist:
        csv += i.listinfo()
    
    # 保证 enc和pub的 list.csv => version 的md5 不一致
    ecsv = csv + version.randinfo()
    pcsv = csv + version.randinfo()

    helper.write(lst.s, pcsv)
    lst.visitEncrypt(modifier)
    lst.visitPublish(modifier)

    helper.write(lst.s, ecsv)
    lst.visitEncrypt(modifier)


if __name__ == "__main__":

    (opts, args) = parseargs()

    domainwork(opts, args)

    os.system("pause")


