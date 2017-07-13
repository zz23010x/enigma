
import sys
import os,os.path
import re
import string
import gzip
import shutil
import md5
from optparse import OptionParser
from xml.etree import ElementTree

luac_cmd_android = "publish-tools\\luajit -b %s %s"
luac_cmd = "publish-tools\\luac -o %s %s"
encrypt_cmd = "publish-tools\\encrypt"

platform = "ios"

class File:
    @staticmethod
    def md5( filepath ):
        content = File.read(filepath)
        mins = md5.new()
        mins.update( content )
        text = mins.hexdigest()        
        return str.upper( text )
        
    @staticmethod
    def md5ext( filepath, ext ):
        content = File.read(filepath) + ext
        mins = md5.new()
        mins.update( content )
        text = mins.hexdigest()        
        return str.upper( text )

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
    def write( filepath, content, mode="wb+" ):
        try:
            fp = open( filepath, mode )
            fp.write( content )
            fp.close()
        except:
            pass
        finally:
            pass

    @staticmethod
    def writegzip( src, dst, path = False ):
        dstdir = os.path.dirname( dst )
        if not os.path.exists( dstdir ):
            os.makedirs( dstdir )

        g = gzip.GzipFile(filename='', mode='wb', compresslevel=9, fileobj=open(dst,'wb'))
        if path :
            g.write( File.read(src) )
        else :
            g.write( src )
        g.close()

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

class Filter:
    def __init__( self ):
        self.irl = [] # include regex list
        self.erl = [] # exclude regex list

    def cleanup():
        self.irl = []
        self.erl = []

    def addir( self, regex_str ):
        r = re.compile( regex_str, re.I )
        self.irl.append( r )
        return self

    def adder( self, regex_str ):
        r = re.compile( regex_str, re.I )
        self.erl.append( r )
        return self

    def _isinc( self, s ):
        for r in self.irl:
            if r.search( s ) > 0:
                return True
        return False

    def _isexc( self, s ):
        for r in self.erl:
            if r.search( s ) > 0:
                return True
        return False

    def check( self, fpath ):
        if self._isexc( fpath ):
            return False
        if self._isinc( fpath ):
            return True
        return True

    def filter( self, slist ):
        if isinstance( slist, str ):
            slist = [ slist ]

        rlist = []
        for s in slist:
            if self.check( s ):
                rlist.append( s )
        return rlist


class info:
    def __init__(self, src):
        self.src = src
        self.enc = src.replace("\\Resources\\", "\\ResourcesEncrypt\\")
        self.gzp = src.replace("\\Resources\\", "\\ResourcesEncryptPublish\\") + ".gz"
        self.key = self.gzp.replace( os.path.join(os.getcwd(), "ResourcesEncryptPublish") + '\\', "" )
        self.key = self.key.replace("\\", '/')
        _, self.ext = os.path.splitext(src)

        if src != "version":
            self.src_md5 = File.md5( src )
        else:
            self.src_md5 = File.md5ext( src, datetime.now().strftime("%y%m%d%H%M") )
        

    def encrypt(self):
        self.enc_md5 = ''

        src = self.src
        enc = self.enc

        dstdir = os.path.dirname( enc )
        if not os.path.exists( dstdir ):
            os.makedirs( dstdir )

        shutil.copy2( src, enc )

        if self.ext == '.lua':
            os.system(luac_cmd % ( enc, enc ))
        if len(self.ext) > 1 and self.ext!=".mp3":
            os.system(encrypt_cmd + " " + enc)

        self.enc_md5 = File.md5( enc )

    def compress(self, use_src):
        src = self.src
        gzp = self.gzp
        enc = self.enc

        dstdir = os.path.dirname( gzp )
        if not os.path.exists( dstdir ):
            os.makedirs( dstdir )

        if use_src:
            File.writegzip( src, gzp, True )
        else:
            File.writegzip( enc, gzp, True )
            
        self.gzp_size = os.path.getsize(gzp)




if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--platform",
                      action="store",
                      dest="platform",
                      default="ios",
                      help="set platform"
                      )
    parser.add_option(
        "-d", "--directory",
        action="store",
        dest="dir",
        default="Resources",
        help="set the dest resource dir"
        )

    (opts, args) = parser.parse_args()
    
    platform = opts.platform
    directory = opts.dir
    
    
    orglist = File.ergodic( directory )

    srclist = Filter().adder(r".*\.svn.*").adder(r".*msg\.dat.*").adder(r"list\.csv").adder(r"\\version$").adder(r"\\straw$").filter( orglist )

    ttl = []
    for i in range( 0, len(srclist) ):
        ttl.append( info(srclist[i]) )
    ttl.append( info( os.path.join( os.getcwd(), directory, "version" ) ) )

    csvcontent = "";
    use_src_gzip = False
    for i in ttl:
        print i.key
        i.encrypt()
        i.compress(use_src_gzip)

        if use_src_gzip:
            csvcontent += "%s,%d,%s\r\n" % (i.src_md5, i.gzp_size, i.key )
        else:
            csvcontent += "%s,%d,%s\r\n" % (i.enc_md5, i.gzp_size, i.key )

    shutil.copy2( os.path.join( os.getcwd(), "Resources", "straw"), os.path.join( os.getcwd(), "ResourcesEncrypt", "straw") )

    csvfile = os.path.join( os.getcwd(), "ResourcesEncrypt", "list.csv")
    csvgzip = os.path.join( os.getcwd(), "ResourcesEncryptPublish", "list.csv.gz")
    File.write( csvfile, csvcontent, "wb" )
    File.writegzip( csvcontent, csvgzip, False )

    print "totoal : %d files" % len(ttl)
    os.system("pause")

