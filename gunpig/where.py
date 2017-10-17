# -*- coding: utf-8 -*-
# @Author: Boffen
# @Date:   2017-10-09 17:01:31
# @Last Modified by:   Boffen
# @Last Modified time: 2017-10-09 19:14:50
import numpy as N 


cords = N.array([ [[1.,1.,1.], [5., 5., 5]], [[1.,1.,1.], [5., 5., 5] ], [[1.,1.,1.], [5., 5., 5] ], [[1.,1.,1.], [5., 5., 2.] ] ])
print cords.shape
print
# bonds = [0.,1.]
# print N.where(0<cords[0,:,0] and 20.>cords[0,:,0])
# print cords[:,:,0]>=5.
# print N.where(cords[:,:,0]>=5.)
# print 
# print N.where(cords[:,:,0]>=5.)[0]
# print N.where(cords[:,:,0]<=20.)
# print N.where(cords[:,:,0]<=20.)[0]

args = N.array(cords[:,:,0]>=5.) * N.array(cords[:,:,1]>=5.) * N.array(cords[:,:,2]>=5.)
# print cords
print args
print
print cords[args]
print
print "sum:", N.sum(args)

print type(cords[:,:,1]>=5.)
print


print ([0.,20.],[0.,20.],[0.,5.]) != 0 and ([0.,20.],[0.,20.],[0.,5.]) != None
