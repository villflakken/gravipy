import subprocess as sp
import pylab as pl
tmp = sp.call('clear',shell=True)

print "-"*80

print "\n *** NUMPYSORTING ***\n"
arr0 = pl.array(["010", "201", "999", "150", "199", "001", "200", "99"],
                )#dtype=pl.int64)
arr0sorted = pl.sort(arr0)
arr1 = pl.array([10, 201, 999, 150, 199, 1, 200, 99],
                dtype=pl.int64)
arr1sorted = pl.sort(arr1)
print "arr0:", arr0
print "arr1:", arr1
print 
print "arr0sorted:  | arr1sorted:"
for x, y in zip(arr0sorted, arr1sorted):
    print "{x:>11d}  | {y:>11d}".format(x=int(x), y=int(y))

print
print "-"*80

print "\n *** PYTHONSORTING ***\n"
a = [ "10", "201", "999", "150", "199",   "1", "200",  "99"]
b = ["010", "201", "999", "150", "199", "001", "200", "099"]
print "list0:", a
print "list1:", b
a.sort(key=float)
b.sort(key=float)
print 
print "list0sorted:  | list1sorted: (key=float)"
for x, y in zip(a, b):
    print "{x:>11d}   | {y:>11d}".format(x=int(x), y=int(y))


print 
print "-"*80
a = [ "10", "201", "999", "150", "199",   "1", "200",  "99"]
b = ["010", "201", "999", "150", "199", "001", "200", "099"]
print "list2:", a
print "list3:", b
a.sort()
b.sort()
print 
print "list2sorted:  | list3sorted:"
for x, y in zip(a, b):
    print "{x:>11d}   | {y:>11d}".format(x=int(x), y=int(y))
print
print "-"*80




# print arr0sorted
# print arr1sorted