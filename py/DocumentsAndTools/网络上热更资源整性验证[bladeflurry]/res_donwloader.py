
import os
import os.path
import sys
import urllib
import urllib.request
import gzip
from optparse import OptionParser


CWD = sys.path[0] + '\\'
print( CWD )


def receive( url ):
    req = urllib.request.Request( url, headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    })
    oper = urllib.request.urlopen(req)
    data = oper.read()

    return data

def save2file( url, filepath ):
    with open(filepath, "wb") as fp:
        fp.write( receive( url ) )

def getlist( baseurl ):
    gz = receive( baseurl + "list.csv.gz" )
    uz = gzip.decompress( gz )
    uz = uz.decode("utf8")

    lines = uz.splitlines()


    ll = []
    count=0
    
    ll.append( "list.csv.gz" )
    count+=1
    for line in lines:
        file = line.split(',')[2]
        ll.append(file)
        count+=1


    print( count )

    return ll

def ckparams( opts ):

    def ckattr( obj, name ):
        if getattr( obj, name ) == None:
            print( "ERROR : '%s' is None" % name )
            return False
        return True

    if not ckattr( opts, "url" ):
        return False
    if not ckattr( opts, "dir" ):
        return False

    return True

def ctdir( file ):
    d = os.path.dirname(file)
    if not os.path.exists(d):
        os.makedirs(d)


def download_all_files( url, ll, dd, continue_ ):
    try:
        for i in ll:
            f = os.path.join( dd, i )
            u = url + i
            ctdir(f)
            if not continue_ or not os.path.exists(f):
                print( u )
                print( "-->>  " + i )
                save2file( u, f )
    except Exception as e:
        print("\n\n\nERROR:\n\n")
        print(u)
        print(e)

def parseArguments():
    op = OptionParser()
    op.add_option(
        "-u",
        "--url",
        action = "store",
        dest   = "url",
        type   = "string"
        )

    op.add_option(
        "-d",
        "--dir",
        action = "store",
        dest   = "dir",
        type   = "string"
        )
        
    op.add_option(
        "-c", "--continue",
        action = "store_true",
        dest   = "cc",
        default= False
        )

    return op.parse_args()


if __name__ == "__main__":
    (opts, args) = parseArguments()
    if not ckparams(opts):
        os.system("pause")
        exit(1)
    
    url = opts.url
    dir = os.path.join( CWD, opts.dir )
    baseUrl = url[0:url.rfind('/')+1]
    ll = getlist(baseUrl)

    print( url )
    print( dir )
    
    download_all_files( baseUrl, ll, dir, opts.cc )

