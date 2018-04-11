import pylab as pl
import os

def write():
    print "Binary data writing commencing."
    with open(os.getcwd()+"/binstuff", 'wb') as openfile0:
        nostringArray = pl.array( [ 0100 ,  0200 ,  100 ,  200 ], dtype=pl.int64 )
        stringArray   = pl.array( ["0100", "0200", "100", "200"], dtype=pl.int64 )
        print "nostringArray:", nostringArray
        print "stringArray:  ", stringArray

        nostringArray.tofile(openfile0)
        stringArray.tofile(openfile0)

        openfile0.close()
    return 0

def read():
    print "\nBinary data written. Binary reading commencing."
    with open(os.getcwd()+"/binstuff", 'rb') as openfile1:
        nostringArray = pl.fromfile( openfile1, pl.int64, 4 )
        stringArray   = pl.fromfile( openfile1, pl.int64, 4 )

        openfile1.close()
    print "nostringArray:", nostringArray
    print "stringArray:  ", stringArray
    return 0

write()
read()