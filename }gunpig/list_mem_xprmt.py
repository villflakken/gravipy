import pylab as pl
import sys
list1 = []

for i in range(4):
    list1.append(pl.rand(3))
    continue

print "list1:"
print list1
print

size = 0
for item in range(len(list1)):
    size += list1[i].nbytes
    print "nbytes:", list1[i].nbytes
    size += sys.getsizeof(list1[i])
    print "sizeof iterated:", sys.getsizeof(list1[i])
    print
    continue

print "list1 size:" 
print size, "bytes"
print "getsizeof(list1):", sys.getsizeof(list1)

itemCheckList = list1[:]
arr1 = pl.zeros((4,3))
for j in range(4):
    arr1[j,:] = list1.pop(0)[:]
    print
    print "elements left in list1:", len(list1)
    itersize = 0
    
    for i in range(len(list1)):
        itersize += list1[i].nbytes
        itersize += sys.getsizeof(list1[i])
        continue

    print "iteration:", j, " -- list1 bytes:", itersize
    continue

print
print "list1 popped:"
print list1
print

print "arr1:"
print arr1
print 


print "itemChecklist :", all( [ all(arr1[i,:] == itemCheckList[i][:]) for i in range(len(arr1)) ] )
print "typecheck :" ,  all( [ type(arr1[i]) == type(itemCheckList[i]) for i in range(len(arr1)) ] )
print

arrconv = pl.array(itemCheckList)
print "arr1 == converted list :", type(arrconv) == type(arr1)
print