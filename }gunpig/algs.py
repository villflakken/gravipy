import pylab as pl


n = 123123123123123# steps
stepsize = pl.array(pl.arange(1,10))
for size in stepsize:
    sfs = pl.arange(0, 64, size)
    if sfs[-1] == 63:
        print
        print "stepsize : ", size, " || len(sfs) : ", len(sfs)
        print sfs
        print
        pass
    else:
        pass
