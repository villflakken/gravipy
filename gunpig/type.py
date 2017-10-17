# -*- coding: utf-8 -*-
# @Author: Boffen
# @Date:   2017-10-10 21:22:54
# @Last Modified by:   Boffen
# @Last Modified time: 2017-10-11 15:23:34

reading_parameters = {
# Data structure parameters
"what"      : ([ "PoS" ]),
"indraN"    : 2,
"iA"        : 0,
"iB"        : 0,
"subfolder" : 63,
"fftfile"   : None,

# Options
"sortIDs"    : True,        #   1/0     <=>     on/off
"lessprint"  : True,        #   1/0     <=>     on/off
"tmpfolder"  : True,        #   when using ".../indra'X'_tmp/..." data
# Extracts data from a coordinate box at positions specified:
"box_params" : ( (0.,20.), (0.,20.), (0.,5.) ),   # Turned off w/: None/False
# Apply floats as "((min,max), (min,max), (min,max))" in Mpc/h units,
# respectively for directions x, y, z.

# Output filename
"outputpath" : False,
# Write 2 file: Probably a bad idea...
"w2f"        : False,
# The most likely wanted output:
"plotdata"   : True
}
print " {0:10} : {1:10} - type={2:s} ".format("what", reading_parameters["what"], type(reading_parameters["what"]) )
print reading_parameters.keys()
print type(reading_parameters["what"])
# print reading_parameters["what"][0]
# print reading_parameters["what"][0].lower()
# print reading_parameters["what"][0]

# print ("subfolder" not in reading_parameters.keys() ) and ("fftfile" not in reading_parameters.keys())
# print reading_parameters["wow"]


# print all( hasattr( ((0.,20.), (0.,20.), (0.,5.)), '__iter__' ) )
iterable = ((0.,20.), (0.,20.), (0.,5.))
print all(map(lambda x: hasattr(x, '__iter__'), iterable))

print all(map(lambda x: hasattr(x, '__float__'), iterable[0]))