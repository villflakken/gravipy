import subprocess as sp
import pylab as pl
tmp = sp.call('clear',shell=True)

topN64bit = (2**64 - 1)/2
a = pl.randint(low=0, high=topN64bit, size=2, dtype=pl.int64)
b = pl.randint(low=0, high=topN64bit, size=3)
c = pl.randint(low=0, high=topN64bit, size=6)
d = pl.randint(low=0, high=topN64bit, size=3)
listOfArrs = [a,b,c,d]

# indSorted = pl.argsort(listOfArrs[2])

# print 
# print "type(listOfArrs)              :", type(listOfArrs)
# print "indices                       :", indSorted
# print "type(indSorted)               :", type(indSorted)
# print "type(listOfArrs[2][indSorted]):", type(listOfArrs[2][indSorted])
# print "listOfArrs[2][indSorted]      :"

# for i in listOfArrs[2][indSorted]:
#     print "\t\t\t\t",i

IDsNumber = 0
argOfMax  = 0
for i in range(len(listOfArrs)):
    if len(item[i]) > IDsNumber:
        IDsNumber = len(item[i]) # Updating
        argOfMax  = i # Largest record of IDs -> arrays' size
        pass
    
    continue

arrWithIndsSorted = pl.zeros( (len(listOfArrs), len(indSorted)),
                               dtype=pl.int64)

indSorted = pl.zeros

for i in pl.arange(len(listOfArrs)):
    
    numberOfIDs = len(listOfArrs[i])
    indsSorted = pl.argsort(listOfArrs[i])

    arrWithIndsSorted[ i , :numberOfIDs] = listOfArrs[i][indSorted]






# for i, j in zip(arrWithIndsSorted,listOfArrs[2][indSorted]):
#     print "\t\t\t\t", i, j